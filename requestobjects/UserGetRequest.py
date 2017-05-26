import xml.etree.ElementTree as ET
from broadsoft.requestobjects.lib.BroadsoftRequest import BroadsoftRequest


class UserGetRequest(BroadsoftRequest):
    command_name = 'UserGetRequest21'

    def __init__(self, did=None, sip_user_id=None, **kwargs):
        self.did = did
        if self.did:
            self.did = BroadsoftRequest.convert_phone_number(number=self.did)
        self.sip_user_id = sip_user_id

        BroadsoftRequest.__init__(self, **kwargs)
        if not self.sip_user_id:
            self.sip_user_id = self.derive_sip_user_id()

    def build_command_xml(self):
        if self.did:
            self.did = BroadsoftRequest.convert_phone_number(number=self.did)
        if not self.sip_user_id:
            self.sip_user_id = self.derive_sip_user_id()
        self.validate()

        cmd = self.build_command_shell()

        e = ET.SubElement(cmd, 'userId')
        e.text = self.sip_user_id

        return cmd

    def validate(self):
        if not self.sip_user_id:
            raise ValueError("can't run UserGetRequest.build_command_xml() without a value for sip_user_id")

    @staticmethod
    def get_user(**kwargs):
        u = UserGetRequest(**kwargs)
        xml = u.post()

        # convert GroupTable to dict
        #if type(xml) is str:
        #    xml = ET.fromstring(xml)
        #group_table = xml.findall('./command/groupTable')[0]
        #return BroadsoftRequest.convert_results_table(xml=group_table)
