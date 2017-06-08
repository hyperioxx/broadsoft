import xml.etree.ElementTree as ET
from broadsoft.requestobjects.lib.BroadsoftRequest import BroadsoftRequest
from broadsoft.requestobjects.datatypes.AccessDeviceCredentials import AccessDeviceCredentials
from nettools.MACtools import MAC


class GroupAccessDeviceModifyRequest(BroadsoftRequest):
    command_name = 'GroupAccessDeviceModifyRequest14'
    check_success = True

    def __init__(self, device_name=None, description=None,
                 protocol='SIP 2.0', transport_protocol='Unspecified', mac_address=None, ip_address=None, port=None,
                 sip_user_name=None, sip_password=None,
                 **kwargs):
        self.description = description
        self.device_name = device_name
        self.ip_address = ip_address
        self.mac_address = mac_address
        self.port = port
        self.protocol = protocol
        self.sip_user_name = sip_user_name
        self.sip_password = sip_password
        self.transport_protocol = transport_protocol

        # these I don't expect to ever feed, so not in __init__args, but available to be modified just in case
        self.configuration_file = None
        self.configuration_mode = 'Default'
        self.mobility_manager_default_originating_service_key = None
        self.mobility_manager_default_terminating_service_key = None
        self.mobility_manager_provisioning_URL = None
        self.mobility_manager_provisioning_user_name = None
        self.mobility_manager_provisioning_password = None
        self.outbound_proxy_server_net_address = None
        self.physical_location = None
        self.serial_number = None
        self.stun_server_net_address = None

        BroadsoftRequest.__init__(self, **kwargs)

    def build_command_xml(self):
        self.prep_for_xml()
        self.validate()

        cmd = self.build_command_shell()

        spid = ET.SubElement(cmd, 'serviceProviderId')
        spid.text = self.service_provider

        gid = ET.SubElement(cmd, 'groupId')
        gid.text = self.group_id

        dn = ET.SubElement(cmd, 'deviceName')
        dn.text = self.device_name

        if self.mac_address:
            ma = ET.SubElement(cmd, 'macAddress')
            ma.text = self.mac_address

        if self.description:
            d = ET.SubElement(cmd, 'description')
            d.text = self.description

        if self.protocol:
            e = ET.SubElement(cmd, 'protocol')
            e.text = self.protocol

        if self.ip_address:
            e = ET.SubElement(cmd, 'netAddress')
            e.text = self.ip_address

        if self.port:
            e = ET.SubElement(cmd, 'port')
            e.text = self.port

        if self.outbound_proxy_server_net_address:
            e = ET.SubElement(cmd, 'outboundProxyServerNetAddress')
            e.text = self.outbound_proxy_server_net_address

        if self.stun_server_net_address:
            e = ET.SubElement(cmd, 'stunServerNetAddress')
            e.text = self.stun_server_net_address

        if self.serial_number:
            e = ET.SubElement(cmd, 'serialNumber')
            e.text = self.serial_number

        if self.configuration_mode:
            e = ET.SubElement(cmd, 'configurationMode')
            e.text = self.configuration_mode

        if self.configuration_file:
            e = ET.SubElement(cmd, 'configurationFile')
            e.text = self.configuration_file

        if self.physical_location:
            e = ET.SubElement(cmd, 'physicalLocation')
            e.text = self.physical_location

        if self.transport_protocol:
            e = ET.SubElement(cmd, 'transportProtocol')
            e.text = self.transport_protocol

        if self.mobility_manager_provisioning_URL:
            e = ET.SubElement(cmd, 'mobilityManagerProvisioningURL')
            e.text = self.mobility_manager_provisioning_URL

        if self.mobility_manager_provisioning_user_name:
            e = ET.SubElement(cmd, 'mobilityManagerProvisioningUserName')
            e.text = self.mobility_manager_provisioning_user_name

        if self.mobility_manager_provisioning_password:
            e = ET.SubElement(cmd, 'mobilityManagerProvisioningPassword')
            e.text = self.mobility_manager_provisioning_password

        if self.mobility_manager_default_originating_service_key:
            e = ET.SubElement(cmd, 'mobilityManagerDefaultOriginatingServiceKey')
            e.text = self.mobility_manager_default_originating_service_key

        if self.mobility_manager_default_terminating_service_key:
            e = ET.SubElement(cmd, 'mobilityManagerDefaultTerminatingServiceKey')
            e.text = self.mobility_manager_default_terminating_service_key

        if self.sip_user_name or self.sip_password:
            e = ET.SubElement(cmd, 'useCustomUserNamePassword')
            e.text = 'true'

            adc = AccessDeviceCredentials(sip_user_name=self.sip_user_name, sip_password=self.sip_password)
            cmd.append(adc.to_xml())

        return cmd

    def validate(self):
        if self.device_name is None:
            raise ValueError("can't run broadsoft.GroupAccessDeviceModifyRequest.to_xml() without a value for device_name")
