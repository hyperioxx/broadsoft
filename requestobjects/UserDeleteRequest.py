import xml.etree.ElementTree as ET
from broadsoft.requestobjects.lib.BroadsoftRequest import BroadsoftRequest


class UserDeleteRequest(BroadsoftRequest):
    command_name = 'UserDeleteRequest'

    def __init__(self, sip_user_id=None, **kwargs):
        self.sip_user_id = sip_user_id

        BroadsoftRequest.__init__(self, **kwargs)

    def build_command_xml(self):
        self.prep_for_xml()
        self.validate()

        cmd = self.build_command_shell()

        e = ET.SubElement(cmd, 'userId')
        e.text = self.sip_user_id

        return cmd

    def validate(self):
        if not self.sip_user_id:
            raise ValueError("can't run UserDeleteRequest.build_command_xml() without a value for sip_user_id")

    @staticmethod
    def delete_user(sip_user_id=None, **kwargs):
        u = UserDeleteRequest(sip_user_id=sip_user_id, **kwargs)
        xml = u.post()
        return xml
