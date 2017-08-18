import xml.etree.ElementTree as ET
from broadsoft.requestobjects.lib.BroadsoftRequest import BroadsoftRequest


class UserSharedCallAppearanceGetRequest(BroadsoftRequest):
    command_name = 'UserSharedCallAppearanceGetRequest16sp2'
    skip_fetch_error = True
    skip_fetch_error_head = '[Error 4008] User not found: '

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
            raise ValueError("can't run UserSharedCallAppearanceGetRequest.build_command_xml() without a value for sip_user_id")

    @staticmethod
    def get_devices(sip_user_id=None, **kwargs):
        u = UserSharedCallAppearanceGetRequest(sip_user_id=sip_user_id, **kwargs)
        xml = u.post()
        return BroadsoftRequest.convert_results_table(xml=xml)
