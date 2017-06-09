from broadsoft.Device import Device
from broadsoft.lib.BroadsoftObject import BroadsoftObject
from broadsoft.requestobjects.UserAddRequest import UserAddRequest
from broadsoft.requestobjects.UserGetRequest import UserGetRequest
from broadsoft.requestobjects.UserModifyRequest import UserModifyRequest
from broadsoft.requestobjects.UserServiceAssignListRequest import UserServiceAssignListRequest
from broadsoft.requestobjects.UserSharedCallAppearanceAddEndpointRequest import \
    UserSharedCallAppearanceAddEndpointRequest
from broadsoft.requestobjects.UserSharedCallAppearanceGetRequest import UserSharedCallAppearanceGetRequest
from broadsoft.requestobjects.UserVoiceMessagingUserModifyVoiceManagementRequest import UserVoiceMessagingUserModifyVoiceManagementRequest
from broadsoft.requestobjects.UserThirdPartyVoiceMailSupportModifyRequest import UserThirdPartyVoiceMailSupportModifyRequest
from broadsoft.requestobjects.lib.BroadsoftRequest import BroadsoftRequest


class Account(BroadsoftObject):
    # these are optional broadsoft services that will get applied by default to every new
    # account
    default_services = [
        'Shared Call Appearance 10',
        'Third-Party Voice Mail Support',
        'Voice Messaging User'
    ]

    def __init__(self, did=None, extension=None, last_name=None, first_name=None,
                 sip_user_id=None, kname=None, email=None, services=None,
                 sip_password=None, **kwargs):
        self.did = did
        self.email = email
        self.first_name = first_name
        self.kname = kname
        self.last_name = last_name
        self.services = self.default_services
        if services:
            if type(services) == str:
                services = [services]
            self.services = services

        # these are optional; will be derived by broadsoft.RequestObjects as needed
        self.extension = extension
        self.sip_user_id = sip_user_id

        # fully optional
        self.devices = []   # Devices associated with this Account (should be broadsoft.Device objects)
        self.sip_password = sip_password

        BroadsoftObject.__init__(self, **kwargs)

    def __repr__(self):
        return "<Broadsoft Account did:%s, last_name:%s, first_name:%s, sip_user_id:%s>" % (self.did, self.last_name, self.first_name, self.sip_user_id)

    def activate_broadsoft_voicemail(self, voice_message_delivery_email_address=None,
                                     use_phone_message_waiting_indicator=False,
                                     send_voice_message_notify_email=True,
                                     voice_message_notify_email_address=None,
                                     send_carbon_copy_voice_message=False,
                                     voice_message_carbon_copy_email_address=None,
                                     transfer_on_zero_to_phone_number=False, transfer_phone_number=None,
                                     always_redirect_to_voice_mail=False, busy_redirect_to_voice_mail=True,
                                     no_answer_redirect_to_voice_mail=True,
                                     out_of_primary_zone_redirect_to_voice_mail=False):
        if not self.sip_user_id:
            raise ValueError("can't call Account.activate_unity_voicemail without a value for sip_user_id")

        if not self.email:
            raise ValueError("can't call Account.activate_unity_voicemail without a value for email")

        if voice_message_notify_email_address is None:
            voice_message_notify_email_address = self.email

        if voice_message_delivery_email_address is None:
            voice_message_delivery_email_address = self.email

        # going to do this as a compound request so that it's pseudo-atomic...if one fails, the rest should
        # fail, regardless of where in the process that failure occurs
        b = BroadsoftRequest()
        self.inject_broadsoftinstance(child=b)

        # activate broadsoft voicemail
        # makes more sense to deactivate unity first, but this is the step that's more likely to fail, so might as well
        # put it first
        activate = UserVoiceMessagingUserModifyVoiceManagementRequest(sip_user_id=self.sip_user_id, is_active=True,
                                     processing='Deliver To Email Address Only',
                                     voice_message_delivery_email_address=voice_message_delivery_email_address,
                                     use_phone_message_waiting_indicator=use_phone_message_waiting_indicator,
                                     send_voice_message_notify_email=send_voice_message_notify_email,
                                     voice_message_notify_email_address=voice_message_notify_email_address,
                                     send_carbon_copy_voice_message=send_carbon_copy_voice_message,
                                     voice_message_carbon_copy_email_address=voice_message_carbon_copy_email_address,
                                     transfer_on_zero_to_phone_number=transfer_on_zero_to_phone_number,
                                     transfer_phone_number=transfer_phone_number,
                                     always_redirect_to_voice_mail=always_redirect_to_voice_mail,
                                     busy_redirect_to_voice_mail=busy_redirect_to_voice_mail,
                                     no_answer_redirect_to_voice_mail=no_answer_redirect_to_voice_mail,
                                     out_of_primary_zone_redirect_to_voice_mail=out_of_primary_zone_redirect_to_voice_mail)

        # deactivate unity
        deactivate = UserThirdPartyVoiceMailSupportModifyRequest(sip_user_id=self.sip_user_id, is_active=False)

        b.commands = [activate, deactivate]
        b.post()

    def activate_unity_voicemail(self, busy_redirect_to_voice_mail=True, no_answer_redirect_to_voice_mail=True,
                                 no_answer_number_of_rings=3, always_redirect_to_voice_mail=False):
        if not self.sip_user_id:
            raise ValueError("can't call Account.activate_unity_voicemail without a value for sip_user_id")

        # going to do this as a compound request so that it's pseudo-atomic...if one fails, the rest should
        # fail, regardless of where in the process that failure occurs
        b = BroadsoftRequest()
        self.inject_broadsoftinstance(child=b)

        # activate unity voicemail
        # makes more sense to deactivate broadsoft first, but this is the step that's more likely to fail, so might as well
        # put it first
        activate = UserThirdPartyVoiceMailSupportModifyRequest(sip_user_id=self.sip_user_id, is_active=True,
                                                               busy_redirect_to_voice_mail=busy_redirect_to_voice_mail,
                                                               no_answer_redirect_to_voice_mail=no_answer_redirect_to_voice_mail,
                                                               user_server=6172530000, mailbox_id_type='User Or Group Phone Number',
                                                               no_answer_number_of_rings=no_answer_number_of_rings,
                                                               always_redirect_to_voice_mail=always_redirect_to_voice_mail,
                                                               out_of_primary_zone_redirect_to_voice_mail=False)

        # deactivate broadsoft
        deactivate = UserVoiceMessagingUserModifyVoiceManagementRequest(sip_user_id=self.sip_user_id, is_active=False)

        b.commands = [activate, deactivate]
        b.post()

    def add_devices(self, req_object):
        if len(self.devices) > 0:
            for d in self.devices:
                # error if missing line_port at this time
                if d.line_port is None:
                    raise RuntimeError("The device " + str(d) + " does not have a line_port specified. One can be automatically generated with a DID and MAC address.")

                # all devices get added to system
                self.inject_broadsoftinstance(child=d)
                d_ro = d.build_provision_request()
                req_object.commands.append(d_ro)

            # first device gets associated directly with user
            self.link_primary_device(req_object=req_object, device=self.devices[0])

            # remaining devices get added as shared call appearances
            for d in self.devices[1:]:
                self.link_sca_device(req_object=req_object, device=d)

    def add_services(self, req_object):
        if self.services and len(self.services) > 0:
            s = UserServiceAssignListRequest()
            self.inject_broadsoftinstance(child=s)
            s.did = self.did
            s.sip_user_id = self.sip_user_id
            s.services = self.services
            req_object.commands.append(s)

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

        return b

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

    def fetch(self):
        self.xml = UserGetRequest.get_user(did=self.did, sip_user_id=self.sip_user_id, broadsoftinstance=self.broadsoftinstance)
        self.from_xml()

    def from_xml(self):
        BroadsoftObject.from_xml(self)
        self.devices = list()
        if self.xml:
            cmd = self.xml.findall('command')[0]
            self.did = cmd.findall('phoneNumber')[0].text
            self.first_name = cmd.findall('firstName')[0].text
            self.last_name = cmd.findall('lastName')[0].text
            self.extension = cmd.findall('extension')[0].text
            self.sip_user_id = cmd.findall('defaultAlias')[0].text
        self.load_devices()

    def generate_sip_password(self):
        if self.sip_password is None:
            import random
            self.sip_password = str(random.randint(1000000000, 9999999999))

    def link_primary_device(self, req_object, device):
        u_mod = UserModifyRequest(did=self.did, sip_user_id=self.sip_user_id, device_name=device.name,
                                  line_port=device.line_port)
        self.inject_broadsoftinstance(child=u_mod)
        req_object.commands.append(u_mod)

    def link_sca_device(self, req_object, device):
        line_port = device.line_port
        sca = UserSharedCallAppearanceAddEndpointRequest(sip_user_id=self.sip_user_id,
                                                         device_name=device.name, line_port=line_port)
        self.inject_broadsoftinstance(child=sca)
        req_object.commands.append(sca)

    def load_devices(self):
        # first, any that were directly in xml
        if self.xml:
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

    def provision(self):
        BroadsoftObject.prep_attributes(self)

        if not self.sip_password:
            self.generate_sip_password()

        BroadsoftObject.provision(self)

        # Not making this part atomic since I want to leverage set_device_passwords(), so it gets called outside of
        # build_provision_request. Seems reasonable to not make the entire request fail if this part does anyway.
        if self.sip_password:
            self.set_device_passwords(new_sip_password=self.sip_password)

    def set_device_passwords(self, new_sip_password=None):
        if not self.sip_user_id and not self.did:
            raise ValueError("can't run Account.set_device_passwords without a value for sip_user_id or did")

        if not new_sip_password and self.sip_password:
            new_sip_password = self.sip_password

        if not self.devices or len(self.devices) == 0:
            self.load_devices()

        for d in self.devices:
            self.inject_broadsoftinstance(child=d)
            d.set_password(sip_user_name=self.sip_user_id, did=self.did, sip_password=new_sip_password)

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
