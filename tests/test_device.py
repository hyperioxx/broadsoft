import unittest.mock
from broadsoft.Device import Device
from broadsoft.requestobjects.GroupAccessDeviceAddRequest import GroupAccessDeviceAddRequest
from xml.etree.ElementTree import Element


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

    def test_from_xml_derives_primary(self):
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

    def test_from_xml_primary_device(self):
        # found in UserGetRequest, which is called by Account
        self.assertFalse("write this")

    def test_from_xml_shared_call_appearance(self):
        # found in UserSharedCallAppearanceGetRequest, which is called by Account
        self.assertFalse("write this")