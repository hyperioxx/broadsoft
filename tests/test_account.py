import unittest.mock
from broadsoft.Device import Device
from broadsoft.Account import Account
from broadsoft.requestobjects.lib.BroadsoftRequest import BroadsoftRequest
from broadsoft.requestobjects.UserAddRequest import UserAddRequest
from broadsoft.requestobjects.UserModifyRequest import UserModifyRequest
from broadsoft.requestobjects.UserServiceAssignListRequest import UserServiceAssignListRequest
from broadsoft.requestobjects.GroupAccessDeviceAddRequest import GroupAccessDeviceAddRequest
from broadsoft.requestobjects.UserSharedCallAppearanceAddEndpointRequest import UserSharedCallAppearanceAddEndpointRequest
from xml.etree.ElementTree import Element
import xml.etree.ElementTree as ET


def get_device_mock(name, **kwargs):
    if name == 'beaver550':
        xml = """<?xml version="1.0" encoding="ISO-8859-1"?>
            <BroadsoftDocument protocol="OCI" xmlns="C" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
            <sessionId xmlns="">192.168.0.100,1743299062,1496154334750</sessionId>
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
            </BroadsoftDocument>"""
        return ET.fromstring(xml)

    if name == 'beavervvx':
        xml = """<?xml version="1.0" encoding="ISO-8859-1"?>
            <BroadsoftDocument protocol="OCI" xmlns="C" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
            <sessionId xmlns="">192.168.0.100,1743299062,1496154334750</sessionId>
            <command echo="" xsi:type="GroupAccessDeviceGetResponse18sp1" xmlns="">
                <deviceType>Polycom-VVX1500</deviceType>
                <protocol>SIP 2.0</protocol>
                <description>cool vvx</description>
                <numberOfPorts>
                    <quantity>4</quantity>
                </numberOfPorts>
                <numberOfAssignedPorts>1</numberOfAssignedPorts>
                <status>Online</status>
                <configurationMode>Default</configurationMode>
                <transportProtocol>Unspecified</transportProtocol>
                <useCustomUserNamePassword>false</useCustomUserNamePassword>
            </command>
            </BroadsoftDocument>"""
        return ET.fromstring(xml)

    if name == 'beaverspa':
        xml = """<?xml version="1.0" encoding="ISO-8859-1"?>
            <BroadsoftDocument protocol="OCI" xmlns="C" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
            <sessionId xmlns="">192.168.0.100,1743299062,1496154334750</sessionId>
            <command echo="" xsi:type="GroupAccessDeviceGetResponse18sp1" xmlns="">
                <deviceType>Cisco SPA8000</deviceType>
                <protocol>SIP 2.0</protocol>
                <description>cool spa</description>
                <numberOfPorts>
                    <quantity>4</quantity>
                </numberOfPorts>
                <numberOfAssignedPorts>1</numberOfAssignedPorts>
                <status>Online</status>
                <configurationMode>Default</configurationMode>
                <transportProtocol>Unspecified</transportProtocol>
                <useCustomUserNamePassword>false</useCustomUserNamePassword>
            </command>
            </BroadsoftDocument>"""
        return ET.fromstring(xml)


def get_sca_mock(**kwargs):
    xml = """<?xml version="1.0" encoding="ISO-8859-1"?>
        <BroadsoftDocument protocol="OCI" xmlns="C" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
        <sessionId xmlns="">192.168.0.100,1507939013,1496153955612</sessionId>
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
                    <col>beavervvx</col>
                    <col>Polycom-VVX1500</col>
                    <col>beavervvx_lp@broadsoft-dev.mit.edu</col>
                    <col>sip:</col>
                    <col/>
                    <col>false</col>
                    <col>true</col>
                    <col>true</col>
                    <col>true</col>
                    <col/>
                </row>
                <row>
                    <col>Group</col>
                    <col>beaverspa</col>
                    <col>Cisco SPA8000</col>
                    <col>beaverspa_lp@broadsoft-dev.mit.edu</col>
                    <col>sip:</col>
                    <col/>
                    <col>false</col>
                    <col>true</col>
                    <col>true</col>
                    <col>true</col>
                    <col/>
                </row>
            </endpointTable>
            <allowBridgingBetweenLocations>false</allowBridgingBetweenLocations>
            <bridgeWarningTone>None</bridgeWarningTone>
            <enableCallParkNotification>false</enableCallParkNotification>
        </command>
        </BroadsoftDocument>"""
    return ET.fromstring(xml)


class TestBroadsoftAccount(unittest.TestCase):
    def test_account_attrs_get_passed_to_request_object(self):
        a = Account(did=6175551212, extension=51212, last_name='beaver', first_name='tim',
                    sip_user_id='beaver@broadsoft.mit.edu', kname='beaver', email='beaver@mit.edu',
                    use_test=True)
        ro = a.build_request_object()
        uadd = ro.commands[0]
        self.assertEqual(a.did, uadd.did)
        self.assertEqual(a.last_name, uadd.last_name)
        self.assertEqual(a.first_name, uadd.first_name)
        self.assertEqual(a.sip_user_id, uadd.sip_user_id)
        self.assertEqual(a.kname, uadd.kname)
        self.assertEqual(a.email, uadd.email)
        self.assertEqual(a.use_test, uadd.use_test)

        # try again, flip-flopping use test
        a = Account(did=6175551212, extension=51212, last_name='beaver', first_name='tim',
                    sip_user_id='beaver@broadsoft.mit.edu', kname='beaver', email='beaver@mit.edu',
                    use_test=False)
        ro = a.build_request_object()
        uadd = ro.commands[0]
        self.assertEqual(a.did, uadd.did)
        self.assertEqual(a.last_name, uadd.last_name)
        self.assertEqual(a.first_name, uadd.first_name)
        self.assertEqual(a.sip_user_id, uadd.sip_user_id)
        self.assertEqual(a.kname, uadd.kname)
        self.assertEqual(a.email, uadd.email)
        self.assertEqual(a.use_test, uadd.use_test)

    def test_devices_added_get_built_into_request_object(self):
        d1 = Device(description='beaver phone 1', name='beaverphone1', type='iphone')
        d2 = Device(description='beaver phone 2', name='beaverphone2', type='hamburger')
        a = Account(did=6175551212, extension=51212, last_name='beaver', first_name='tim',
                    sip_user_id='beaver@broadsoft.mit.edu', kname='beaver', email='beaver@mit.edu',
                    use_test=True, services=['a'])
        a.devices = [d1, d2]
        ro = a.build_request_object()

        # expect to see 6 commands in the request object...
        self.assertEqual(6, len(ro.commands))

        # ... one to add the user
        cmd = ro.commands[0]
        self.assertIsInstance(cmd, UserAddRequest)

        # ... one to configure services
        cmd = ro.commands[1]
        self.assertIsInstance(cmd, UserServiceAssignListRequest)
        self.assertEqual(['a'], cmd.services)

        # ... one to add d1
        cmd = ro.commands[2]
        self.assertIsInstance(cmd, GroupAccessDeviceAddRequest)
        self.assertEqual(cmd.device_name, 'beaverphone1')

        # ... one to add d2
        cmd = ro.commands[3]
        self.assertIsInstance(cmd, GroupAccessDeviceAddRequest)
        self.assertEqual(cmd.device_name, 'beaverphone2')

        # ... one to associate d1 with the user directly
        cmd = ro.commands[4]
        self.assertIsInstance(cmd, UserModifyRequest)
        self.assertEqual(cmd.device_name, 'beaverphone1')

        # ... one to associate d2 with the user as shared call appearance
        cmd = ro.commands[5]
        self.assertIsInstance(cmd, UserSharedCallAppearanceAddEndpointRequest)
        self.assertEqual(cmd.device_name, 'beaverphone2')

    def test_child_objects_inherit_use_test(self):
        d1 = Device(description='beaver phone 1', name='beaverphone1', type='iphone', use_test=False)
        a = Account(did=6175551212, extension=51212, last_name='beaver', first_name='tim',
                    sip_user_id='beaver@broadsoft.mit.edu', kname='beaver', email='beaver@mit.edu',
                    use_test=True)
        a.devices = [d1]
        ro = a.build_request_object()
        for cmd in ro.commands:
            self.assertTrue(cmd.use_test)

    def test_inherits_default_services(self):
        a = Account()
        self.assertEqual(a.default_services, a.services)

        # and can override default services
        a = Account(services=['a'])
        self.assertEqual(['a'], a.services)

    def test_add_services(self):
        # when no services specified, should get default services in UserServiceAssignListRequest object
        a = Account()
        b = BroadsoftRequest()
        a.add_services(req_object=b)
        s = b.commands[0]
        self.assertIsInstance(s, UserServiceAssignListRequest)
        self.assertEqual(a.default_services, s.services)

        # when services overridden, should get inserted
        a = Account(services=['a','b'])
        b = BroadsoftRequest()
        a.add_services(req_object=b)
        s = b.commands[0]
        self.assertIsInstance(s, UserServiceAssignListRequest)
        self.assertEqual(['a','b'], s.services)

    def test_link_primary_device(self):
        a = Account(did=6175551212)
        b = BroadsoftRequest()
        d1 = Device(description='beaver phone 1', name='beaverphone1', type='iphone', use_test=False)
        a.link_primary_device(req_object=b, device=d1)
        self.assertEqual(1, len(b.commands))
        cmd = b.commands[0]
        self.assertIsInstance(cmd, UserModifyRequest)
        self.assertEqual(cmd.did, str(a.did))
        self.assertEqual(cmd.sip_user_id, str(a.did) + '@' + b.default_domain)
        self.assertEqual(cmd.device_name, d1.name)

    def test_link_sca_device(self):
        a = Account(did=6175551212)
        b = BroadsoftRequest()
        d1 = Device(description='beaver phone 1', name='beaverphone1', type='iphone', use_test=False)
        a.link_sca_device(req_object=b, device=d1)
        self.assertEqual(1, len(b.commands))
        cmd = b.commands[0]
        self.assertIsInstance(cmd, UserSharedCallAppearanceAddEndpointRequest)
        self.assertEqual(cmd.did, str(a.did))
        self.assertEqual(cmd.sip_user_id, str(a.did) + '@' + b.default_domain)
        self.assertEqual(cmd.device_name, d1.name)
        self.assertEqual(cmd.line_port, d1.name + '_lp@' + b.default_domain)

    def test_add_devices(self):
        a = Account(did=6175551212)
        b = BroadsoftRequest()
        d1 = Device(description='beaver phone 1', name='beaverphone1', type='iphone', use_test=False)
        d2 = Device(description='beaver phone 2', name='beaverphone2', type='cisco', use_test=False)
        a.devices = [d1, d2]
        a.add_devices(req_object=b)

        # should be four requests
        self.assertEqual(4, len(b.commands))

        # Not going to investigate each one in details, that's handled in test_link_primary_device() and
        # test_link_sca_device(). Just checking for object type and order.
        cmd = b.commands[0]
        self.assertIsInstance(cmd, GroupAccessDeviceAddRequest)
        self.assertEqual(d1.name, cmd.device_name)

        cmd = b.commands[1]
        self.assertIsInstance(cmd, GroupAccessDeviceAddRequest)
        self.assertEqual(d2.name, cmd.device_name)

        cmd = b.commands[2]
        self.assertIsInstance(cmd, UserModifyRequest)
        self.assertEqual(d1.name, cmd.device_name)

        cmd = b.commands[3]
        self.assertIsInstance(cmd, UserSharedCallAppearanceAddEndpointRequest)
        self.assertEqual(d2.name, cmd.device_name)

    def test_xml_converted_to_elementtree_at_init(self):
        a = Account(xml="""
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

        self.assertIsInstance(a.xml, Element)

    def test_xml_converted_to_elementtree_at_from_xml(self):
        a = Account()
        a.xml = """
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
        a.from_xml()
        self.assertIsInstance(a.xml, Element)

    def test_from_xml_hands_off_accessDeviceEndpoint_to_device_object(self):
        # for each one, instantiate a Device object
        self.assertFalse("write this")

    def test_fetch_secondary_call_appearances(self):
        # for each one, instantiate a Device object
        self.assertFalse("write this")

    def test_from_xml_blanks_out_devices(self):
        a = Account()
        a.devices = ('a')
        a.from_xml()
        self.assertEqual([], a.devices)

    @unittest.mock.patch('broadsoft.requestobjects.UserSharedCallAppearanceGetRequest.UserSharedCallAppearanceGetRequest.get_devices', side_effect=get_sca_mock)
    @unittest.mock.patch('broadsoft.requestobjects.GroupAccessDeviceGetRequest.GroupAccessDeviceGetRequest.get_device', side_effect=get_device_mock)
    def test_load_devices(
            self,
            get_device_patch,
            get_scas_patch
    ):
        a = Account(xml = """
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
        a.did = '2212221101'
        a.sip_user_id = '2212221101@broadsoft-dev.mit.edu'
        a.load_devices()

        # should be a call to GroupAccessDeviceGetRequest.get_device for the primary device in the user xml
        call = get_device_patch.call_args_list[0]
        args, kwargs = call
        self.assertEqual('beaver550', kwargs['name'])

        # should be a call to GroupAccessDeviceGetRequest.get_device for the two scas
        call = get_device_patch.call_args_list[1]
        args, kwargs = call
        self.assertEqual('beavervvx', kwargs['name'])

        call = get_device_patch.call_args_list[2]
        args, kwargs = call
        self.assertEqual('beaverspa', kwargs['name'])

        # should be three devices
        self.assertEqual(3, len(a.devices))

        d = a.devices[0]
        self.assertEqual('beaver550', d.name)
        self.assertTrue(d.is_primary)

        d = a.devices[1]
        self.assertEqual('beavervvx', d.name)
        self.assertFalse(d.is_primary)

        d = a.devices[2]
        self.assertEqual('beaverspa', d.name)
        self.assertFalse(d.is_primary)

    def test_fetch(self):
        self.assertFalse("write this")

    def test_can_pass_use_test_to_child_objects(self):
        self.assertFalse("write this")

    def test_from_xml(self):
        self.assertFalse("mock out calls in load_devices here and every call")
        a = Account()
        a.xml = """
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
        a.from_xml()
        self.assertEqual('2212221101', a.did)
        self.assertEqual('Tim', a.first_name)
        self.assertEqual('Beaver', a.last_name)
        self.assertEqual('1101', a.extension)
        self.assertEqual('2212221101@broadsoft-dev.mit.edu', a.sip_user_id)
        self.assertEqual(1, len(a.devices))
