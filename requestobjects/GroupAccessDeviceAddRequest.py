import xml.etree.ElementTree as ET
from broadsoft.requestobjects.lib.BroadsoftRequest import BroadsoftRequest
from nettools.MACtools import MAC


class GroupAccessDeviceAddRequest(BroadsoftRequest):
    command_name = 'GroupAccessDeviceAddRequest14'
    check_success = True

    def __init__(self, device_name=None, device_type=None, description=None,
                 protocol='SIP 2.0', transport_protocol='Unspecified', mac_address=None, **kwargs):
        # group_id will be inherited from BroadsoftRequest.default_group_id, but can be overridden by passing
        # group_id (will get picked up in **kwargs)
        self.description = description
        self.device_name = device_name
        self.device_type = device_type
        self.mac_address = mac_address
        if self.mac_address:
            self.convert_mac_address()
        self.protocol = protocol
        self.transport_protocol = transport_protocol
        BroadsoftRequest.__init__(self, **kwargs)

    def build_command_xml(self):
        if self.mac_address:
            self.convert_mac_address()
        self.validate()

        cmd = self.build_command_shell()

        spid = ET.SubElement(cmd, 'serviceProviderId')
        spid.text = self.service_provider

        gid = ET.SubElement(cmd, 'groupId')
        gid.text = self.group_id

        dn = ET.SubElement(cmd, 'deviceName')
        dn.text = self.device_name

        dt = ET.SubElement(cmd, 'deviceType')
        dt.text = self.device_type

        if self.mac_address:
            ma = ET.SubElement(cmd, 'macAddress')
            ma.text = self.mac_address

        d = ET.SubElement(cmd, 'description')
        d.text = self.description

        return cmd

    def convert_mac_address(self):
        m = MAC(mac=self.mac_address)
        m.denude()
        self.mac_address = m.bare_mac

    def validate(self):
        import re

        if self.mac_address:
            m = MAC(mac=self.mac_address)
            m.validate()
            if not m.valid:
                raise ValueError("the MAC address you provided to broadsoft.GroupAccessDeviceAddRequest.to_xml() is not valid")

        if self.device_name is None:
            raise ValueError("can't run broadsoft.GroupAccessDeviceAddRequest.to_xml() without a value for device_name")

        if self.device_type is None:
            raise ValueError("can't run broadsoft.GroupAccessDeviceAddRequest.to_xml() without a value for device_type")

        if self.protocol is None:
            raise ValueError("can't run broadsoft.GroupAccessDeviceAddRequest.to_xml() without a value for protocol")

        if self.transport_protocol is None:
            raise ValueError("can't run broadsoft.GroupAccessDeviceAddRequest.to_xml() without a value for transport_protocol")

    @staticmethod
    def add(first_name, last_name, did, sip_user_id=None, kname=None, sip_password=None, email=None, **kwargs):
        #u = GroupAccessDeviceAddRequest(first_name=first_name, last_name=last_name, did=did, sip_user_id=sip_user_id, kname=kname, sip_password=sip_password, email=email, **kwargs)
        #u.post()
        pass
