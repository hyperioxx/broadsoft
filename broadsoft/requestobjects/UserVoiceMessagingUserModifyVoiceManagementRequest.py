import xml.etree.ElementTree as ET
from broadsoft.requestobjects.lib.BroadsoftRequest import BroadsoftRequest


class UserVoiceMessagingUserModifyVoiceManagementRequest(BroadsoftRequest):
    command_name = 'UserVoiceMessagingUserModifyVoiceManagementRequest'
    check_success = True

    booleans = [
        'is_active',
        'use_phone_message_waiting_indicator',
        'send_voice_message_notify_email',
        'send_carbon_copy_voice_message',
        'transfer_on_zero_to_phone_number',
        'always_redirect_to_voice_mail',
        'busy_redirect_to_voice_mail',
        'no_answer_redirect_to_voice_mail',
        'out_of_primary_zone_redirect_to_voice_mail'
    ]

    def __init__(self, sip_user_id=None, is_active=None, processing=None, voice_message_delivery_email_address=None,
                 use_phone_message_waiting_indicator=None, send_voice_message_notify_email=None,
                 voice_message_notify_email_address=None, send_carbon_copy_voice_message=None,
                 voice_message_carbon_copy_email_address=None, transfer_on_zero_to_phone_number=None,
                 transfer_phone_number=None, always_redirect_to_voice_mail=None, busy_redirect_to_voice_mail=None,
                 no_answer_redirect_to_voice_mail=None, out_of_primary_zone_redirect_to_voice_mail=None,
                 **kwargs):
        self.sip_user_id = sip_user_id
        self.is_active = is_active
        self.processing = processing
        self.voice_message_delivery_email_address = voice_message_delivery_email_address
        self.use_phone_message_waiting_indicator = use_phone_message_waiting_indicator
        self.send_voice_message_notify_email = send_voice_message_notify_email
        self.voice_message_notify_email_address = voice_message_notify_email_address
        self.send_carbon_copy_voice_message = send_carbon_copy_voice_message
        self.voice_message_carbon_copy_email_address = voice_message_carbon_copy_email_address
        self.transfer_on_zero_to_phone_number = transfer_on_zero_to_phone_number
        self.transfer_phone_number = transfer_phone_number
        self.always_redirect_to_voice_mail = always_redirect_to_voice_mail
        self.busy_redirect_to_voice_mail = busy_redirect_to_voice_mail
        self.no_answer_redirect_to_voice_mail = no_answer_redirect_to_voice_mail
        self.out_of_primary_zone_redirect_to_voice_mail = out_of_primary_zone_redirect_to_voice_mail
        BroadsoftRequest.__init__(self, **kwargs)

    def build_command_xml(self):
        if self.transfer_phone_number is not None:
            self.transfer_phone_number = BroadsoftRequest.convert_phone_number(number=self.transfer_phone_number)
        self.prep_for_xml()
        self.validate()

        cmd = self.build_command_shell()

        uid = ET.SubElement(cmd, 'userId')
        uid.text = self.sip_user_id

        if self.is_active is not None:
            s = ET.SubElement(cmd, 'isActive')
            s.text = self.is_active

        if self.processing is not None:
            s = ET.SubElement(cmd, 'processing')
            s.text = self.processing

        if self.voice_message_delivery_email_address is not None:
            s = ET.SubElement(cmd, 'voiceMessageDeliveryEmailAddress')
            s.text = self.voice_message_delivery_email_address

        if self.use_phone_message_waiting_indicator is not None:
            s = ET.SubElement(cmd, 'usePhoneMessageWaitingIndicator')
            s.text = self.use_phone_message_waiting_indicator

        if self.send_voice_message_notify_email is not None:
            s = ET.SubElement(cmd, 'sendVoiceMessageNotifyEmail')
            s.text = self.send_voice_message_notify_email

        if self.voice_message_notify_email_address is not None:
            s = ET.SubElement(cmd, 'voiceMessageNotifyEmailAddress')
            s.text = self.voice_message_notify_email_address

        if self.send_carbon_copy_voice_message is not None:
            s = ET.SubElement(cmd, 'sendCarbonCopyVoiceMessage')
            s.text = self.send_carbon_copy_voice_message

        if self.voice_message_carbon_copy_email_address is not None:
            s = ET.SubElement(cmd, 'voiceMessageCarbonCopyEmailAddress')
            s.text = self.voice_message_carbon_copy_email_address

        if self.transfer_on_zero_to_phone_number is not None:
            s = ET.SubElement(cmd, 'transferOnZeroToPhoneNumber')
            s.text = self.transfer_on_zero_to_phone_number

        if self.transfer_phone_number is not None:
            s = ET.SubElement(cmd, 'transferPhoneNumber')
            s.text = self.transfer_phone_number

        if self.always_redirect_to_voice_mail is not None:
            s = ET.SubElement(cmd, 'alwaysRedirectToVoiceMail')
            s.text = self.always_redirect_to_voice_mail

        if self.busy_redirect_to_voice_mail is not None:
            s = ET.SubElement(cmd, 'busyRedirectToVoiceMail')
            s.text = self.busy_redirect_to_voice_mail

        if self.no_answer_redirect_to_voice_mail is not None:
            s = ET.SubElement(cmd, 'noAnswerRedirectToVoiceMail')
            s.text = self.no_answer_redirect_to_voice_mail

        if self.out_of_primary_zone_redirect_to_voice_mail is not None:
            s = ET.SubElement(cmd, 'outOfPrimaryZoneRedirectToVoiceMail')
            s.text = self.out_of_primary_zone_redirect_to_voice_mail

        return cmd

    def validate(self):
        if self.sip_user_id is None:
            raise ValueError("can't run broadsoft.UserSharedCallAppearanceModifyRequest.to_xml() without a value for sip_user_id.")

    @staticmethod
    def activate_broadsoft_voicemail(sip_user_id, processing='Deliver To Email Address Only',
                                     voice_message_delivery_email_address=None,
                                     use_phone_message_waiting_indicator=False,
                                     send_voice_message_notify_email=True,
                                     voice_message_notify_email_address=None,
                                     send_carbon_copy_voice_message=False,
                                     voice_message_carbon_copy_email_address=None,
                                     transfer_on_zero_to_phone_number=False, transfer_phone_number=None,
                                     always_redirect_to_voice_mail=False, busy_redirect_to_voice_mail=True,
                                     no_answer_redirect_to_voice_mail=True,
                                     out_of_primary_zone_redirect_to_voice_mail=False,
                                     **kwargs):
        u = UserVoiceMessagingUserModifyVoiceManagementRequest(sip_user_id=sip_user_id, is_active=True,
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
                                                               out_of_primary_zone_redirect_to_voice_mail=out_of_primary_zone_redirect_to_voice_mail,
                                                               **kwargs)
        u.post()

    @staticmethod
    def deactivate_broadsoft_voicemail(sip_user_id, **kwargs):
        u = UserVoiceMessagingUserModifyVoiceManagementRequest(sip_user_id=sip_user_id, is_active=False, **kwargs)
        u.post()