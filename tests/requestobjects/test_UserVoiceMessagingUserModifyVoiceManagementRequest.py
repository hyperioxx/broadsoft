import unittest.mock
import xml.etree.ElementTree as ET
from broadsoft.requestobjects.UserVoiceMessagingUserModifyVoiceManagementRequest import UserVoiceMessagingUserModifyVoiceManagementRequest


class TestUserVoiceMessagingUserModifyVoiceManagementRequest(unittest.TestCase):
    def test_validate(self):
        u = UserVoiceMessagingUserModifyVoiceManagementRequest()
        with self.assertRaises(ValueError):
            u.validate()

    @unittest.mock.patch.object(UserVoiceMessagingUserModifyVoiceManagementRequest, 'validate')
    def test_build_command_xml_invokes_validate(
            self,
            validate_patch
    ):
        u = UserVoiceMessagingUserModifyVoiceManagementRequest(sip_user_id='6175551212@broadsoft-dev.mit.edu')
        u.build_command_xml()
        self.assertTrue(validate_patch.called)

    def test_build_command_xml_call(self):
        self.maxDiff = None
        u = UserVoiceMessagingUserModifyVoiceManagementRequest(sip_user_id='6175551212@broadsoft-dev.mit.edu',
                                                  is_active=True, processing='Deliver To Email Address Only',
                                                               voice_message_delivery_email_address='beaver1@mit.edu',
                 use_phone_message_waiting_indicator=False, send_voice_message_notify_email=True,
                 voice_message_notify_email_address='beaver2@mit.edu', send_carbon_copy_voice_message=False,
                 voice_message_carbon_copy_email_address='beaver3@mit.edu', transfer_on_zero_to_phone_number=True,
                 transfer_phone_number='617-555-2121', always_redirect_to_voice_mail=False,
                                                               busy_redirect_to_voice_mail=True,
                 no_answer_redirect_to_voice_mail=False, out_of_primary_zone_redirect_to_voice_mail=True)
        target_xml = \
            '<command xmlns="" xsi:type="UserVoiceMessagingUserModifyVoiceManagementRequest">' + \
            '<userId>6175551212@broadsoft-dev.mit.edu</userId>' + \
            '<isActive>true</isActive>' + \
            '<processing>Deliver To Email Address Only</processing>' + \
            '<voiceMessageDeliveryEmailAddress>beaver1@mit.edu</voiceMessageDeliveryEmailAddress>' + \
            '<usePhoneMessageWaitingIndicator>false</usePhoneMessageWaitingIndicator>' + \
            '<sendVoiceMessageNotifyEmail>true</sendVoiceMessageNotifyEmail>' + \
            '<voiceMessageNotifyEmailAddress>beaver2@mit.edu</voiceMessageNotifyEmailAddress>' + \
            '<sendCarbonCopyVoiceMessage>false</sendCarbonCopyVoiceMessage>' + \
            '<voiceMessageCarbonCopyEmailAddress>beaver3@mit.edu</voiceMessageCarbonCopyEmailAddress>' + \
            '<transferOnZeroToPhoneNumber>true</transferOnZeroToPhoneNumber>' + \
            '<transferPhoneNumber>6175552121</transferPhoneNumber>' + \
            '<alwaysRedirectToVoiceMail>false</alwaysRedirectToVoiceMail>' + \
            '<busyRedirectToVoiceMail>true</busyRedirectToVoiceMail>' + \
            '<noAnswerRedirectToVoiceMail>false</noAnswerRedirectToVoiceMail>' + \
            '<outOfPrimaryZoneRedirectToVoiceMail>true</outOfPrimaryZoneRedirectToVoiceMail>' + \
            '</command>'

        xml = u.to_xml()
        cmd = xml.findall('./command')[0]
        self.assertEqual(
            target_xml,
            ET.tostring(cmd).decode('utf-8')
        )

        # flop booleans to help ensure no mixups
        u = UserVoiceMessagingUserModifyVoiceManagementRequest(sip_user_id='6175551212@broadsoft-dev.mit.edu',
                                                               is_active=False,
                                                               processing='Deliver To Email Address Only',
                                                               voice_message_delivery_email_address='beaver1@mit.edu',
                                                               use_phone_message_waiting_indicator=True,
                                                               send_voice_message_notify_email=False,
                                                               voice_message_notify_email_address='beaver2@mit.edu',
                                                               send_carbon_copy_voice_message=True,
                                                               voice_message_carbon_copy_email_address='beaver3@mit.edu',
                                                               transfer_on_zero_to_phone_number=False,
                                                               transfer_phone_number='617-555-2121',
                                                               always_redirect_to_voice_mail=True,
                                                               busy_redirect_to_voice_mail=False,
                                                               no_answer_redirect_to_voice_mail=True,
                                                               out_of_primary_zone_redirect_to_voice_mail=False)
        target_xml = \
            '<command xmlns="" xsi:type="UserVoiceMessagingUserModifyVoiceManagementRequest">' + \
            '<userId>6175551212@broadsoft-dev.mit.edu</userId>' + \
            '<isActive>false</isActive>' + \
            '<processing>Deliver To Email Address Only</processing>' + \
            '<voiceMessageDeliveryEmailAddress>beaver1@mit.edu</voiceMessageDeliveryEmailAddress>' + \
            '<usePhoneMessageWaitingIndicator>true</usePhoneMessageWaitingIndicator>' + \
            '<sendVoiceMessageNotifyEmail>false</sendVoiceMessageNotifyEmail>' + \
            '<voiceMessageNotifyEmailAddress>beaver2@mit.edu</voiceMessageNotifyEmailAddress>' + \
            '<sendCarbonCopyVoiceMessage>true</sendCarbonCopyVoiceMessage>' + \
            '<voiceMessageCarbonCopyEmailAddress>beaver3@mit.edu</voiceMessageCarbonCopyEmailAddress>' + \
            '<transferOnZeroToPhoneNumber>false</transferOnZeroToPhoneNumber>' + \
            '<transferPhoneNumber>6175552121</transferPhoneNumber>' + \
            '<alwaysRedirectToVoiceMail>true</alwaysRedirectToVoiceMail>' + \
            '<busyRedirectToVoiceMail>false</busyRedirectToVoiceMail>' + \
            '<noAnswerRedirectToVoiceMail>true</noAnswerRedirectToVoiceMail>' + \
            '<outOfPrimaryZoneRedirectToVoiceMail>false</outOfPrimaryZoneRedirectToVoiceMail>' + \
            '</command>'

        xml = u.to_xml()
        cmd = xml.findall('./command')[0]
        self.assertEqual(
            target_xml,
            ET.tostring(cmd).decode('utf-8')
        )
