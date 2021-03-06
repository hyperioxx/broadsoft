import broadsoft.requestobjects.lib.BroadsoftRequest
from broadsoft.Device import Device
from broadsoft.lib.BroadsoftObject import BroadsoftObject
from broadsoft.requestobjects.UserAddRequest import UserAddRequest
from broadsoft.requestobjects.UserGetRequest import UserGetRequest
from broadsoft.requestobjects.UserModifyRequest import UserModifyRequest
from broadsoft.requestobjects.UserServiceAssignListRequest import UserServiceAssignListRequest
from broadsoft.requestobjects.UserSharedCallAppearanceAddEndpointRequest import \
    UserSharedCallAppearanceAddEndpointRequest
from broadsoft.requestobjects.UserSharedCallAppearanceGetRequest import UserSharedCallAppearanceGetRequest
from broadsoft.requestobjects.lib.BroadsoftRequest import BroadsoftRequest
from broadsoft.Voicemail import Voicemail
from broadsoft.requestobjects.UserVoiceMessagingUserModifyVoiceManagementRequest import \
    UserVoiceMessagingUserModifyVoiceManagementRequest
from broadsoft.requestobjects.UserThirdPartyVoiceMailSupportModifyRequest import \
    UserThirdPartyVoiceMailSupportModifyRequest
from broadsoft.requestobjects.UserDeleteRequest import UserDeleteRequest
from broadsoft.requestobjects.UserGetListInGroupRequest import UserGetListInGroupRequest
from broadsoft.requestobjects.UserSharedCallAppearanceDeleteEndpointListRequest import \
    UserSharedCallAppearanceDeleteEndpointListRequest
from broadsoft.requestobjects.UserAuthenticationModifyRequest import UserAuthenticationModifyRequest
from broadsoft.requestobjects.UserSharedCallAppearanceModifyRequest import UserSharedCallAppearanceModifyRequest
import re
import logging


class Account(BroadsoftObject):
    # default_service_pack = 'MIT-Pack'
    default_service_pack = None

    def __init__(self, default_device_count=36, did=None, extension=None, last_name=None, first_name=None,
                 sip_user_id=None, kname=None, email=None, services=None, service_pack=None,
                 sip_password=None, voicemail='broadsoft', voicemail_mwi=None, **kwargs):
        self.default_device_count = default_device_count
        self.did = did
        self.email = email
        self.first_name = first_name
        self.kname = kname
        self.last_name = last_name
        self.service_pack = self.default_service_pack
        if service_pack:
            self.service_pack = service_pack
        self.services = self.load_default_services()
        if services:
            if type(services) == str:
                services = [services]
            self.services = services
        self.voicemail = voicemail

        # these are optional; will be derived by broadsoft.RequestObjects as needed
        self.extension = extension
        self.sip_user_id = sip_user_id

        # fully optional
        self.devices = []  # Devices associated with this Account (should be broadsoft.Device objects)
        self.sip_password = sip_password
        self.voicemail_mwi = voicemail_mwi

        self.old_did = self.did
        BroadsoftObject.__init__(self, **kwargs)

    def __repr__(self):
        return "<Broadsoft Account did:%s, last_name:%s, first_name:%s, sip_user_id:%s>" % (
            self.did, self.last_name, self.first_name, self.sip_user_id)

    def activate_voicemail(self, type=None, voicemail_object=None):
        if not self.sip_user_id:
            raise ValueError("can't call Account.activate_unity_voicemail without a value for sip_user_id")

        # no type provided? inherit from object.
        if type is None:
            type = self.voicemail

        # user didn't specify a custom Voicemail object? Instantiate the default for the given type.
        if voicemail_object is None:
            voicemail_object = Voicemail(type=type, broadsoftinstance=self.broadsoftinstance,
                                         logging_level=self.logging_level)

        # get email, sip_user_id, and mwi into voicemail object, whether constructed or passed
        if voicemail_object.email is None:
            voicemail_object.email = self.email
        if voicemail_object.sip_user_id is None:
            voicemail_object.sip_user_id = self.sip_user_id
        if voicemail_object.mwi is None:
            voicemail_object.mwi = self.voicemail_mwi
        if voicemail_object.sip_password is None:
            voicemail_object.sip_password = self.sip_password
        if voicemail_object.did is None:
            voicemail_object.did = self.did

        # going to do this as a compound request so that it's pseudo-atomic...if one fails, the rest should
        # fail, regardless of where in the process that failure occurs
        b = BroadsoftRequest()
        self.inject_broadsoftinstance(child=b)

        # build XML to activate chosen voicemail system
        # makes more sense to deactivate counterpart first, but this is the step that's more likely to fail, so might
        # as well put it first
        activate = voicemail_object.build_activate_command()

        # build XML to deactivate counterpart
        deactivate = voicemail_object.build_deactivate_counterpart_command()

        b.commands = activate + deactivate
        b.post()
        return [b]

    def add_devices(self, req_object):
        # delete primary device first so we don't run into "Exceeded maximum number of allowed appearances" error

        # delete all shared call appearances applied to user
        d_list = UserSharedCallAppearanceGetRequest.get_devices(broadsoftinstance=self.broadsoftinstance,
                                                                sip_user_id=self.sip_user_id)
        if len(d_list) > 0:
            devices = []
            for r in d_list:
                device = {'line_port': r['Line/Port'], 'name': r['Device Name']}
                devices.append(device)
            del_d = UserSharedCallAppearanceDeleteEndpointListRequest(broadsoftinstance=self.broadsoftinstance,
                                                                      sip_user_id=self.sip_user_id, devices=devices)
            req_object.commands.append(del_d)

        one_primary = False
        if len(self.devices) > 0:
            for d in self.devices:
                if d.is_primary:
                    if one_primary:
                        raise RuntimeError("attempted to create more than one primary device")
                    one_primary = True
                    self.link_primary_device(req_object=req_object, device=d)

                else:
                    self.link_sca_device(req_object=req_object, device=d)

    def add_services(self, req_object):
        if self.services_defined():
            s = UserServiceAssignListRequest()
            self.inject_broadsoftinstance(child=s)
            s.did = self.did
            s.sip_user_id = self.sip_user_id
            s.services = self.services
            s.service_pack = self.service_pack
            req_object.commands.append(s)

    def attach_default_devices(self):
        self.attach_primary_device()

        while not self.derive_enough_devices():
            self.attach_sca()

    def attach_default_devices__build_description(self):
        description = ''
        if self.last_name:
            description = self.last_name

        if self.first_name:
            if self.last_name:
                description = self.first_name + ' ' + self.last_name
            else:
                description = self.first_name

        return description

    def attach_primary_device(self):
        # attach a primary device, with no line_port suffix
        d = Device(logging_level=self.logging_level)
        d.broadsoftinstance = self.broadsoftinstance
        d.logging_level = self.logging_level
        d.is_primary = True
        d.did = self.did
        d.description = self.attach_default_devices__build_description()
        d.type = 'Generic SIP Phone'
        d.derive_line_port()
        d.implicit_overwrite = False
        d.skip_if_exists = True
        self.devices.append(d)

    def attach_sca(self, index=None):
        d = Device(logging_level=self.logging_level)
        d.index = self.derive_sca_index(index=index)
        d.broadsoftinstance = self.broadsoftinstance
        d.logging_level = self.logging_level
        d.is_primary = False
        d.did = self.did
        d.description = self.attach_default_devices__build_description()
        d.type = 'Generic SIP Phone'
        d.derive_line_port()
        d.implicit_overwrite = False
        d.skip_if_exists = True

        self.devices.append(d)

    def build_modify_object(self):
        kwargs = {
            'did': self.did,
            'sip_user_id': self.sip_user_id,
            'broadsoftinstance': self.broadsoftinstance,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email_address': self.email
        }

        u = UserModifyRequest(**kwargs)
        self.inject_broadsoftinstance(child=u)
        return u

    def build_provision_request(self):
        # going to do this as a compound request so that it's pseudo-atomic...if one fails, the rest should
        # fail, regardless of where in the process that failure occurs
        b = BroadsoftRequest()
        self.inject_broadsoftinstance(child=b)

        # object to create the user
        u_add = UserAddRequest()
        self.inject_broadsoftinstance(child=u_add)
        u_add.first_name = self.first_name
        u_add.last_name = self.last_name
        u_add.did = self.did
        u_add.kname = self.kname
        u_add.sip_user_id = self.sip_user_id
        u_add.sip_password = self.sip_password
        u_add.email = self.email
        b.commands = [u_add]

        # if there are services to add for user, add them
        self.add_services(req_object=b)

        # if there are devices to add for user, add them
        self.add_devices(req_object=b)

        # default settings for all SCAs, set once per account
        self.configure_sca_settings(req_object=b)

        # set authentication creds
        self.set_auth_creds(req_object=b)

        return b

    def configure_sca_settings(self, req_object):
        self.prep_attributes()

        if self.sip_user_id is None:
            self.derive_sip_user_id(did=self.did)

        u = UserSharedCallAppearanceModifyRequest()
        self.inject_broadsoftinstance(child=u)

        u.sip_user_id = self.sip_user_id
        u.alert_all_appearances_for_click_to_dial_calls = True
        u.alert_all_appearances_for_group_paging_calls = True
        u.allow_sca_call_retrieve = True
        u.multiple_call_arrangement_is_active = True
        u.allow_bridging_between_locations = True
        u.enable_call_park_notification = True
        u.bridge_warning_tone = 'None'

        req_object.commands.append(u)

    def deactivate_unity_voicemail(self):
        if not self.sip_user_id:
            raise ValueError("can't call Account.deactivate_unity_voicemail without a value for sip_user_id")

        UserThirdPartyVoiceMailSupportModifyRequest.deactivate_unity_voicemail(sip_user_id=self.sip_user_id,
                                                                               broadsoftinstance=self.broadsoftinstance)

    def deactivate_broadsoft_voicemail(self):
        if not self.sip_user_id:
            raise ValueError("can't call Account.deactivate_unity_voicemail without a value for sip_user_id")

        UserVoiceMessagingUserModifyVoiceManagementRequest.deactivate_broadsoft_voicemail(sip_user_id=self.sip_user_id,
                                                                                          broadsoftinstance=self.broadsoftinstance)

    def delete(self, delete_devices=False):
        self.prep_attributes()

        if delete_devices and len(self.devices) == 0:
            self.load_devices()

        if self.sip_user_id is None:
            raise ValueError("can't call Account.delete() without a value for sip_user_id")

        # going to do this as a compound request so that it's pseudo-atomic...if one fails, the rest should
        # fail, regardless of where in the process that failure occurs
        b = BroadsoftRequest()
        self.inject_broadsoftinstance(child=b)

        # build XML to delete user
        user = UserDeleteRequest(sip_user_id=self.sip_user_id)
        b.commands = [user]

        # -- doing no device management in broadsoft, therefore no need for
        # -- "clear the decks behavior"...create device. Exists already? Fine.
        # for each device, add XML for device deletion
        # for d in self.devices:
        #    b.commands.append(d.delete(bundle=True))

        b.post()
        return [b]

    def derive_enough_devices(self):
        if len(self.devices) < self.default_device_count:
            return False

        return True

    def derive_sca_index(self, index=None):
        if index is not None:
            return index

        else:
            highest_index = 0
            for d in self.devices:
                if d.index is not None and int(d.index) > highest_index:
                    highest_index = d.index
            return highest_index + 1

    # want to make sure type doesn't get in the way, so extending explicit method
    def did_changed(self):
        if str(self.did) == str(self.old_did):
            return False
        return True

    def fetch(self, get_devices=True):
        self.xml = UserGetRequest.get_user(sip_user_id=self.sip_user_id, broadsoftinstance=self.broadsoftinstance)
        self.from_xml(get_devices=get_devices)
        self.set_old_did()

    def from_xml(self, get_devices=True):
        BroadsoftObject.from_xml(self)
        self.devices = list()
        if self.xml:
            cmd = self.xml.findall('command')[0]
            if cmd.findall('phoneNumber'):
                self.did = cmd.findall('phoneNumber')[0].text
            if cmd.findall('firstName'):
                self.first_name = cmd.findall('firstName')[0].text
            if cmd.findall('lastName'):
                self.last_name = cmd.findall('lastName')[0].text
            if cmd.findall('extension'):
                self.extension = cmd.findall('extension')[0].text
            if cmd.findall('defaultAlias'):
                self.sip_user_id = cmd.findall('defaultAlias')[0].text
            if cmd.findall('emailAddress'):
                self.email = cmd.findall('emailAddress')[0].text

        if get_devices:
            self.load_devices()

    def generate_sip_password(self):
        if self.sip_password is None:
            import random
            self.sip_password = str(random.randint(1000000000, 9999999999))

    def link_primary_device(self, req_object, device):
        u_mod = UserModifyRequest(did=self.did, sip_user_id=self.sip_user_id, device_name=device.name,
                                  line_port=device.line_port, include_endpoint=True)
        self.inject_broadsoftinstance(child=u_mod)
        req_object.commands.append(u_mod)

    def link_sca_device(self, req_object, device):
        line_port = device.line_port
        sca = UserSharedCallAppearanceAddEndpointRequest(sip_user_id=self.sip_user_id, line_port=line_port)
        self.inject_broadsoftinstance(child=sca)
        req_object.commands.append(sca)

    def load_default_services(self):
        services = [
            # 'Advice Of Charge',
            'Alternate Numbers',
            'Anonymous Call Rejection',
            'Authentication',
            'Automatic Callback',
            'Automatic Hold/Retrieve',
            'Barge-in Exempt',
            'Basic Call Logs',
            'BroadTouch Business Communicator Desktop',
            'BroadTouch Business Communicator Desktop - Audio',
            'Client License 18', # API name for 'BroadTouch Business Communicator Desktop - Video',
            'BroadTouch Business Communicator Mobile',
            'BroadTouch Business Communicator Mobile - Audio',
            'Client License 17', # API name for 'BroadTouch Business Communicator Mobile - Video',
            #'BroadTouch Business Communicator Tablet',
            #'BroadTouch Business Communicator Tablet - Audio',
            #'BroadTouch Business Communicator Tablet - Video',
            'Client License 19', # API name for 'BroadTouch MobileLink',
            'BroadWorks Agent',
            'BroadWorks Anywhere',
            'Client License 4', # API name for 'BroadWorks Receptionist - Enterprise',
            'BroadWorks Receptionist - Office',
            'BroadWorks Receptionist - Small Business',
            'BroadWorks Supervisor',
            'Busy Lamp Field',
            'Call Center - Basic',
            'Call Center - Premium',
            'Call Center - Standard',
            'Call Center Monitoring',
            'Call Forwarding Always',
            'Call Forwarding Busy',
            'Call Forwarding No Answer',
            'Call Forwarding Not Reachable',
            'Call Forwarding Selective',
            'Calling Line ID Delivery Blocking',
            'Calling Name Delivery',
            # 'Calling Name Retrieval',
            'Calling Number Delivery',
            'Calling Party Category',
            'Call Me Now',
            'Call Notify',
            #'Call Recording',
            'Call Return',
            'Call Transfer',
            'Call Waiting',
            'Charge Number',
            'Classmark',
            'Collaborate - Audio',
            'Collaborate - Sharing',
            'Collaborate - Video',
            'Connected Line Identification Presentation',
            'Connected Line Identification Restriction',
            'Customer Originated Trace',
            'Custom Ringback User',
            'Custom Ringback User - Call Waiting',
            'Custom Ringback User - Video',
            'Directed Call Pickup',
            'Directed Call Pickup with Barge-in',
            # 'Directory Number Hunting',
            'Diversion Inhibitor',
            'Do Not Disturb',
            'Executive',
            'Executive-Assistant',
            'External Calling Line ID Delivery',
            'Fax Messaging',
            'Flash Call Hold',
            'Flexible Seating Guest',
            'Group Night Forwarding',
            'Hoteling Guest',
            'Hoteling Host',
            'In-Call Service Activation',
            'Integrated IMP',
            'Intercept User',
            'Internal Calling Line ID Delivery',
            'Last Number Redial',
            'Multiple Call Arrangement',
            'Music On Hold User',
            'MWI Delivery to Mobile Endpoint',
            'N-Way Call',
            #'Personal Assistant',
            'Physical Location',
            'Polycom Phone Services',
            'Pre-alerting Announcement',
            'Preferred Carrier User',
            'Priority Alert',
            'Privacy',
            'Push to Talk',
            'Remote Office',
            'Route List',
            # 'Security Classification',
            'Selective Call Acceptance',
            'Selective Call Rejection',
            'Sequential Ring',
            'Shared Call Appearance',
            'Shared Call Appearance 10',
            'Shared Call Appearance 15',
            'Shared Call Appearance 20',
            'Shared Call Appearance 25',
            'Shared Call Appearance 30',
            'Shared Call Appearance 35',
            'Simultaneous Ring Personal',
            'Speed Dial 100',
            'Speed Dial 8',
            'Third-Party MWI Control',
            'Third-Party Voice Mail Support',
            'Three-Way Call',
            'Two-Stage Dialing',
            'Video On Hold User',
            'Virtual On-Net Enterprise Extensions',
            'Voice Messaging User',
            'Voice Messaging User - Video',
            'Voice Portal Calling'
        ]

        return services

    def load_devices(self):
        # if there's no XML for the user, fetch entire User. Primary device will be in User record, rest found by
        # searching for shared call appearances. Since .fetch() calls .load_devices(), will wind up back here.
        if self.xml is None:
            self.fetch()

        # if there is XML for the user...
        else:
            # first, any that were directly in xml
            for ade in self.xml.findall('./command/accessDeviceEndpoint'):
                d = Device()
                self.inject_broadsoftinstance(child=d)
                # the <accessDeviceEndpoint> gives us enough info to actually fetch the device
                d.bootstrap_access_device_endpoint(ade=ade)
                d.fetch(target_name=d.name)
                self.devices.append(d)

            # now find any shared call appearances
            sca_xml = UserSharedCallAppearanceGetRequest.get_devices(sip_user_id=self.sip_user_id,
                                                                     broadsoftinstance=self.broadsoftinstance)
            scas = BroadsoftRequest.convert_results_table(xml=sca_xml)
            for sca in scas:
                d = Device()
                self.inject_broadsoftinstance(child=d)
                # the shared call appearance listings give us nearly everything about a device, but we run a fetch as well
                # to get everything
                d.bootstrap_shared_call_appearance(sca=sca)
                d.fetch(target_name=d.name)
                self.devices.append(d)

    def modify(self):
        # call prep_attributes(); want to make sure attrs that depend on other attrs get updated (such as sip_user_id,
        # etc)
        self.prep_attributes()

        # DID didn't change? can run as modify
        if not self.did_changed():
            mod = self.build_modify_object()
            mod.post()

        # if the DID did change, delete and re provision (in broadsoft, key is sip_user_id, which is built from DID)
        else:
            self.delete(delete_devices=True)
            self.sip_user_id = self.derive_sip_user_id(did=self.did)
            self.provision()

    def overwrite(self):
        logging.getLogger('broadsoftapi').info("overwriting pre-existing account for DID: " + str(self.did),
                     extra={'session_id': self.broadsoftinstance.session_id})

        # here should derive sip_user_id if not present
        if not self.sip_user_id:
            self.did = self.derive_sip_user_id(did=self.did)
            logging.getLogger('broadsoftapi').info("overwriting pre-existing account for DID: " + str(self.did) +
                         ", derived " + str(self.sip_user_id) + " as sip_user_id",
                         extra={'session_id': self.broadsoftinstance.session_id})

        if self.sip_user_id is not None:
            logging.getLogger('broadsoftapi').info("overwriting pre-existing account for DID: " + str(self.did) +
                         ", executing",
                         extra={'session_id': self.broadsoftinstance.session_id})

            try:
                self.delete()

            except RuntimeError as e:
                if 'the SOAP server threw an error: [Error 4008] User not found: ' not in str(e):
                    raise (e)
                pass

    def provision(self):
        BroadsoftObject.prep_attributes(self)

        if not self.sip_password:
            self.generate_sip_password()

        # each new account gets 36 non-specific devices attached to it. we're doing no device management in broadsoft.
        if len(self.devices) == 0 or self.devices is None:
            self.attach_default_devices()

        BroadsoftObject.provision(self)

        # set up voicemail
        # Not making this part atomic since it seems reasonable to not make the entire request fail if this part does.
        if self.voicemail:
            self.activate_voicemail()

    def services_defined(self):
        if self.service_pack is not None:
            return True

        if self.services and len(self.services) > 0:
            return True

        return False

    def set_auth_creds(self, req_object):
        self.prep_attributes()

        if self.did is None:
            raise ValueError("can't run Account.set_auth_creds() without a did")

        if self.sip_password is None:
            self.generate_sip_password()

        if self.sip_user_id is None:
            self.derive_sip_user_id(did=self.did)

        u = UserAuthenticationModifyRequest()
        self.inject_broadsoftinstance(child=u)
        u.did = self.did
        u.sip_user_id = self.sip_user_id
        u.new_password = self.sip_password

        req_object.commands.append(u)

    def set_device_passwords(self, new_sip_password=None):
        if not self.sip_user_id and not self.did:
            raise ValueError("can't run Account.set_device_passwords without a value for sip_user_id or did")

        if not new_sip_password and self.sip_password:
            new_sip_password = self.sip_password

        if new_sip_password is None:
            raise ValueError("can't run Account.set_device_passwords() with providing a password")

        if not self.devices or len(self.devices) == 0:
            self.load_devices()

        for d in self.devices:
            if d.is_primary:
                self.inject_broadsoftinstance(child=d)
                d.set_password(sip_user_name=self.sip_user_id, did=self.did, sip_password=new_sip_password)

    def set_old_did(self):
        self.old_did = str(self.did)

    def set_portal_password(self, sip_password=None):
        new_password = sip_password
        if not sip_password:
            new_password = self.sip_password
        else:
            self.sip_password = new_password

        if not self.did and not self.sip_user_id:
            raise AttributeError("can't reset Account sip_password without a did or sip_user_did set")

        if not new_password:
            raise AttributeError("can't reset Account sip_password without a value for sip_password")

        UserModifyRequest.set_password(did=self.did, sip_user_id=self.sip_user_id, new_password=new_password,
                                       broadsoftinstance=self.broadsoftinstance)

    @staticmethod
    def get_accounts(instance='prod', **kwargs):
        if 'broadsoftinstance' not in kwargs or kwargs['broadsoftinstance'] is None:
            i = broadsoft.requestobjects.lib.BroadsoftRequest.instance_factory(instance=instance)
            kwargs['broadsoftinstance'] = i

        accounts = []
        results = UserGetListInGroupRequest.list_users(**kwargs)
        for row in results:
            sip_user_id = row['User Id']
            last_name = row['Last Name']
            email = row['Email Address']
            did = row['Phone Number']
            first_name = row['First Name']
            extension = row['Extension']

            a = Account(sip_user_id=sip_user_id, last_name=last_name, email=email, did=did, first_name=first_name,
                        extension=extension, **kwargs)
            accounts.append(a)
        return accounts

    @staticmethod
    def split_name(name):
        last_name = name
        first_name = None

        s = re.search(r'(.+?) (\S+)$', name)
        if s:
            first_name = s.group(1)
            last_name = s.group(2)

        return (first_name, last_name)

    @staticmethod
    def thaw_from_db(user_record, voicemail='broadsoft', voicemail_mwi=True,
                     force_when_no_devices=False, skip_if_exists=True, **kwargs):
        from mitroles.MitRoles import MitRoles

        (firstname, lastname) = Account.split_name(name=user_record.display_name)

        owner = None
        r = MitRoles()
        owners = r.get_owners_for_did(did=user_record.did)
        if owners and len(owners) > 0:
            owner = owners[0]

        # build the user
        a = Account(skip_if_exists=skip_if_exists, **kwargs)
        a.did = user_record.did
        a.first_name = firstname
        a.last_name = lastname
        a.voicemail = voicemail
        a.sip_password = user_record.password
        a.voicemail_mwi = voicemail_mwi

        if owner:
            a.kname = owner
            a.email = owner + '@mit.edu'

        a.provision()

        return a
