import unittest.mock
from broadsoft.Device import Device
from broadsoft.requestobjects.GroupAccessDeviceAddRequest import GroupAccessDeviceAddRequest
from xml.etree.ElementTree import Element
import xml.etree.ElementTree as ET


def fetch_device_mock(**kwargs):
    xml = """<ns0:BroadsoftDocument xmlns:ns0="C" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" protocol="OCI">
    <sessionId>Chriss-MacBook-Pro-4.local,2017-05-30 01:45:30.442624,5492572214</sessionId>
    <command echo="" xsi:type="GroupAccessDeviceGetResponse18sp1">
        <deviceType>Polycom SoundPoint IP 550</deviceType>
        <protocol>SIP 2.0</protocol>
        <description>the 550 what tim uses</description>
        <numberOfPorts>
            <quantity>4</quantity>
        </numberOfPorts>
        <numberOfAssignedPorts>1</numberOfAssignedPorts>
        <status>Online</status>
        <configurationMode>Default</configurationMode>
        <transportProtocol>Unspecified</transportProtocol>
        <useCustomUserNamePassword>false</useCustomUserNamePassword>
    </command>
    </ns0:BroadsoftDocument>"""
    return ET.fromstring(xml)


class TestBroadsoftDevice(unittest.TestCase):
    def test_device_attrs_get_passed_to_request_object(self):
        d = Device(name='beaverphone', description="Tim Beaver's Phone", type='iphone',
                   use_test=True, mac_address='aabbcc112233', protocol='gopher',
                   transport_protocol='ftp')
        ro = d.build_request_object()
        self.assertEqual(d.name, ro.device_name)
        self.assertEqual(d.type, ro.device_type)
        self.assertEqual(d.mac_address, ro.mac_address)
        self.assertEqual(d.protocol, ro.protocol)
        self.assertEqual(d.transport_protocol, ro.transport_protocol)

        # try again, flip-flopping use test
        d = Device(name='beaverphone', description="Tim Beaver's Phone", type='iphone',
                   use_test=False, mac_address='aabbcc112233', protocol='gopher',
                   transport_protocol='ftp')
        ro = d.build_request_object()
        self.assertEqual(d.name, ro.device_name)
        self.assertEqual(d.type, ro.device_type)
        self.assertEqual(d.mac_address, ro.mac_address)
        self.assertEqual(d.protocol, ro.protocol)
        self.assertEqual(d.transport_protocol, ro.transport_protocol)

    def test_device_default_protocols_respected(self):
        d = Device(name='beaverphone', description="Tim Beaver's Phone", type='iphone',
                   mac_address='aabbcc112233', protocol=None, transport_protocol=None)
        ro = d.build_request_object()

        g = GroupAccessDeviceAddRequest()

        self.assertEqual(ro.protocol, g.protocol)
        self.assertEqual(ro.transport_protocol, g.transport_protocol)

    def test_xml_converted_to_elementtree_at_init(self):
        d = Device(xml="""
                    <ns0:BroadsoftDocument xmlns:ns0="C" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" protocol="OCI">
                    <sessionId>dhcp-18-189-4-125.dyn.mit.edu,2017-05-26 15:33:32.605555,3222027341</sessionId>
                    <command echo="" xsi:type="UserGetResponse21">
                        <serviceProviderId>ENT136</serviceProviderId>
                        <groupId>mit</groupId>
                        <lastName>Beaver</lastName>
                        <firstName>Tim</firstName>
                        <callingLineIdLastName>Beaver</callingLineIdLastName>
                        <callingLineIdFirstName>Tim</callingLineIdFirstName>
                        <hiraganaLastName>Beaver</hiraganaLastName>
                        <hiraganaFirstName>Tim</hiraganaFirstName>
                        <phoneNumber>2212221101</phoneNumber>
                        <extension>1101</extension>
                        <language>English</language>
                        <timeZone>America/New_York</timeZone>
                        <timeZoneDisplayName>(GMT-04:00) (US) Eastern Time</timeZoneDisplayName>
                        <defaultAlias>2212221101@broadsoft-dev.mit.edu</defaultAlias>
                        <accessDeviceEndpoint>
                            <accessDevice>
                                <deviceLevel>Group</deviceLevel>
                                <deviceName>beaver550</deviceName>
                            </accessDevice>
                            <linePort>2212221101_lp@broadsoft-dev.mit.edu</linePort>
                            <staticRegistrationCapable>false</staticRegistrationCapable>
                            <useDomain>true</useDomain>
                            <supportVisualDeviceManagement>false</supportVisualDeviceManagement>
                        </accessDeviceEndpoint>
                        <countryCode>1</countryCode>
                    </command>
                    </ns0:BroadsoftDocument>
                """)

        self.assertIsInstance(d.xml, Element)

    def test_xml_converted_to_elementtree_at_from_xml(self):
        d = Device()
        d.xml = """<?xml version="1.0" encoding="ISO-8859-1"?>
            <BroadsoftDocument protocol="OCI" xmlns="C" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
            <sessionId xmlns="">192.168.0.100,1476473244,1496170270368</sessionId>
            <command echo="" xsi:type="GroupAccessDeviceGetResponse18sp1" xmlns="">
                <deviceType>Polycom SoundPoint IP 550</deviceType>
                <protocol>SIP 2.0</protocol>
                <description>the 550 what tim uses</description>
                <numberOfPorts>
                    <quantity>4</quantity>
                </numberOfPorts>
                <numberOfAssignedPorts>1</numberOfAssignedPorts>
                <status>Online</status>
                <configurationMode>Default</configurationMode>
                <transportProtocol>Unspecified</transportProtocol>
                <useCustomUserNamePassword>false</useCustomUserNamePassword>
            </command>
            </BroadsoftDocument>
            """
        d.from_xml()
        self.assertIsInstance(d.xml, Element)

    def test_from_shared_call_appearance(self):
        row = {'Mac Address': 'aa:bb:cc:dd:ee:ff', 'Device Level': 'Group', 'Allow Termination': 'true', 'Allow Origination': 'true', 'Device Type': 'Polycom-VVX1500', 'Is Active': 'true', 'Port Number': None, 'Line/Port': 'beavervvx_lp@broadsoft-dev.mit.edu', 'Device Support Visual Device Management': 'false', 'Device Name': 'beavervvx', 'SIP Contact': 'sip:'}
        d = Device()
        d.bootstrap_shared_call_appearance(sca=row)
        self.assertEqual(d.mac_address, row['Mac Address'])
        self.assertEqual(d.type, row['Device Type'])
        self.assertEqual(d.line_port, row['Line/Port'])
        self.assertEqual(d.name, row['Device Name'])
        self.assertFalse(d.is_primary)

    @unittest.mock.patch.object(Device, 'from_xml')
    @unittest.mock.patch('broadsoft.requestobjects.GroupAccessDeviceGetRequest.GroupAccessDeviceGetRequest.get_device')
    def test_fetch(
            self, get_device_patch, from_xml_patch
    ):
        # d.name set, target_name not
        d = Device(name='beaverphone')
        d.fetch()
        call = get_device_patch.call_args_list[0]
        args, kwargs = call
        self.assertEqual('beaverphone', kwargs['name'])

        # d.name set, target_name set
        d = Device(name='beaverphone')
        d.fetch(target_name='beaverandroid')
        call = get_device_patch.call_args_list[1]
        args, kwargs = call
        self.assertEqual('beaverandroid', kwargs['name'])

        # d.name not set, target_name set
        d = Device()
        d.fetch(target_name='beaverandroid')
        call = get_device_patch.call_args_list[2]
        args, kwargs = call
        self.assertEqual('beaverandroid', kwargs['name'])

        # use_test
        d = Device(name='beaverphone', use_test=True)
        d.fetch()
        call = get_device_patch.call_args_list[3]
        args, kwargs = call
        self.assertTrue(kwargs['use_test'])

        d = Device(name='beaverphone', use_test=False)
        d.fetch()
        call = get_device_patch.call_args_list[4]
        args, kwargs = call
        self.assertFalse(kwargs['use_test'])
