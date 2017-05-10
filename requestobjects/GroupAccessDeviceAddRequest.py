import xml.etree.ElementTree as ET
from broadsoft.requestobjects.lib.BroadsoftRequest import BroadsoftRequest


class GroupAccessDeviceAddRequest(BroadsoftRequest):
    command_name = 'GroupAccessDeviceAddRequest14'
    check_success = True

    def __init__(self, did=None, device_name=None, device_type=None, protocol='SIP 2.0',
                 transport_protocol='Unspecified', **kwargs):
        # group_id will be inherited from BroadsoftRequest.default_group_id, but can be overridden by passing
        # group_id (will get picked up in **kwargs)
        self.did = did
        if self.did:
            self.did = BroadsoftRequest.convert_phone_number(number=self.did)
        self.device_name = device_name
        self.device_type = device_type
        self.protocol = protocol
        self.transport_protocol = transport_protocol
        BroadsoftRequest.__init__(self, **kwargs)

    def build_command_xml(self):
        self.did = BroadsoftRequest.convert_phone_number(number=self.did)
        self.validate()

        cmd = self.build_command_shell()

        """
        serviceProviderId
        groupId
        deviceName
        deviceType
        macAddress
        description
        
        <command xsi:type="GroupAccessDeviceAddRequest14" xmlns="" echo="GroupAccessDeviceAddRequest14 - add genericSIP Primary Line device">
            <serviceProviderId>ENT136</serviceProviderId>
            <groupId>mit</groupId>
            <deviceName>mituser1_genericSIP</deviceName>
            <deviceType>Generic SIP Phone</deviceType>
            <protocol>SIP 2.0</protocol>
            <transportProtocol>Unspecified</transportProtocol>
        </command>
        """

        return cmd

    def validate(self):
        import re
        # ensure required fields set
        # need a list of legal device types
        raise RuntimeError("need to develop this")

    @staticmethod
    def add(first_name, last_name, did, sip_user_id=None, kname=None, sip_password=None, email=None, **kwargs):
        #u = GroupAccessDeviceAddRequest(first_name=first_name, last_name=last_name, did=did, sip_user_id=sip_user_id, kname=kname, sip_password=sip_password, email=email, **kwargs)
        #u.post()
        pass
