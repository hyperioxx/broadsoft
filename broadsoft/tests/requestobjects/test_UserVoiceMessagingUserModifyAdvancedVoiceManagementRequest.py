import unittest.mock
import xml.etree.ElementTree as ET
from broadsoft.requestobjects.UserVoiceMessagingUserModifyAdvancedVoiceManagementRequest import UserVoiceMessagingUserModifyAdvancedVoiceManagementRequest


class TestUserVoiceMessagingUserModifyAdvancedVoiceManagementRequest(unittest.TestCase):
    def test_validate(self):
        u = UserVoiceMessagingUserModifyAdvancedVoiceManagementRequest()
        with self.assertRaises(ValueError):
            u.validate()

    @unittest.mock.patch.object(UserVoiceMessagingUserModifyAdvancedVoiceManagementRequest, 'validate')
    def test_build_command_xml_invokes_validate(
            self,
            validate_patch
    ):
        u = UserVoiceMessagingUserModifyAdvancedVoiceManagementRequest(sip_user_id='6175551212@broadsoft-dev.mit.edu')
        u.build_command_xml()
        self.assertTrue(validate_patch.called)

    def test_build_command_xml_call(self):
        self.maxDiff = None
        u = UserVoiceMessagingUserModifyAdvancedVoiceManagementRequest(sip_user_id='6175551212@broadsoft-dev.mit.edu',
                                                                       mail_server_selection='mss',
                                                                       group_mail_server_email_address='gmsea',
                                                                       group_mail_server_user_id='gmsui',
                                                                       group_mail_server_password='gmso',
                                                                       use_group_default_mail_server_full_mailbox_limit=False,
                                                                       group_mail_server_full_mailbox_limit=10,
                                                                       personal_mail_server_net_address='pmsna',
                                                                       personal_mail_server_protocol='pmsp',
                                                                       personal_mail_server_real_delete_for_imap='pmsrdfi',
                                                                       personal_mail_server_email_address='pmsea',
                                                                       personal_mail_server_user_id='pmsui',
                                                                       personal_mail_server_password='pmsp'
                                                                       )
        target_xml = \
            '<command xmlns="" xsi:type="UserVoiceMessagingUserModifyAdvancedVoiceManagementRequest"><userId>6175551212@broadsoft-dev.mit.edu</userId><mailServerSelection>mss</mailServerSelection><groupMailServerEmailAddress>gmsea</groupMailServerEmailAddress><groupMailServerUserId>gmsui</groupMailServerUserId><groupMailServerPassword>gmso</groupMailServerPassword><useGroupDefaultMailServerFullMailboxLimit>false</useGroupDefaultMailServerFullMailboxLimit><groupMailServerFullMailboxLimit>10</groupMailServerFullMailboxLimit><personalMailServerNetAddress>pmsna</personalMailServerNetAddress><personalMailServerProtocol>pmsp</personalMailServerProtocol><personalMailServerRealDeleteForImap>pmsrdfi</personalMailServerRealDeleteForImap><personalMailServerEmailAddress>pmsea</personalMailServerEmailAddress><personalMailServerUserId>pmsui</personalMailServerUserId><personalMailServerPassword>pmsp</personalMailServerPassword></command>'

        xml = u.to_xml()
        cmd = xml.findall('./command')[0]

        self.assertEqual(
            target_xml,
            ET.tostring(cmd).decode('utf-8')
        )
