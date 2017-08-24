import xml.etree.ElementTree as ET
from broadsoft.requestobjects.lib.BroadsoftRequest import BroadsoftRequest


class UserAuthenticationModifyRequest(BroadsoftRequest):
    command_name = 'UserAuthenticationModifyRequest'
    check_success = True

    def __init__(self, sip_user_id=None, did=None, new_password=None, **kwargs):
        self.did = did
        self.new_password = new_password
        self.sip_user_id = sip_user_id

        BroadsoftRequest.__init__(self, **kwargs)

    def build_command_xml(self):
        self.prep_for_xml()
        self.validate()

        cmd = self.build_command_shell()

        e = ET.SubElement(cmd, 'userId')
        e.text = self.sip_user_id

        e = ET.SubElement(cmd, 'userName')
        e.text = self.did

        e = ET.SubElement(cmd, 'newPassword')
        e.text = self.new_password

        return cmd

    def validate(self):
        import re
        if self.sip_user_id is None:
            raise ValueError("can't run broadsoft.UserAuthenticationModifyRequest.to_xml() without a value for sip_user_id.")

        if self.did is None or not re.match(r'^\d{10}$', str(self.did)):
            raise ValueError("the value for did you provided to UserAuthenticationModifyRequest is not valid")

        if self.new_password is None:
            raise ValueError("can't run broadsoft.UserAuthenticationModifyRequest.to_xml() without a value for password.")

    @staticmethod
    def set_credentials(new_password, did, sip_user_id, **kwargs):
        u = UserAuthenticationModifyRequest(sip_user_id=sip_user_id, did=did, new_password=new_password, **kwargs)
        u.post()
