import xml.etree.ElementTree as ET
from broadsoft.requestobjects.lib.BroadsoftRequest import BroadsoftRequest


class UserGetRequest(BroadsoftRequest):
    command_name = 'UserGetRequest21'

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
            raise ValueError("can't run UserGetRequest.build_command_xml() without a value for sip_user_id")

    @staticmethod
    def get_user(sip_user_id=None, **kwargs):
        u = UserGetRequest(sip_user_id=sip_user_id, **kwargs)
        xml = u.post()
        return xml

        # convert GroupTable to dict
        #if type(xml) is str:
        #    xml = ET.fromstring(xml)
        #group_table = xml.findall('./command/groupTable')[0]
        #return BroadsoftRequest.convert_results_table(xml=group_table)
