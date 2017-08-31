import xml.etree.ElementTree as ET
from broadsoft.requestobjects.lib.BroadsoftRequest import BroadsoftRequest


class UserVoiceMessagingUserModifyAdvancedVoiceManagementRequest(BroadsoftRequest):
    command_name = 'UserVoiceMessagingUserModifyAdvancedVoiceManagementRequest'
    check_success = True

    booleans = [
        'use_group_default_mail_server_full_mailbox_limit'
    ]

    def __init__(self, sip_user_id=None, mail_server_selection=None, group_mail_server_email_address=None,
                 group_mail_server_user_id=None, group_mail_server_password=None,
                 use_group_default_mail_server_full_mailbox_limit=True,
                 group_mail_server_full_mailbox_limit=None,
                 personal_mail_server_net_address=None,
                 personal_mail_server_protocol=None,
                 personal_mail_server_real_delete_for_imap=None, personal_mail_server_email_address=None,
                 personal_mail_server_user_id=None, personal_mail_server_password=None,
                 **kwargs):
        self.sip_user_id = sip_user_id
        self.mail_server_selection = mail_server_selection
        self.group_mail_server_email_address = group_mail_server_email_address
        self.group_mail_server_user_id = group_mail_server_user_id
        self.group_mail_server_password = group_mail_server_password
        self.use_group_default_mail_server_full_mailbox_limit = use_group_default_mail_server_full_mailbox_limit
        self.group_mail_server_full_mailbox_limit = group_mail_server_full_mailbox_limit
        self.personal_mail_server_net_address = personal_mail_server_net_address
        self.personal_mail_server_protocol = personal_mail_server_protocol
        self.personal_mail_server_real_delete_for_imap = personal_mail_server_real_delete_for_imap
        self.personal_mail_server_email_address = personal_mail_server_email_address
        self.personal_mail_server_user_id = personal_mail_server_user_id
        self.personal_mail_server_password = personal_mail_server_password
        BroadsoftRequest.__init__(self, **kwargs)

    def build_command_xml(self):
        self.prep_for_xml()
        self.validate()

        cmd = self.build_command_shell()

        uid = ET.SubElement(cmd, 'userId')
        uid.text = self.sip_user_id

        if self.mail_server_selection is not None:
            s = ET.SubElement(cmd, 'self.mail_server_selection')
            s.text = self.mail_server_selection

        if self.group_mail_server_email_address is not None:
            s = ET.SubElement(cmd, 'self.group_mail_server_email_address')
            s.text = self.group_mail_server_email_address

        if self.group_mail_server_user_id is not None:
            s = ET.SubElement(cmd, 'self.group_mail_server_user_id')
            s.text = self.group_mail_server_user_id

        if self.group_mail_server_password is not None:
            s = ET.SubElement(cmd, 'self.group_mail_server_password')
            s.text = self.group_mail_server_password

        if self.use_group_default_mail_server_full_mailbox_limit is not None:
            s = ET.SubElement(cmd, 'self.use_group_default_mail_server_full_mailbox_limit')
            s.text = self.use_group_default_mail_server_full_mailbox_limit

        if self.group_mail_server_full_mailbox_limit is not None:
            s = ET.SubElement(cmd, 'self.group_mail_server_full_mailbox_limit')
            s.text = str(self.group_mail_server_full_mailbox_limit)

        if self.personal_mail_server_net_address is not None:
            s = ET.SubElement(cmd, 'self.personal_mail_server_net_address')
            s.text = self.personal_mail_server_net_address

        if self.personal_mail_server_protocol is not None:
            s = ET.SubElement(cmd, 'self.personal_mail_server_protocol')
            s.text = self.personal_mail_server_protocol

        if self.personal_mail_server_real_delete_for_imap is not None:
            s = ET.SubElement(cmd, 'self.personal_mail_server_real_delete_for_imap')
            s.text = self.personal_mail_server_real_delete_for_imap

        if self.personal_mail_server_email_address is not None:
            s = ET.SubElement(cmd, 'self.personal_mail_server_email_address')
            s.text = self.personal_mail_server_email_address

        if self.personal_mail_server_user_id is not None:
            s = ET.SubElement(cmd, 'self.personal_mail_server_user_id')
            s.text = self.personal_mail_server_user_id

        if self.personal_mail_server_password is not None:
            s = ET.SubElement(cmd, 'self.personal_mail_server_password')
            s.text = self.personal_mail_server_password

        return cmd

    def validate(self):
        if self.sip_user_id is None:
            raise ValueError("can't run broadsoft.UserSharedCallAppearanceModifyRequest.to_xml() without a value for sip_user_id.")
