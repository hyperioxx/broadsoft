import xml.etree.ElementTree as ET
from broadsoft.requestobjects.lib.BroadsoftRequest import BroadsoftRequest


class GroupAccessDeviceDeleteRequest(BroadsoftRequest):
    command_name = 'GroupAccessDeviceDeleteRequest'

    def __init__(self, device_name=None, **kwargs):
        self.device_name = device_name

        BroadsoftRequest.__init__(self, **kwargs)

    def build_command_xml(self):
        self.prep_for_xml()
        self.validate()

        cmd = self.build_command_shell()

        e = ET.SubElement(cmd, 'serviceProviderId')
        e.text = self.service_provider

        e = ET.SubElement(cmd, 'groupId')
        e.text = self.group_id

        e = ET.SubElement(cmd, 'deviceName')
        e.text = self.device_name

        return cmd

    def validate(self):
        if not self.device_name:
            raise ValueError("can't run GroupAccessDeviceDeleteRequest.delete() without a value for device_name")

    @staticmethod
    def delete_device(device_name=None, **kwargs):
        u = GroupAccessDeviceDeleteRequest(device_name=device_name, **kwargs)
        xml = u.post()
        return xml
