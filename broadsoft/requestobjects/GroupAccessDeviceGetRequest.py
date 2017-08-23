import xml.etree.ElementTree as ET
from broadsoft.requestobjects.lib.BroadsoftRequest import BroadsoftRequest

"""
This is for getting Device/Identity Profiles...we actually don't want to do that; we are planning on using a single
master generic profile for all our phones. Don't expect to use this, but leaving in case we do need it.

We only expect to link the Generic device profile as a primary/SCA, which will be handled via either UserModifyRequest
and UserSharedCallAppearanceAddEndpointRequest.
"""


class GroupAccessDeviceGetRequest(BroadsoftRequest):
    command_name = 'GroupAccessDeviceGetRequest18sp1'
    skip_fetch_error = True
    skip_fetch_error_head = '[Error 4505] Access Device not found: '

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
