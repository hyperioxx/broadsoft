import xml.etree.ElementTree as ET
from broadsoft.requestobjects.lib.BroadsoftRequest import BroadsoftRequest
from broadsoft.requestobjects.datatypes.AccessDeviceEndpoint import AccessDeviceEndpoint


class UserSharedCallAppearanceDeleteEndpointListRequest(BroadsoftRequest):
    command_name = 'UserSharedCallAppearanceDeleteEndpointListRequest14'
    skip_fetch_error = True
    skip_fetch_error_head = '[Error 4008] User not found: '

    def __init__(self, sip_user_id=None, devices=None, **kwargs):
        self.sip_user_id = sip_user_id
        self.devices = devices

        BroadsoftRequest.__init__(self, **kwargs)

    def build_command_xml(self):
        self.prep_for_xml()
        self.validate()

        cmd = self.build_command_shell()

        e = ET.SubElement(cmd, 'userId')
        e.text = self.sip_user_id

        for d in self.devices:
            ade_xml = AccessDeviceEndpoint(device_name=d['name'], line_port=d['line_port']).to_xml()
            cmd.append(ade_xml)

        return cmd

    def validate(self):
        if not self.devices or len(self.devices) == 0:
            raise ValueError(
                "can't run UserSharedCallAppearanceDeleteEndpointListRequest.build_command_xml() without a list of devices, which should be dicts with a device name and a line port")

        if not self.sip_user_id:
            raise ValueError("can't run UserSharedCallAppearanceDeleteEndpointListRequest.build_command_xml() without a value for sip_user_id")

    @staticmethod
    def delete_devices(sip_user_id=None, **kwargs):
        u = UserSharedCallAppearanceDeleteEndpointListRequest(sip_user_id=sip_user_id, **kwargs)
        xml = u.post()
        return xml
