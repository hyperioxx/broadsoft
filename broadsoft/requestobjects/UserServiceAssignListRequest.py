import xml.etree.ElementTree as ET
from broadsoft.requestobjects.lib.BroadsoftRequest import BroadsoftRequest


class UserServiceAssignListRequest(BroadsoftRequest):
    command_name = 'UserServiceAssignListRequest'
    check_success = True

    def __init__(self, sip_user_id=None, services=None, service_pack=None, **kwargs):
        self.service_pack = service_pack
        self.services = []
        if services:
            if type(services) is str():
                services = [services]
            for s in services:
                self.services.append(s)
        self.sip_user_id = sip_user_id

        BroadsoftRequest.__init__(self, **kwargs)

    def build_command_xml(self):
        self.prep_for_xml()
        self.validate()

        cmd = self.build_command_shell()

        uid = ET.SubElement(cmd, 'userId')
        uid.text = self.sip_user_id

        if self.service_pack is not None:
            sp = ET.SubElement(cmd, 'servicePackName')
            sp.text = self.service_pack

        if self.services is not None:
            for s in self.services:
                sn = ET.SubElement(cmd, 'serviceName')
                sn.text = s

        return cmd

    def validate(self):
        if self.sip_user_id is None:
            raise ValueError("can't run broadsoft.UserServiceAssignListRequest.to_xml() without a value for sip_user_id.")

        services_assigned = False
        if self.services and type(self.services) is list and len(self.services) > 0:
            services_assigned = True
        if self.service_pack is not None:
            services_assigned = True

        if not services_assigned:
            raise ValueError(
                "can't run broadsoft.UserServiceAssignListRequest.to_xml() without a list of services or a service_pack to add.")
