from broadsoft.requestobjects.GroupAccessDeviceAddRequest import GroupAccessDeviceAddRequest
from broadsoft.requestobjects.GroupAccessDeviceGetRequest import GroupAccessDeviceGetRequest
from broadsoft.BroadsoftObject import BroadsoftObject
import xml.etree.ElementTree as ET
import re


class Device(BroadsoftObject):
    def __init__(self, name=None, type=None, description=None, use_test=False, mac_address=None, protocol=None,
                 transport_protocol=None, line_port=None, is_primary=None, **kwargs):
        self.description = description
        self.is_primary = is_primary
        self.name = name
        self.type = type
        self.use_test = use_test

        # optional
        self.line_port = line_port
        self.mac_address = mac_address
        self.protocol = protocol
        self.transport_protocol = transport_protocol

        BroadsoftObject.__init__(self, **kwargs)

    def build_request_object(self):
        g = GroupAccessDeviceAddRequest(use_test=self.use_test)
        g.description = self.description
        g.device_name = self.name
        g.device_type = self.type
        g.mac_address = self.mac_address
        if self.protocol:
            g.protocol = self.protocol
        if self.transport_protocol:
            g.transport_protocol = self.transport_protocol
        return g

    def fetch(self, name):
        self.name = name
        d = GroupAccessDeviceGetRequest.get_device(name=self.name, use_test=self.use_test)
        self.unpack_group_access_device(device=d)

    def from_xml(self):
        BroadsoftObject.from_xml(self)

        # may have received a primary device from a user object,
        # a raw primary device not embedded in a larger object,
        # or a secondary device from a shared call appearance.
        # each one has a different structure.
        if self.xml:
            cmd = None
            cmds = self.xml.findall('./command')
            if len(cmds) > 0:
                cmd = cmds[0]

            # check to see if there's an accessDeviceEndpoint within a command in the xml
            ades = self.xml.findall('./command/accessDeviceEndpoint')
            if len(ades) > 0:
                ade = ades[0]
                self.is_primary = True
                self.unpack_access_device_endpoint(ade)

            # check to see if the xml is itself an accessDeviceEndpoint
            if self.xml.tag == 'accessDeviceEndpoint':
                ade = self.xml
                self.is_primary = True
                self.unpack_access_device_endpoint(ade)

            # check to see if sharedCallAppearance
            # can tell if command has xsi:type UserSharedCallAppearanceGetResponse
            if cmd and re.match(r'^UserSharedCallAppearanceGetResponse', cmd.get('{http://www.w3.org/2001/XMLSchema-instance}type')):
                self.is_primary = False
                self.unpack_shared_call_appearance(cmd)

    def unpack_access_device_endpoint(self, ade):
        self.name = ade.findall('./accessDevice/deviceName')[0].text
        self.line_port = ade.findall('./linePort')[0].text

        # don't get a full version of the device from what's embedded in the User record...
        # fetch full version from system
        self.fetch(name=self.name)

    def unpack_group_access_device(self, device):
        self.type = device.findall('./command/deviceType')[0].text
        self.description = device.findall('./command/description')[0].text

    def unpack_shared_call_appearance(self, sca):
        pass