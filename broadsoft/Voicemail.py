from broadsoft.lib.BroadsoftObject import BroadsoftObject
from broadsoft.requestobjects.UserVoiceMessagingUserModifyVoiceManagementRequest import UserVoiceMessagingUserModifyVoiceManagementRequest
from broadsoft.requestobjects.UserThirdPartyVoiceMailSupportModifyRequest import UserThirdPartyVoiceMailSupportModifyRequest
from broadsoft.requestobjects.UserVoiceMessagingUserModifyAdvancedVoiceManagementRequest import UserVoiceMessagingUserModifyAdvancedVoiceManagementRequest
from broadsoft.requestobjects.lib.BroadsoftRequest import BroadsoftRequest


class Voicemail(BroadsoftObject):
    unity_number = 6172530000

    def __init__(self, behavior='email', busy_to_voicemail=True, cc_email=None, did=None, email=None, mwi=None,
                 no_answer_to_voicemail=True, rings=3, straight_to_voicemail=False, send_cc=False, sip_user_id=None,
                 type='broadsoft', transfer_on_zero=False, transfer_number=None, sip_password=None,
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
        self.transfer_on_zero = transfer_on_zero
        self.transfer_number = transfer_number
        self.type = type                                    # broadsoft or unity

        BroadsoftObject.__init__(self, **kwargs)

    def build_activate_command(self):
        self.validate()

        if self.type == 'broadsoft':
            return self.build_activate_command__broadsoft()
        elif self.type == 'unity':
            return self.build_activate_command__unity()
        else:
            raise NotImplementedError("no Voicemail.build_activate_command() behavior defined for type " + str(self.type))

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
        surgemail.group_mail_server_email_address = self.email
        surgemail.group_mail_server_user_id = self.did
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
        if self.type == 'unity':
            # if we're activating unity, deactivate broadsoft
            # returning a list to ease merging with other activate/deactivate possibilities
            return [UserVoiceMessagingUserModifyVoiceManagementRequest(sip_user_id=self.sip_user_id, is_active=False)]

        elif self.type == 'broadsoft':
            # if we're activating broadsoft, deactivate third party
            # returning a list to ease merging with other activate/deactivate possibilities
            return [UserThirdPartyVoiceMailSupportModifyRequest(sip_user_id=self.sip_user_id, is_active=False)]

        else:
            raise NotImplementedError("no Voicemail.build_deactivate_counterpart_command() behavior defined for type " + str(self.type))

    def validate(self):
        if not self.sip_user_id:
            raise ValueError("can't call Account.activate_unity_voicemail without a value for sip_user_id")

        if not self.email:
            raise ValueError("can't call Account.activate_unity_voicemail without a value for email")
