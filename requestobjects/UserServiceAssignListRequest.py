import xml.etree.ElementTree as ET
from broadsoft.requestobjects.lib.BroadsoftRequest import BroadsoftRequest


class UserServiceAssignListRequest(BroadsoftRequest):
    command_name = 'UserServiceAssignListRequest'
    check_success = True

    def __init__(self, sip_user_id=None, did=None, services=None, **kwargs):
        self.did = did
        self.services = []
        if services:
            if type(services) is str():
                services = [services]
            for s in services:
                self.services.append(s)
        self.sip_user_id = sip_user_id

        BroadsoftRequest.__init__(self, **kwargs)
        if self.did and self.sip_user_id is None:
            self.sip_user_id = self.derive_sip_user_id()

    def build_command_xml(self):
        if self.did and not self.sip_user_id:
            self.sip_user_id = self.derive_sip_user_id()
        self.validate()

        cmd = self.build_command_shell()

        uid = ET.SubElement(cmd, 'userId')
        uid.text = self.sip_user_id

        for s in self.services:
            sn = ET.SubElement(cmd, 'serviceName')
            sn.text = s

        return cmd

    def validate(self):
        if self.sip_user_id is None:
            raise ValueError("can't run broadsoft.UserServiceAssignListRequest.to_xml() without a value for sip_user_id.")

        if not self.services or type(self.services) is not list or len(self.services) == 0:
            raise ValueError(
                "can't run broadsoft.UserServiceAssignListRequest.to_xml() without a list() of services to add.")