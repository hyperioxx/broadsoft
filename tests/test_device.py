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
        d.xml = """
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
                """
        d.from_xml()()
        self.assertIsInstance(d.xml, Element)

    def test_from_xml_derives_primary_value(self):
        # raw response for fetching a user with a device
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
        d.from_xml()
        self.assertTrue(d.is_primary)

        # device extracted from user
        d = Device(xml="""
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
                """)
        d.from_xml()
        self.assertTrue(d.is_primary)

        # shared call appearance
        d = Device(xml='<?xml version="1.0" encoding="ISO-8859-1"?><BroadsoftDocument protocol="OCI" xmlns="C" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><sessionId xmlns="">192.168.1.151,1476473244,1496090738961</sessionId><command echo="" xsi:type="UserSharedCallAppearanceGetResponse16sp2" xmlns=""><alertAllAppearancesForClickToDialCalls>false</alertAllAppearancesForClickToDialCalls><alertAllAppearancesForGroupPagingCalls>false</alertAllAppearancesForGroupPagingCalls><maxAppearances>10</maxAppearances><allowSCACallRetrieve>false</allowSCACallRetrieve><enableMultipleCallArrangement>false</enableMultipleCallArrangement><multipleCallArrangementIsActive>false</multipleCallArrangementIsActive><endpointTable><colHeading>Device Level</colHeading><colHeading>Device Name</colHeading><colHeading>Device Type</colHeading><colHeading>Line/Port</colHeading><colHeading>SIP Contact</colHeading><colHeading>Port Number</colHeading><colHeading>Device Support Visual Device Management</colHeading><colHeading>Is Active</colHeading><colHeading>Allow Origination</colHeading><colHeading>Allow Termination</colHeading><colHeading>Mac Address</colHeading><row><col>Group</col><col>beavervvx</col><col>Polycom-VVX1500</col><col>beavervvx_lp@broadsoft-dev.mit.edu</col><col>sip:</col><col/><col>false</col><col>true</col><col>true</col><col>true</col><col/></row></endpointTable><allowBridgingBetweenLocations>false</allowBridgingBetweenLocations><bridgeWarningTone>None</bridgeWarningTone><enableCallParkNotification>false</enableCallParkNotification></command></BroadsoftDocument>')
        d.from_xml()
        self.assertFalse(d.is_primary)

        # nothing
        d = Device()
        d.from_xml()
        self.assertIsNone(d.is_primary)

    def test_provision_respects_is_primary_when_set(self):
        self.assertFalse("write this")

    @unittest.mock.patch('broadsoft.requestobjects.GroupAccessDeviceGetRequest.GroupAccessDeviceGetRequest.get_device', side_effect=fetch_device_mock)
    def test_from_xml_primary_device_embedded_in_user(
            self,
            fetch_device_patch
    ):
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
        d.from_xml()
        self.assertEqual(d.name, 'beaver550')
        self.assertEqual(d.line_port, '2212221101_lp@broadsoft-dev.mit.edu')
        self.assertEqual(d.type, 'Polycom SoundPoint IP 550')
        self.assertEqual(d.description, 'the 550 what tim uses')

    @unittest.mock.patch('broadsoft.requestobjects.GroupAccessDeviceGetRequest.GroupAccessDeviceGetRequest.get_device',
                         side_effect=fetch_device_mock)
    def test_from_xml_primary_device_standalone(
            self,
            fetch_device_patch
    ):
        d = Device(xml="""
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
                        """)
        d.from_xml()
        self.assertEqual(d.name, 'beaver550')
        self.assertEqual(d.line_port, '2212221101_lp@broadsoft-dev.mit.edu')
        self.assertEqual(d.type, 'Polycom SoundPoint IP 550')
        self.assertEqual(d.description, 'the 550 what tim uses')

    @unittest.mock.patch('broadsoft.requestobjects.GroupAccessDeviceGetRequest.GroupAccessDeviceGetRequest.get_device',
                         side_effect=fetch_device_mock)
    def test_from_xml_shared_call_appearance(
            self,
            get_device_patch
    ):
        d = Device(xml="""<?xml version="1.0" encoding="ISO-8859-1"?>
            <BroadsoftDocument protocol="OCI" xmlns="C" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
            <sessionId xmlns="">192.168.1.151,1476473244,1496090738961</sessionId>
            <command echo="" xsi:type="UserSharedCallAppearanceGetResponse16sp2" xmlns="">
                <alertAllAppearancesForClickToDialCalls>false</alertAllAppearancesForClickToDialCalls>
                <alertAllAppearancesForGroupPagingCalls>false</alertAllAppearancesForGroupPagingCalls>
                <maxAppearances>10</maxAppearances>
                <allowSCACallRetrieve>false</allowSCACallRetrieve>
                <enableMultipleCallArrangement>false</enableMultipleCallArrangement>
                <multipleCallArrangementIsActive>false</multipleCallArrangementIsActive>
                <endpointTable>
                    <colHeading>Device Level</colHeading>
                    <colHeading>Device Name</colHeading>
                    <colHeading>Device Type</colHeading>
                    <colHeading>Line/Port</colHeading>
                    <colHeading>SIP Contact</colHeading>
                    <colHeading>Port Number</colHeading>
                    <colHeading>Device Support Visual Device Management</colHeading>
                    <colHeading>Is Active</colHeading>
                    <colHeading>Allow Origination</colHeading>
                    <colHeading>Allow Termination</colHeading>
                    <colHeading>Mac Address</colHeading>
                    <row>
                        <col>Group</col>
                        <col>beaverphone</col>
                        <col>Polycom SoundPoint IP 550</col>
                        <col>beavervvx_lp@broadsoft-dev.mit.edu</col>
                        <col>sip:</col>
                        <col/>
                        <col>false</col>
                        <col>true</col>
                        <col>true</col>
                        <col>false</col>
                        <col>aa:bb:cc:11:22:33</col>
                    </row>
                </endpointTable>
                <allowBridgingBetweenLocations>false</allowBridgingBetweenLocations>
                <bridgeWarningTone>None</bridgeWarningTone>
                <enableCallParkNotification>false</enableCallParkNotification>
            </command>
        </BroadsoftDocument>
        """)
        d.from_xml()
        self.assertEqual('beavervvx_lp@broadsoft-dev.mit.edu', d.line_port)
        self.assertEqual('aa:bb:cc:11:22:33', d.mac_address)
        self.assertEqual('beaverphone', d.name)
        self.assertEqual('Polycom SoundPoint IP 550', d.type)
        self.assertEqual(d.description, 'the 550 what tim uses')

    def test_derive_xml_type_when_is_single_sca(self):
        self.assertFalse("figure out what multiple results wuold look like and write this")

    def test_when_call_fetch_discovers_lineport(self):
        self.assertFalse("write this")

    def test_from_shared_call_appearance(self):
        row = {'Mac Address': 'aa:bb:cc:dd:ee:ff', 'Device Level': 'Group', 'Allow Termination': 'true', 'Allow Origination': 'true', 'Device Type': 'Polycom-VVX1500', 'Is Active': 'true', 'Port Number': None, 'Line/Port': 'beavervvx_lp@broadsoft-dev.mit.edu', 'Device Support Visual Device Management': 'false', 'Device Name': 'beavervvx', 'SIP Contact': 'sip:'}
        d = Device()
        d.bootstrap_shared_call_appearance(sca=row)
        self.assertEqual(d.mac_address, row['Mac Address'])
        self.assertEqual(d.type, row['Device Type'])
        self.assertEqual(d.line_port, row['Line/Port'])
        self.assertEqual(d.name, row['Device Name'])
        self.assertFalse(d.is_primary)
        self.assertFalse("also need to fetch and mock that fetch")

    def test_fetch(self):
        # can pass use_test, override name, etc
        self.assertFalse("write this; based on name")