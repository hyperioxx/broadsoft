from broadsoft.lib.BroadsoftObject import BroadsoftObject
from broadsoft.requestobjects.UserVoiceMessagingUserModifyVoiceManagementRequest import UserVoiceMessagingUserModifyVoiceManagementRequest
from broadsoft.requestobjects.UserThirdPartyVoiceMailSupportModifyRequest import UserThirdPartyVoiceMailSupportModifyRequest
from broadsoft.requestobjects.UserVoiceMessagingUserModifyAdvancedVoiceManagementRequest import UserVoiceMessagingUserModifyAdvancedVoiceManagementRequest
from broadsoft.requestobjects.lib.BroadsoftRequest import BroadsoftRequest
from broadsoft.requestobjects.UserServiceAssignListRequest import UserServiceAssignListRequest
from broadsoft.requestobjects.UserServiceUnassignListRequest import UserServiceUnassignListRequest


class Voicemail(BroadsoftObject):
    unity_number = 6172530000

    def __init__(self, behavior='email', busy_to_voicemail=True, cc_email=None, did=None, email=None, mwi=None,
                 no_answer_to_voicemail=True, rings=3, straight_to_voicemail=False, send_cc=False, sip_user_id=None,
                 type='broadsoft', transfer_on_zero=False, transfer_number=None, sip_password=None, surgemail_domain=None,
                 **kwargs):
        self.behavior = behavior                            # "email" or "store" (on server)
        self.busy_to_voicemail = busy_to_voicemail
        self.cc_email = cc_email
        self.did = did
        self.email = email
        self.mwi = mwi
        self.no_answer_to_voicemail = no_answer_to_voicemail
        self.rings = rings
        self.send_cc = send_cc
        self.sip_password = sip_password
        self.sip_user_id = sip_user_id
        self.straight_to_voicemail = straight_to_voicemail
        self.surgemail_domain=surgemail_domain
        self.transfer_on_zero = transfer_on_zero
        self.transfer_number = transfer_number
        self.type = type                                    # broadsoft or unity

        BroadsoftObject.__init__(self, **kwargs)

        if self.surgemail_domain is None:
            self.surgemail_domain = self.broadsoftinstance.surgemail_domain

    def build_activate_command(self):
        self.validate()

        command = []

        # add relevant user services
        vm_services, counterpart_services = self.get_services()
        services = UserServiceAssignListRequest()
        services.sip_user_id = self.sip_user_id
        services.services = vm_services

        command.append(services)

        # now stuff specific to voicemail type
        if self.type == 'broadsoft':
            command = command + self.build_activate_command__broadsoft()
        elif self.type == 'unity':
            command = command + self.build_activate_command__unity()
        else:
            raise NotImplementedError("no Voicemail.build_activate_command() behavior defined for type " + str(self.type))

        return command

    def build_activate_command__broadsoft(self):
        # UserVoiceMessagingUserModifyVoiceManagementRequest configures basic behavoir
        activate = UserVoiceMessagingUserModifyVoiceManagementRequest()
        activate.sip_user_id = self.sip_user_id
        activate.is_active = True
        activate.processing = 'Deliver To Email Address Only'
        activate.voice_message_delivery_email_address = self.email
        activate.use_phone_message_waiting_indicator = self.mwi
        activate.send_voice_message_notify_email = self.email
        activate.voice_message_notify_email_address = self.email
        activate.send_carbon_copy_voice_message = self.send_cc
        activate.voice_message_carbon_copy_email_address = self.cc_email
        activate.transfer_on_zero_to_phone_number = self.transfer_on_zero
        activate.transfer_phone_number = self.transfer_number
        activate.always_redirect_to_voice_mail = self.straight_to_voicemail
        activate.busy_redirect_to_voice_mail = self.busy_to_voicemail
        activate.no_answer_redirect_to_voice_mail = self.no_answer_to_voicemail
        activate.out_of_primary_zone_redirect_to_voice_mail = False

        # probably because it's a poorly planned tack-on service, surgemail (which provides their voicemail service)
        # has to be configured separately, even though some of the functionality is duplicated, via
        # UserVoiceMessagingUserModifyAdvancedVoiceManagementRequest
        surgemail = UserVoiceMessagingUserModifyAdvancedVoiceManagementRequest()
        surgemail.sip_user_id = self.sip_user_id
        surgemail.mail_server_selection = 'Group Mail Server'
        surgemail.group_mail_server_email_address = str(self.did) + '@' + self.surgemail_domain
        surgemail.group_mail_server_user_id = str(self.did) + '@' + self.surgemail_domain
        surgemail.group_mail_server_password = self.sip_password
        surgemail.use_group_default_mail_server_full_mailbox_limit = True

        return [activate, surgemail]

    def build_activate_command__unity(self):
        # configure the XML object that activates unity voicemail
        activate = UserThirdPartyVoiceMailSupportModifyRequest()
        activate.sip_user_id = self.sip_user_id
        activate.is_active = True
        activate.busy_redirect_to_voice_mail = self.busy_to_voicemail
        activate.no_answer_redirect_to_voice_mail = self.no_answer_to_voicemail
        activate.user_server = self.unity_number
        activate.mailbox_id_type = 'User Or Group Phone Number'
        activate.no_answer_number_of_rings = self.rings
        activate.always_redirect_to_voice_mail = self.straight_to_voicemail
        activate.out_of_primary_zone_redirect_to_voice_mail = False

        # returning a list to ease merging with other activate/deactivate possibilities
        return [activate]

    def build_deactivate_counterpart_command(self):
        command = []

        vm_services, counterpart_services = self.get_services()
        services = UserServiceUnassignListRequest()
        services.sip_user_id = self.sip_user_id
        services.services = counterpart_services
        command.append(services)

        # since we're removing the service from the user, these commands will be rejected...and should be then
        # unnecessary anyway
        """
        if self.type == 'unity':
            # if we're activating unity, deactivate broadsoft
            # returning a list to ease merging with other activate/deactivate possibilities
            command.append(
                UserVoiceMessagingUserModifyVoiceManagementRequest(sip_user_id=self.sip_user_id, is_active=False)
            )

        elif self.type == 'broadsoft':
            # if we're activating broadsoft, deactivate third party
            # returning a list to ease merging with other activate/deactivate possibilities
            command.append(
                UserThirdPartyVoiceMailSupportModifyRequest(sip_user_id=self.sip_user_id, is_active=False)
            )
        """

        if self.type != 'unity' and self.type != 'broadsoft':
            raise NotImplementedError(
                "no Voicemail.build_deactivate_counterpart_command() behavior defined for type " + str(self.type))

        return command

    # Only want to assign the relevant voicemail services. Furthermore, as a belt-and-suspenders move, want to unassign
    # services for other voicemail systems.
    def get_services(self):
        vm_services = {
            'broadsoft': [
                'Voice Messaging User',
                'Voice Messaging User - Video',
                'Voice Portal Calling'
            ],

            'unity': [
                'Third-Party MWI Control',
                'Third-Party Voice Mail Support'
            ]
        }

        services = []
        counterpart_services = []

        for this_type, this_services in vm_services.items():
            if this_type == self.type:
                services = services + this_services
            else:
                counterpart_services = counterpart_services + this_services

        return services, counterpart_services

    def validate(self):
        if not self.sip_user_id:
            raise ValueError("can't call Account.activate_unity_voicemail without a value for sip_user_id")

        if not self.email:
            raise ValueError("can't call Account.activate_unity_voicemail without a value for email")

        if not self.did:
            raise ValueError("can't call Account.activate_unity_voicemail without a value for did")
