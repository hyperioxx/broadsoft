from broadsoft.requestobjects.GroupAccessDeviceAddRequest import GroupAccessDeviceAddRequest
from broadsoft.requestobjects.GroupAccessDeviceGetRequest import GroupAccessDeviceGetRequest
from broadsoft.requestobjects.GroupAccessDeviceModifyRequest import GroupAccessDeviceModifyRequest
from broadsoft.requestobjects.lib.BroadsoftRequest import BroadsoftRequest
from broadsoft.BroadsoftObject import BroadsoftObject
import xml.etree.ElementTree as ET
import re


class Device(BroadsoftObject):
    def __init__(self, name=None, type=None, description=None, mac_address=None, protocol=None,
                 transport_protocol=None, line_port=None, is_primary=None, **kwargs):
        self.description = description
        self.is_primary = is_primary
        self.name = name
        self.type = type

        # optional
        self.line_port = line_port
        self.mac_address = mac_address
        self.protocol = protocol
        self.transport_protocol = transport_protocol

        BroadsoftObject.__init__(self, **kwargs)

    def __repr__(self):
        return "<Broadsoft Device name:%s, type:%s, line_port:%s>" % (self.name, self.type, self.line_port)

    # expects <AccessDeviceEndpoint> coming from User xml
    def bootstrap_access_device_endpoint(self, ade):
        self.name = ade.findall('./accessDevice/deviceName')[0].text
        self.line_port = ade.findall('./linePort')[0].text
        self.is_primary = True

    # expects to get a result row, from running a UserSharedCallAppearanceGetRequest, which was run through
    # BroadsoftRequest.convert_results_table
    def bootstrap_shared_call_appearance(self, sca):
        self.mac_address = sca['Mac Address']
        self.type = sca['Device Type']
        self.line_port = sca['Line/Port']
        self.name = sca['Device Name']
        self.is_primary = False

    def build_provision_request(self):
        g = GroupAccessDeviceAddRequest(broadsoftinstance=self.broadsoftinstance)
        g.description = self.description
        g.device_name = self.name
        g.device_type = self.type
        g.mac_address = self.mac_address
        if self.protocol:
            g.protocol = self.protocol
        if self.transport_protocol:
            g.transport_protocol = self.transport_protocol
        return g

    def fetch(self, target_name=None):
        if not target_name:
            target_name = self.name
        self.xml = GroupAccessDeviceGetRequest.get_device(name=target_name, broadsoftinstance=self.broadsoftinstance)
        self.from_xml()

    def from_xml(self):
        BroadsoftObject.from_xml(self)

        self.type = self.xml.findall('./command/deviceType')[0].text
        descs = self.xml.findall('./command/description')
        if len(descs) > 0:
            self.description = descs[0].text

    def set_password(self, did=None, sip_user_name=None, sip_password=None, **kwargs):
        if not did and not sip_user_name:
            raise ValueError("can't call Device.set_password without a value for did or sip_user_name")

        if not sip_password:
            raise ValueError("can't call Device.set_password without a value for password")

        if not self.name:
            raise ValueError("can't call Device.set_password without a value for device name")

        if not sip_user_name and did:
            b = BroadsoftRequest()
            sip_user_name = self.derive_sip_user_id(did=did)

        g = GroupAccessDeviceModifyRequest(device_name=self.name, sip_user_name=sip_user_name,
                                           sip_password=sip_password, broadsoftinstance=self.broadsoftinstance,
                                           **kwargs)
        g.post()