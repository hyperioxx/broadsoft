import xml.etree.ElementTree as ET
from broadsoft.requestobjects.lib.BroadsoftRequest import BroadsoftRequest


class GroupAccessDeviceGetRequest(BroadsoftRequest):
    command_name = 'GroupAccessDeviceGetRequest18sp1'

    def __init__(self, name=None, **kwargs):
        self.name = name

        BroadsoftRequest.__init__(self, **kwargs)

    def build_command_xml(self):
        self.prep_for_xml()
        self.validate()

        cmd = self.build_command_shell()

        e = ET.SubElement(cmd, 'serviceProviderId')
        e.text = self.broadsoftinstance.service_provider

        e = ET.SubElement(cmd, 'groupId')
        e.text = self.group_id

        e = ET.SubElement(cmd, 'deviceName')
        e.text = self.name

        return cmd

    def validate(self):
        if not self.name:
            raise ValueError("can't run GroupAccessDeviceGetRequest.build_command_xml() without a value for name")

    @staticmethod
    def get_device(name, **kwargs):
        g = GroupAccessDeviceGetRequest(name=name, **kwargs)
        xml = g.post()
        return xml
