import unittest.mock
import xml.etree.ElementTree as ET
from broadsoft.requestobjects.UserThirdPartyVoiceMailSupportModifyRequest import UserThirdPartyVoiceMailSupportModifyRequest


class TestUserThirdPartyVoiceMailSupportModifyRequest(unittest.TestCase):
    def test_validate(self):
        u = UserThirdPartyVoiceMailSupportModifyRequest()
        with self.assertRaises(ValueError):
            u.validate()

    @unittest.mock.patch.object(UserThirdPartyVoiceMailSupportModifyRequest, 'validate')
    def test_build_command_xml_calls_validate(
            self,
            validate_patch
    ):
        u = UserThirdPartyVoiceMailSupportModifyRequest(sip_user_id='6175551212@broadsoft-dev.mit.edu')
        u.build_command_xml()
        self.assertTrue(validate_patch.called)

    def test_build_command_xml(self):
        self.maxDiff = None
        u = UserThirdPartyVoiceMailSupportModifyRequest(sip_user_id='6175551212@broadsoft-dev.mit.edu',
                                                  is_active=True, busy_redirect_to_voice_mail=False,
                                                  no_answer_redirect_to_voice_mail=True,
                                                  server_selection='User Specific Mail Server',
                                                  user_server='617-253-0000',
                                                  mailbox_id_type='User Or Group Phone Number',
                                                  no_answer_number_of_rings=3, always_redirect_to_voice_mail=False,
                                                  out_of_primary_zone_redirect_to_voice_mail=True)
        target_xml = \
            '<command xmlns="" xsi:type="UserThirdPartyVoiceMailSupportModifyRequest">' + \
            '<userId>6175551212@broadsoft-dev.mit.edu</userId>' + \
            '<isActive>true</isActive>' + \
            '<busyRedirectToVoiceMail>false</busyRedirectToVoiceMail>' + \
            '<noAnswerRedirectToVoiceMail>true</noAnswerRedirectToVoiceMail>' + \
            '<serverSelection>User Specific Mail Server</serverSelection>' + \
            '<userServer>6172530000</userServer>' + \
            '<mailboxIdType>User Or Group Phone Number</mailboxIdType>' + \
            '<noAnswerNumberOfRings>3</noAnswerNumberOfRings>' +\
            '<alwaysRedirectToVoiceMail>false</alwaysRedirectToVoiceMail>' + \
            '<outOfPrimaryZoneRedirectToVoiceMail>true</outOfPrimaryZoneRedirectToVoiceMail>' + \
            '</command>'

        xml = u.to_xml()
        cmd = xml.findall('./command')[0]
        self.assertEqual(
            target_xml,
            ET.tostring(cmd).decode('utf-8')
        )

        # change the results to ensure no mix ups
        u = UserThirdPartyVoiceMailSupportModifyRequest(sip_user_id='6175551213@broadsoft-dev.mit.edu',
                                                        is_active=False, busy_redirect_to_voice_mail=True,
                                                        no_answer_redirect_to_voice_mail=False,
                                                        server_selection='garbanzo',
                                                        user_server='617-253-0001',
                                                        mailbox_id_type='ham',
                                                        no_answer_number_of_rings=4,
                                                        always_redirect_to_voice_mail=True,
                                                        out_of_primary_zone_redirect_to_voice_mail=False)
        target_xml = \
            '<command xmlns="" xsi:type="UserThirdPartyVoiceMailSupportModifyRequest">' + \
            '<userId>6175551213@broadsoft-dev.mit.edu</userId>' + \
            '<isActive>false</isActive>' + \
            '<busyRedirectToVoiceMail>true</busyRedirectToVoiceMail>' + \
            '<noAnswerRedirectToVoiceMail>false</noAnswerRedirectToVoiceMail>' + \
            '<serverSelection>garbanzo</serverSelection>' + \
            '<userServer>6172530001</userServer>' + \
            '<mailboxIdType>ham</mailboxIdType>' + \
            '<noAnswerNumberOfRings>4</noAnswerNumberOfRings>' + \
            '<alwaysRedirectToVoiceMail>true</alwaysRedirectToVoiceMail>' + \
            '<outOfPrimaryZoneRedirectToVoiceMail>false</outOfPrimaryZoneRedirectToVoiceMail>' + \
            '</command>'

        xml = u.to_xml()
        cmd = xml.findall('./command')[0]
        self.assertEqual(
            target_xml,
            ET.tostring(cmd).decode('utf-8')
        )
