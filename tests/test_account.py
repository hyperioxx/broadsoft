import unittest.mock
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element
from broadsoft.lib import BroadsoftInstance
from broadsoft.Account import Account
from broadsoft.Device import Device
from broadsoft.lib.BroadsoftObject import BroadsoftObject
from broadsoft.requestobjects.GroupAccessDeviceAddRequest import GroupAccessDeviceAddRequest
from broadsoft.requestobjects.UserAddRequest import UserAddRequest
from broadsoft.requestobjects.UserModifyRequest import UserModifyRequest
from broadsoft.requestobjects.UserServiceAssignListRequest import UserServiceAssignListRequest
from broadsoft.requestobjects.UserSharedCallAppearanceAddEndpointRequest import \
    UserSharedCallAppearanceAddEndpointRequest
from broadsoft.requestobjects.lib.BroadsoftRequest import BroadsoftRequest
from broadsoft.Voicemail import Voicemail
from broadsoft.requestobjects.UserVoiceMessagingUserModifyVoiceManagementRequest import UserVoiceMessagingUserModifyVoiceManagementRequest
from broadsoft.requestobjects.UserThirdPartyVoiceMailSupportModifyRequest import UserThirdPartyVoiceMailSupportModifyRequest
from broadsoft.requestobjects.GroupAccessDeviceDeleteRequest import GroupAccessDeviceDeleteRequest


def fake_phone_db_record():
    class FakeDbPhone:
        def __init__(self):
            self.did = '6175551212'
            self.description = 'beaverphone'
            self.phone_type = 'batphone'
            self.hwaddr = 'aabbcc112233'
            self.active = 'Y'
            self.line_port = 'lp@mit.edu'

    return FakeDbPhone()


def fake_users_db_record():
    class FakeDbUser:
        def __init__(self):
            self.did = '6175551212'
            self.display_name = 'Tim Beaver'
            self.password = '123456'

    return FakeDbUser()

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


def list_users_mock(*args, **kwargs):
    xml = """<?xml version="1.0" encoding="ISO-8859-1"?>
            <BroadsoftDocument protocol="OCI" xmlns="C" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
                <sessionId xmlns="">Chriss-MacBook-Pro-4.local,2017-06-12 20:29:56.190885,9387725444</sessionId>
                <command echo="" xsi:type="UserGetListInGroupResponse" xmlns="">
                    <userTable>
                        <colHeading>User Id</colHeading>
                        <colHeading>Last Name</colHeading>
                        <colHeading>First Name</colHeading>
                        <colHeading>Department</colHeading>
                        <colHeading>Phone Number</colHeading>
                        <colHeading>Phone Number Activated</colHeading>
                        <colHeading>Email Address</colHeading>
                        <colHeading>Hiragana Last Name</colHeading>
                        <colHeading>Hiragana First Name</colHeading>
                        <colHeading>In Trunk Group</colHeading>
                        <colHeading>Extension</colHeading>
                        <colHeading>Country Code</colHeading>
                        <colHeading>National Prefix</colHeading>
                        <row>
                            <col>6175551212@broadsoft.mit.edu</col>
                            <col>Beaver</col>
                            <col>Tim</col>
                            <col/>
                            <col>+1-6175551212</col>
                            <col>true</col>
                            <col>beaver@mit.edu</col>
                            <col>Beaver</col>
                            <col>Tim</col>
                            <col>false</col>
                            <col>1212</col>
                            <col>1</col>
                            <col/>
                        </row>
                    </userTable>
                </command>
            </BroadsoftDocument>"""
    return ET.fromstring(xml)


def return_empty_array(*args, **kwargs):
    return []


def return_none(*args, **kwargs):
    return None


def roles_mock(*args, **kwargs):
    return ['beaver']


class TestBroadsoftAccount(unittest.TestCase):
    def test_account_attrs_get_passed_to_request_object(self):
        a = Account(did=6175551212, extension=51212, last_name='beaver', first_name='tim',
                    sip_user_id='beaver@broadsoft.mit.edu', kname='beaver', email='beaver@mit.edu',
                    sip_password='password', broadsoftinstance=BroadsoftInstance.factory())
        ro = a.build_provision_request()
        uadd = ro.commands[0]
        self.assertEqual(a.did, uadd.did)
        self.assertEqual(a.last_name, uadd.last_name)
        self.assertEqual(a.first_name, uadd.first_name)
        self.assertEqual(a.sip_user_id, uadd.sip_user_id)
        self.assertEqual(a.kname, uadd.kname)
        self.assertEqual(a.email, uadd.email)
        self.assertEqual(a.sip_password, uadd.sip_password)

    def test_devices_added_get_built_into_request_object(self):
        d1 = Device(description='beaver phone 1', name='beaverphone1', type='iphone', line_port='lp1')
        d2 = Device(description='beaver phone 2', name='beaverphone2', type='hamburger', line_port='lp2')
        a = Account(did=6175551212, extension=51212, last_name='beaver', first_name='tim',
                    sip_user_id='beaver@broadsoft.mit.edu', kname='beaver', email='beaver@mit.edu',
                    use_test=True, services=['a'])
        a.devices = [d1, d2]
        ro = a.build_provision_request()

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
        b = BroadsoftRequest()
        a = Account(did=6175551212)
        d1 = Device(description='beaver phone 1', name='beaverphone1', type='iphone', use_test=False)
        a.link_primary_device(req_object=b, device=d1)
        self.assertEqual(1, len(b.commands))
        cmd = b.commands[0]
        self.assertIsInstance(cmd, UserModifyRequest)
        self.assertEqual(cmd.did, str(a.did))
        self.assertEqual(cmd.sip_user_id, str(a.did) + '@' + a.broadsoftinstance.default_domain)
        self.assertEqual(cmd.device_name, d1.name)

    def test_link_sca_device(self):
        a = Account(did=6175551212)
        b = BroadsoftRequest()
        d1 = Device(description='beaver phone 1', name='beaverphone1', type='iphone', use_test=False)
        a.link_sca_device(req_object=b, device=d1)
        self.assertEqual(1, len(b.commands))
        cmd = b.commands[0]
        self.assertIsInstance(cmd, UserSharedCallAppearanceAddEndpointRequest)
        self.assertEqual(cmd.sip_user_id, str(a.did) + '@' + a.broadsoftinstance.default_domain)
        self.assertEqual(cmd.device_name, d1.name)

    def test_add_devices(self):
        a = Account(did=6175551212)
        b = BroadsoftRequest()
        d1 = Device(description='beaver phone 1', name='beaverphone1', type='iphone', use_test=False, line_port='lp1')
        d2 = Device(description='beaver phone 2', name='beaverphone2', type='cisco', use_test=False, line_port='lp2')
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

    @unittest.mock.patch.object(Account, 'load_devices')
    def test_xml_converted_to_elementtree_at_from_xml(self, load_devices_patch):
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

    @unittest.mock.patch.object(Account, 'load_devices')
    def test_from_xml_blanks_out_devices(self, load_devices_patch):
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

    @unittest.mock.patch.object(BroadsoftRequest, 'convert_results_table')
    @unittest.mock.patch('broadsoft.requestobjects.UserSharedCallAppearanceGetRequest.UserSharedCallAppearanceGetRequest.get_devices')
    @unittest.mock.patch.object(Device, 'fetch')
    @unittest.mock.patch.object(Account, 'fetch')
    def test_load_devices_should_call_fetch_when_necessary(
            self, account_fetch_patch, device_account_patch, get_scas_patch, convert_results_patch
    ):
        # no xml in Account? fetch.
        a = Account(did=6175551212)
        account_fetch_patch.called = False
        a.load_devices()
        self.assertTrue(account_fetch_patch.called)

        # xml in Account? don't fetch.
        a = Account(did=6175551212)
        xml = """
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
        a.xml = ET.fromstring(xml)
        account_fetch_patch.called = False
        a.load_devices()
        self.assertFalse(account_fetch_patch.called)

    @unittest.mock.patch('broadsoft.requestobjects.UserGetRequest.UserGetRequest.get_user')
    @unittest.mock.patch.object(Account, 'from_xml')
    def test_fetch(
            self, load_devices_patch, get_user_patch
    ):
        a = Account(did=6175551212, sip_user_id='6175551212@mit.edu')
        a.fetch()
        call = get_user_patch.call_args_list[0]
        args, kwargs = call
        self.assertEqual(a.sip_user_id, kwargs['sip_user_id'])

    @unittest.mock.patch.object(Device, 'fetch')
    @unittest.mock.patch(
        'broadsoft.requestobjects.UserSharedCallAppearanceGetRequest.UserSharedCallAppearanceGetRequest.get_devices',
        side_effect=get_sca_mock)
    def test_from_xml(
            self, get_devices_patch, device_fetch_patch
    ):
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
        # per what we've mocked, expect three devices: one primary, two shared call appearances
        self.assertEqual(3, len(a.devices))

        d = a.devices[0]
        self.assertTrue(d.is_primary)
        self.assertEqual('beaver550', d.name)

        d = a.devices[1]
        self.assertFalse(d.is_primary)
        self.assertEqual('beavervvx', d.name)

        d = a.devices[2]
        self.assertFalse(d.is_primary)
        self.assertEqual('beaverspa', d.name)

    def test_set_portal_password_requires_did_or_sip_user_id(self):
        a = Account()
        a.sip_password = 'password'
        with self.assertRaises(AttributeError):
            a.set_portal_password()

    @unittest.mock.patch.object(UserModifyRequest, 'set_password')
    def test_set_portal_password_pass_in_value(
            self, umr_set_password_patch
    ):
        # passed in init args, not passed in set_password call
        a = Account(did=6175551212, sip_password='password1')
        a.set_portal_password()
        call = umr_set_password_patch.call_args_list[0]
        args, kwargs = call
        self.assertEqual('password1', kwargs['new_password'])

        # not passed in init args, passed in set_password call
        a = Account(did=6175551212)
        a.set_portal_password(sip_password='password2')
        call = umr_set_password_patch.call_args_list[1]
        args, kwargs = call
        self.assertEqual('password2', kwargs['new_password'])

        # passed in init args, also passed in set_password call
        # expect password passed in set_password to win AND overwrite a.sip_password
        a = Account(did=6175551212, sip_password='password1')
        a.set_portal_password(sip_password='password2')
        call = umr_set_password_patch.call_args_list[2]
        args, kwargs = call
        self.assertEqual('password2', kwargs['new_password'])
        self.assertEqual('password2', a.sip_password)

        # never passed
        a = Account(did=6175551212)
        with self.assertRaises(AttributeError):
            a.set_portal_password()

    @unittest.mock.patch.object(Account, 'load_devices')
    @unittest.mock.patch.object(Device, 'set_password')
    def test_set_device_passwords_requires_sip_user_password(
            self, set_device_password_patch, load_devices_patch
    ):
        a = Account(did=6175551212)
        with self.assertRaises(ValueError):
            a.set_device_passwords()

    @unittest.mock.patch.object(Device, 'set_password')
    def test_set_device_passwords_passing_password(
            self, set_device_password_patch
    ):
        d1 = Device()
        d2 = Device()

        # passing via set_devices_passwords
        a = Account(did=6175551212)
        a.devices = [d1, d2]
        a.set_device_passwords(new_sip_password='newpassword')
        call = set_device_password_patch.call_args_list[0]
        args, kwargs = call
        self.assertEqual('newpassword', kwargs['sip_password'])

        # passing via __init__
        a = Account(did=6175551212, sip_password='oldpassword')
        a.devices = [d1, d2]
        a.set_device_passwords()
        call = set_device_password_patch.call_args_list[2]
        args, kwargs = call
        self.assertEqual('oldpassword', kwargs['sip_password'])

        # passing via both, set_devices_password one should win
        a = Account(did=6175551212, sip_password='oldpassword')
        a.devices = [d1, d2]
        a.set_device_passwords(new_sip_password='newpassword')
        call = set_device_password_patch.call_args_list[4]
        args, kwargs = call
        self.assertEqual('newpassword', kwargs['sip_password'])

    @unittest.mock.patch.object(Device, 'set_password')
    def test_set_device_passwords_calls_set_password_for_each_device(
            self, set_device_password_patch
    ):

        d1 = Device()
        d2 = Device()

        # one device
        a = Account(did=6175551212)
        a.devices = [d1]
        a.set_device_passwords(new_sip_password='newpassword')
        self.assertEqual(1, len(set_device_password_patch.call_args_list))

        # two devices (call count should have increased by 2)
        a = Account(did=6175551212)
        a.devices = [d1, d2]
        a.set_device_passwords(new_sip_password='newpassword')
        self.assertEqual(3, len(set_device_password_patch.call_args_list))

    @unittest.mock.patch.object(Account, 'load_devices')
    @unittest.mock.patch.object(Device, 'set_password')
    def test_set_device_passwords_calls_load_devices_when_none_present(
            self, set_device_password_patch, load_devices_patch
    ):
        d1 = Device()

        # no devices, should call load_devices
        a = Account(did=6175551212)
        a.set_device_passwords(new_sip_password='newpassword')
        self.assertTrue(load_devices_patch.called)
        load_devices_patch.called = False

        # devices present, should not call load_devices
        a = Account(did=6175551212)
        a.devices = [d1]
        a.set_device_passwords(new_sip_password='newpassword')
        self.assertFalse(load_devices_patch.called)

    @unittest.mock.patch.object(Account, 'set_device_passwords')
    @unittest.mock.patch.object(BroadsoftObject, 'provision')
    @unittest.mock.patch.object(BroadsoftRequest, 'post')
    def test_provision_handles_sip_password(
            self, post_patch, provision_patch, set_device_passwords_patch
    ):
        d1 = Device(name='d1name')
        d2 = Device(name='d2name')

        # when there is a sip_password, should call set_device_passwords
        # not testing alternate case, because right now ALWAYS a sip_password when provisioning
        a = Account(did=6175551212, last_name='beaver', first_name='tim', sip_password='password',
                    email='beaver@mit.edu')
        a.devices = [d1, d2]
        a.provision()
        self.assertTrue(set_device_passwords_patch.called)

    @unittest.mock.patch.object(Account, 'set_device_passwords')
    @unittest.mock.patch.object(BroadsoftObject, 'provision')
    @unittest.mock.patch.object(BroadsoftRequest, 'post')
    def test_sets_password_implicitly_on_provision_when_required(
            self, post_patch, provision_patch, set_device_passwords_patch
    ):
        # when no sip_password
        a = Account(did=6175551212, last_name='beaver', first_name='tim', email='beaver@mit.edu')
        a.provision()
        self.assertIsNotNone(a.sip_password)

        # when is sip_password
        a = Account(did=6175551212, last_name='beaver', first_name='tim', sip_password='password', email='beaver@mit.edu')
        a.provision()
        self.assertEqual('password', a.sip_password)

    def test_default_services(self):
        self.assertEqual(3, len(Account.default_services))
        self.assertIn('Shared Call Appearance 10', Account.default_services)
        self.assertIn('Third-Party Voice Mail Support', Account.default_services)
        self.assertIn('Voice Messaging User', Account.default_services)

    def test_account_converts_did_at_init(self):
        a = Account(did=6175551212)
        self.assertEqual('6175551212', a.did)

        a = Account(did='617 555 1212')
        self.assertEqual('6175551212', a.did)

    @unittest.mock.patch.object(Account, 'set_device_passwords')
    @unittest.mock.patch.object(BroadsoftObject, 'provision')
    @unittest.mock.patch.object(BroadsoftRequest, 'post')
    def test_account_converts_did_at_provision(
            self, post_patch, provision_patch, set_device_passwords_patch
    ):
        a = Account(email='beaver@mit.edu')
        a.did = 6175551212
        a.provision()
        self.assertEqual('6175551212', a.did)

        a = Account(email='beaver@mit.edu')
        a.did = '617 555 1212'
        a.provision()
        self.assertEqual('6175551212', a.did)

    def test_account_derives_sip_user_id_at_init(self):
        a = Account(did=6175551212)
        self.assertEqual('6175551212@' + a.broadsoftinstance.default_domain, a.sip_user_id)

    @unittest.mock.patch.object(Account, 'set_device_passwords')
    @unittest.mock.patch.object(BroadsoftObject, 'provision')
    @unittest.mock.patch.object(BroadsoftRequest, 'post')
    def test_account_derives_sip_user_id_at_provision(
            self, post_patch, provision_patch, set_device_passwords_patch
    ):
        a = Account(email='beaver@mit.edu')
        a.did = 6175551212
        a.provision()
        self.assertEqual('6175551212@' + a.broadsoftinstance.default_domain, a.sip_user_id)

        a = Account(email='beaver@mit.edu')
        a.did = '617 555 1212'
        a.provision()
        self.assertEqual('6175551212@' + a.broadsoftinstance.default_domain, a.sip_user_id)

    def test_inject_broadsoftinstance(self):
        prod_i = BroadsoftInstance.factory()
        test_i = BroadsoftInstance.factory(use_test=True)

        # using prod instance (device has none)
        d = Device(name='dname')
        a = Account(broadsoftinstance=prod_i)
        a.inject_broadsoftinstance(child=d)
        self.assertIsInstance(d.broadsoftinstance, BroadsoftInstance.BroadsoftInstance)

        # using test instance (device has none)
        d = Device(name='dname')
        a = Account(broadsoftinstance=test_i)
        a.inject_broadsoftinstance(child=d)
        self.assertIsInstance(d.broadsoftinstance, BroadsoftInstance.TestBroadsoftInstance)

        # using prod instance (device has test)
        d = Device(name='dname', broadsoftinstance=test_i)
        a = Account(broadsoftinstance=prod_i)
        a.inject_broadsoftinstance(child=d)
        self.assertIsInstance(d.broadsoftinstance, BroadsoftInstance.BroadsoftInstance)

        # using test instance (device has prod)
        d = Device(name='dname', broadsoftinstance=prod_i)
        a = Account(broadsoftinstance=test_i)
        a.inject_broadsoftinstance(child=d)
        self.assertIsInstance(d.broadsoftinstance, BroadsoftInstance.TestBroadsoftInstance)

        # using none (device has test)
        d = Device(name='dname', broadsoftinstance=test_i)
        a = Account()
        a.broadsoftinstance = None
        a.inject_broadsoftinstance(child=d)
        self.assertIsInstance(d.broadsoftinstance, BroadsoftInstance.TestBroadsoftInstance)

        # using none (device has prod)
        d = Device(name='dname', broadsoftinstance=prod_i)
        a = Account()
        a.broadsoftinstance = None
        a.inject_broadsoftinstance(child=d)
        self.assertIsInstance(d.broadsoftinstance, BroadsoftInstance.BroadsoftInstance)

    @unittest.mock.patch.object(Account, 'inject_broadsoftinstance')
    @unittest.mock.patch.object(Account, 'link_sca_device')
    @unittest.mock.patch.object(Account, 'link_primary_device')
    @unittest.mock.patch.object(Account, 'build_provision_request')
    def test_add_devices_injects_broadsoftinstance_once_per_device(
            self, build_provision_request_patch, link_primary_device_patch, link_sca_device_patch,
            inject_broadsoftinstance_patch
    ):
        d1 = Device(name='dname1', line_port='lp1')
        d2 = Device(name='dname2', line_port='lp2')
        a = Account(broadsoftinstance=BroadsoftInstance.factory())
        a.devices = [d1, d2]
        a.add_devices(req_object=BroadsoftRequest())

        self.assertTrue(inject_broadsoftinstance_patch.called)
        self.assertEqual(2, len(inject_broadsoftinstance_patch.call_args_list))

        call = inject_broadsoftinstance_patch.call_args_list[0]
        args, kwargs = call
        self.assertEqual(d1.name, kwargs['child'].name)
        self.assertIsInstance(kwargs['child'], Device)

        call = inject_broadsoftinstance_patch.call_args_list[1]
        args, kwargs = call
        self.assertEqual(d2.name, kwargs['child'].name)
        self.assertIsInstance(kwargs['child'], Device)

    @unittest.mock.patch.object(BroadsoftObject, 'inject_broadsoftinstance')
    def test_add_services_injects_broadsoftinstance(
            self, inject_broadsoftinstance_patch
    ):
        from broadsoft.requestobjects.UserServiceAssignListRequest import UserServiceAssignListRequest
        a = Account(broadsoftinstance=BroadsoftInstance.factory())
        a.services = ['a', 'b', 'c']
        a.add_services(req_object=BroadsoftRequest())
        self.assertTrue(inject_broadsoftinstance_patch.called)
        self.assertEqual(1, len(inject_broadsoftinstance_patch.call_args_list))

        call = inject_broadsoftinstance_patch.call_args_list[0]
        args, kwargs = call
        self.assertIsInstance(kwargs['child'], UserServiceAssignListRequest)

    @unittest.mock.patch.object(Account, 'add_devices')
    @unittest.mock.patch.object(Account, 'add_services')
    @unittest.mock.patch.object(BroadsoftObject, 'inject_broadsoftinstance')
    def test_build_provision_request_injects_broadsoftinstance(
            self, inject_broadsoftinstance_patch, add_services_patch, add_devices_patch
    ):
        a = Account(broadsoftinstance=BroadsoftInstance.factory())
        a.build_provision_request()
        self.assertTrue(inject_broadsoftinstance_patch.called)
        self.assertEqual(2, len(inject_broadsoftinstance_patch.call_args_list))

        call = inject_broadsoftinstance_patch.call_args_list[0]
        args, kwargs = call
        self.assertIsInstance(kwargs['child'], BroadsoftRequest)

        call = inject_broadsoftinstance_patch.call_args_list[1]
        args, kwargs = call
        self.assertIsInstance(kwargs['child'], UserAddRequest)

    @unittest.mock.patch('broadsoft.requestobjects.UserGetRequest.UserGetRequest.get_user')
    @unittest.mock.patch.object(Account, 'from_xml')
    def fetch_passes_broadsoftinstance(
            self, from_xml_patch, get_user_patch
    ):
        bi = BroadsoftInstance.factory()
        a = Account(did=6175551212, broadsoftinstance=bi)
        a.fetch()

        call = get_user_patch.call_args_list[0]
        args, kwargs = call
        self.assertIsInstance(kwargs['broadsoftinstance'], BroadsoftInstance.BroadsoftInstance)

    @unittest.mock.patch.object(BroadsoftObject, 'inject_broadsoftinstance')
    def test_link_primary_device_injects_broadsoftinstance(
            self, inject_broadsoftinstance_patch
    ):
        d1 = Device(name='dname1')
        a = Account(broadsoftinstance=BroadsoftInstance.factory())
        a.link_primary_device(req_object=BroadsoftRequest(), device=d1)

        self.assertTrue(inject_broadsoftinstance_patch.called)
        self.assertEqual(1, len(inject_broadsoftinstance_patch.call_args_list))

        call = inject_broadsoftinstance_patch.call_args_list[0]
        args, kwargs = call
        self.assertIsInstance(kwargs['child'], UserModifyRequest)

    @unittest.mock.patch.object(BroadsoftObject, 'inject_broadsoftinstance')
    def test_link_sca_device_injects_broadsoftinstance(
            self, inject_broadsoftinstance_patch
    ):
        d1 = Device(name='dname1')
        a = Account(broadsoftinstance=BroadsoftInstance.factory())
        a.link_sca_device(req_object=BroadsoftRequest(), device=d1)

        self.assertTrue(inject_broadsoftinstance_patch.called)
        self.assertEqual(1, len(inject_broadsoftinstance_patch.call_args_list))

        call = inject_broadsoftinstance_patch.call_args_list[0]
        args, kwargs = call
        self.assertIsInstance(kwargs['child'], UserSharedCallAppearanceAddEndpointRequest)

    @unittest.mock.patch(
        'broadsoft.requestobjects.UserSharedCallAppearanceGetRequest.UserSharedCallAppearanceGetRequest.get_devices',
        side_effect=get_sca_mock
    )
    @unittest.mock.patch.object(Device, 'bootstrap_access_device_endpoint')
    @unittest.mock.patch.object(Device, 'bootstrap_shared_call_appearance')
    @unittest.mock.patch.object(Device, 'fetch')
    @unittest.mock.patch.object(BroadsoftObject, 'inject_broadsoftinstance')
    def test_load_devices_injects_broadsoftinstance(
            self, inject_broadsoftinstance_patch, device_fetch_patch, device_bootstrap_sca_patch,
            device_bootstrap_ade_patch, get_scas_patch
    ):
        xml = """<?xml version="1.0" encoding="ISO-8859-1"?>
            <BroadsoftDocument protocol="OCI" xmlns="C" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
            <sessionId xmlns="">192.168.0.100,1743299062,1496154334750</sessionId>
            <command echo="" xsi:type="UserGetResponse21" xmlns="">
                <accessDeviceEndpoint>
                    <blah>1</blah>
                </accessDeviceEndpoint>
                <accessDeviceEndpoint>
                    <blah>2</blah>
                </accessDeviceEndpoint>
            </command>
            </BroadsoftDocument>"""
        xml = ET.fromstring(xml)

        a = Account(broadsoftinstance=BroadsoftInstance.factory())
        a.xml = xml
        a.load_devices()

        # expect to see 4 calls to inject_broadsoftinstance_patch
        self.assertTrue(inject_broadsoftinstance_patch.called)
        self.assertEqual(4, len(inject_broadsoftinstance_patch.call_args_list))
        # * 2 for the faked accessDeviceEndpoint results in a.xml
        call = inject_broadsoftinstance_patch.call_args_list[0]
        args, kwargs = call
        self.assertIsInstance(kwargs['child'], Device)

        call = inject_broadsoftinstance_patch.call_args_list[1]
        args, kwargs = call
        self.assertIsInstance(kwargs['child'], Device)

        # * 2 for the faked rows in UserSharedCallAppearanceGetRequest.get_devices
        call = inject_broadsoftinstance_patch.call_args_list[2]
        args, kwargs = call
        self.assertIsInstance(kwargs['child'], Device)

        call = inject_broadsoftinstance_patch.call_args_list[3]
        args, kwargs = call
        self.assertIsInstance(kwargs['child'], Device)

        # furthermore, when we call UserSharedCallAppearanceGetRequest.get_devices should pass the instance
        call = get_scas_patch.call_args_list[0]
        args, kwargs = call
        self.assertIsInstance(kwargs['broadsoftinstance'], BroadsoftInstance.BroadsoftInstance)

    @unittest.mock.patch.object(Device, 'set_password')
    @unittest.mock.patch.object(BroadsoftObject, 'inject_broadsoftinstance')
    def test_set_device_passwords_injects_broadsoftinstance(
            self, inject_broadsoftinstance_patch, device_set_password_patch
    ):
        d1 = Device(name='dname1')
        d2 = Device(name='dname2')
        a = Account(broadsoftinstance=BroadsoftInstance.factory(), did=6175551212)
        a.devices = [d1, d2]
        a.set_device_passwords(new_sip_password='pw')

        self.assertTrue(inject_broadsoftinstance_patch.called)
        self.assertEqual(2, len(inject_broadsoftinstance_patch.call_args_list))

        call = inject_broadsoftinstance_patch.call_args_list[0]
        args, kwargs = call
        self.assertEqual(d1.name, kwargs['child'].name)
        self.assertIsInstance(kwargs['child'], Device)

        call = inject_broadsoftinstance_patch.call_args_list[1]
        args, kwargs = call
        self.assertEqual(d2.name, kwargs['child'].name)
        self.assertIsInstance(kwargs['child'], Device)

    @unittest.mock.patch.object(UserModifyRequest, 'set_password')
    def test_set_portal_password_passes_broadsoftinstance(
            self, set_password_patch
    ):
        a = Account(broadsoftinstance=BroadsoftInstance.factory(), did=6175551212)
        a.set_portal_password(sip_password='pw')

        call = set_password_patch.call_args_list[0]
        args, kwargs = call
        self.assertIsInstance(kwargs['broadsoftinstance'], BroadsoftInstance.BroadsoftInstance)

    @unittest.mock.patch.object(UserModifyRequest, '__init__', side_effect=return_none)
    def test_link_primary_device_post_call(
            self, umr_init_patch
    ):
        d = Device(name='dname', line_port='lp')
        a = Account(did=6175551212, sip_user_id='6175551212@broadsoft.mit.edu')
        a.link_primary_device(req_object=BroadsoftRequest(), device=d)

        call = umr_init_patch.call_args_list[0]
        args, kwargs = call
        self.assertEqual(kwargs['did'], a.did)
        self.assertEqual(kwargs['sip_user_id'], a.sip_user_id)
        self.assertEqual(kwargs['device_name'], d.name)
        self.assertEqual(kwargs['line_port'], d.line_port)

    @unittest.mock.patch.object(UserSharedCallAppearanceAddEndpointRequest, '__init__', side_effect=return_none)
    def test_link_sca_device_post_call(
            self, usca_init_patch
    ):
        d = Device(name='dname', line_port='lp')
        a = Account(did=6175551212, sip_user_id='6175551212@broadsoft.mit.edu')
        a.link_sca_device(req_object=BroadsoftRequest(), device=d)

        call = usca_init_patch.call_args_list[0]
        args, kwargs = call
        self.assertEqual(kwargs['sip_user_id'], a.sip_user_id)
        self.assertEqual(kwargs['device_name'], d.name)
        self.assertEqual(kwargs['line_port'], d.line_port)

    def test_barf_if_try_to_add_device_missing_lineport(self):
        d1 = Device(name='d1', line_port='d1_lp')
        d2 = Device(name='d2')
        d2.line_port = None
        a = Account(did=6175551212)
        a.devices = [d1, d2]

        with self.assertRaises(RuntimeError):
            a.add_devices(req_object=BroadsoftRequest())

    @unittest.mock.patch('broadsoft.requestobjects.UserThirdPartyVoiceMailSupportModifyRequest.UserThirdPartyVoiceMailSupportModifyRequest.deactivate_unity_voicemail')
    def test_deactivate_unity_voicemail_passes_broadsoftinstance(
            self, deactivate_unity_voicemail_patch
    ):
        a = Account(sip_user_id='6175551212@mit.edu')
        a.deactivate_unity_voicemail()
        call = deactivate_unity_voicemail_patch.call_args_list[0]
        args, kwargs = call
        self.assertIsInstance(kwargs['broadsoftinstance'], BroadsoftInstance.BroadsoftInstance)

    def test_deactivate_unity_voicemail_barfs_when_no_user_id(self):
        a = Account()
        a.sip_user_id = None
        with self.assertRaises(ValueError):
            a.deactivate_unity_voicemail()

    def test_deactivate_voicemail_barfs_when_no_user_id(self):
        a = Account()
        a.sip_user_id = None
        with self.assertRaises(ValueError):
            a.deactivate_broadsoft_voicemail()

    @unittest.mock.patch(
        'broadsoft.requestobjects.UserVoiceMessagingUserModifyVoiceManagementRequest.UserVoiceMessagingUserModifyVoiceManagementRequest.deactivate_broadsoft_voicemail')
    def test_deactivate_broadsoft_voicemail_passes_broadsoftinstance(
            self, deactivate_broadsoft_voicemail_patch
    ):
        a = Account(sip_user_id='6175551212@mit.edu')
        a.deactivate_broadsoft_voicemail()
        call = deactivate_broadsoft_voicemail_patch.call_args_list[0]
        args, kwargs = call
        self.assertIsInstance(kwargs['broadsoftinstance'], BroadsoftInstance.BroadsoftInstance)

    @unittest.mock.patch.object(BroadsoftObject, 'inject_broadsoftinstance')
    @unittest.mock.patch.object(BroadsoftRequest, 'post')
    def test_activate_voicemail_passes_broadsoftinstance(
            self, post_patch, inject_broadsoftinstance_patch
    ):
        i = BroadsoftInstance.factory(use_test=True)
        a = Account(sip_user_id='6175551212@mit.edu', email='beaver@mit.edu', broadsoftinstance=i)
        a.activate_voicemail()

        # expect to see inject_broadsoftinstance_patch called once, for the BroadsoftRequest object that's containing
        # our activate and deactivate calls
        self.assertTrue(inject_broadsoftinstance_patch.called)
        self.assertEqual(1, inject_broadsoftinstance_patch.called)
        call = inject_broadsoftinstance_patch.call_args_list[0]
        args, kwargs = call
        self.assertIsInstance(kwargs['child'], BroadsoftRequest)

    def test_email_derived_from_kname(self):
        a = Account(sip_user_id='6175551212@mit.edu', kname='beaver')
        self.assertEqual('beaver@mit.edu', a.email)

    def test_activate_voicemail_barfs_without_email(self):
        a = Account(sip_user_id='6175551212@mit.edu')
        with self.assertRaises(ValueError):
            a.activate_voicemail()

    @unittest.mock.patch.object(BroadsoftRequest, 'post')
    def test_activate_voicemail_pass_voicemail_object(
            self, post_patch
    ):
        v = Voicemail(straight_to_voicemail=True, type='broadsoft')
        a = Account(sip_user_id='6175551212@broadsoft.com', email='beaver@mit.edu')
        r = a.activate_voicemail(voicemail_object=v)

        # the first command in the returned object from activate_voicemail will
        request = r[0]
        activate = request.commands[0]
        # default object has always_redirect_to_voice_mail set to False. If our custom voicemail object was passed,
        # will be true.
        self.assertTrue(activate.always_redirect_to_voice_mail)

    @unittest.mock.patch.object(BroadsoftRequest, 'post')
    def test_activate_voicemail_construct_voicemail_object(
            self, post_patch
    ):
        a = Account(sip_user_id='6175551212@broadsoft.com', email='beaver@mit.edu')
        r = a.activate_voicemail()

        # the first command in the returned object from activate_voicemail will
        request = r[0]
        activate = request.commands[0]
        # default object has always_redirect_to_voice_mail set to True.
        self.assertFalse(activate.always_redirect_to_voice_mail)

    @unittest.mock.patch.object(BroadsoftRequest, 'post')
    def test_activate_voicemail_commands_built(
            self, post_patch
    ):
        # build default (broadsoft)
        a = Account(sip_user_id='6175551212@broadsoft.com', email='beaver@mit.edu')
        r = a.activate_voicemail()

        # expect to see two commands: an activate, and a deactivate
        request = r[0]
        activate = request.commands[0]
        deactivate = request.commands[1]

        # default is broadsoft, so activate should be for broadsoft, and deactivate for third party
        self.assertIsInstance(activate, UserVoiceMessagingUserModifyVoiceManagementRequest)
        self.assertIsInstance(deactivate, UserThirdPartyVoiceMailSupportModifyRequest)

        # build unity
        a = Account(sip_user_id='6175551212@broadsoft.com', email='beaver@mit.edu', voicemail='unity')
        r = a.activate_voicemail()

        # expect to see two commands: an activate, and a deactivate
        request = r[0]
        activate = request.commands[0]
        deactivate = request.commands[1]

        # asked for unity, so activate should be for thirdparty, and deactivate for broadsoft
        self.assertIsInstance(activate, UserThirdPartyVoiceMailSupportModifyRequest)
        self.assertIsInstance(deactivate, UserVoiceMessagingUserModifyVoiceManagementRequest)

    @unittest.mock.patch.object(BroadsoftRequest, 'post')
    def test_activate_voicemail_passes_relevant_attributes(self, post_patch):
        # with mwi True
        a = Account(sip_user_id='6175551212@broadsoft.com', email='beaver@mit.edu', voicemail_mwi=True)
        [request] = a.activate_voicemail()

        # check activate command for email, sip_user_id, and mwi
        activate = request.commands[0]
        self.assertEqual(activate.voice_message_delivery_email_address, a.email)
        self.assertEqual(activate.voice_message_notify_email_address, a.email)
        self.assertEqual(activate.send_voice_message_notify_email, a.email)
        self.assertEqual(activate.sip_user_id, a.sip_user_id)
        self.assertTrue(activate.use_phone_message_waiting_indicator)

        # with mwi False
        a = Account(sip_user_id='6175551212@broadsoft.com', email='beaver@mit.edu', voicemail_mwi=False)
        [request] = a.activate_voicemail()

        # check activate command for email, sip_user_id, and mwi
        activate = request.commands[0]
        self.assertEqual(activate.voice_message_delivery_email_address, a.email)
        self.assertEqual(activate.voice_message_notify_email_address, a.email)
        self.assertEqual(activate.send_voice_message_notify_email, a.email)
        self.assertEqual(activate.sip_user_id, a.sip_user_id)
        self.assertFalse(activate.use_phone_message_waiting_indicator)

    @unittest.mock.patch.object(BroadsoftRequest, 'post')
    def test_delete_converts_did_to_sip_user_id(
            self, post_patch
    ):
        a = Account(did='617-555-1212')
        requests = a.delete()
        request = requests[0]
        cmd = request.commands[0]

        self.assertEqual('6175551212@' + a.broadsoftinstance.default_domain, cmd.sip_user_id)

    @unittest.mock.patch.object(BroadsoftRequest, 'post')
    def test_delete_barfs_when_no_sip_user_id(
            self, post_patch
    ):
        a = Account()
        with self.assertRaises(ValueError):
            requests = a.delete()

    @unittest.mock.patch.object(BroadsoftObject, 'inject_broadsoftinstance')
    @unittest.mock.patch.object(BroadsoftRequest, 'post')
    def test_delete_injects_broadsoftinstance(
            self, post_patch, inject_patch
    ):
        i = BroadsoftInstance.factory(use_test=True)
        a = Account(sip_user_id='6175551212@mit.edu', broadsoftinstance=i)
        a.delete()

        self.assertTrue(inject_patch.called)

    @unittest.mock.patch.object(BroadsoftRequest, 'post')
    def test_delete_should_allow_delete_devices(
            self, post_patch
    ):
        d1 = Device(name='dname1')
        d2 = Device(name='dname2')
        a = Account(sip_user_id='6175551212@mit.edu')
        a.devices = [d1, d2]
        requests = a.delete(delete_devices=True)
        request = requests[0]

        # expect to see three commands in the request, the latter two for the devices
        self.assertEqual(3, len(request.commands))

        delete_device_1 = request.commands[1]
        self.assertIsInstance(delete_device_1, GroupAccessDeviceDeleteRequest)
        self.assertEqual('dname1', delete_device_1.device_name)

        delete_device_2 = request.commands[2]
        self.assertIsInstance(delete_device_2, GroupAccessDeviceDeleteRequest)
        self.assertEqual('dname2', delete_device_2.device_name)

    @unittest.mock.patch.object(Account, 'load_devices', side_effect=return_empty_array)
    @unittest.mock.patch.object(BroadsoftRequest, 'post')
    def test_delete_does_not_barf_when_no_devices_found(
            self, post_patch, load_devices_patch
    ):
        a = Account(sip_user_id='6175551212@mit.edu')
        requests = a.delete(delete_devices=True)
        request = requests[0]

        # expect to see 1 commands in the request, since no devices
        self.assertEqual(1, len(request.commands))

    @unittest.mock.patch.object(Account, 'load_devices')
    @unittest.mock.patch.object(BroadsoftRequest, 'post')
    def test_delete_should_fetch_devices_when_necessary(
            self, post_patch, load_devices_patch
    ):
        # devices are present, and delete_devices is True: shouldn't load
        d1 = Device(name='dname1')
        d2 = Device(name='dname2')
        a = Account(sip_user_id='6175551212@mit.edu')
        a.devices = [d1, d2]
        a.delete(delete_devices=True)
        self.assertFalse(load_devices_patch.called)

        # devices are present, and delete_devices is False: shouldn't load
        d1 = Device(name='dname1')
        d2 = Device(name='dname2')
        a = Account(sip_user_id='6175551212@mit.edu')
        a.devices = [d1, d2]
        a.delete(delete_devices=True)
        self.assertFalse(load_devices_patch.called)

        # devices are not present, and delete_devices is False: shouldn't load
        a = Account(sip_user_id='6175551212@mit.edu')
        a.delete(delete_devices=False)
        self.assertFalse(load_devices_patch.called)

        # devices are not present, and delete_devices is True: should load
        a = Account(sip_user_id='6175551212@mit.edu')
        a.delete(delete_devices=True)
        self.assertTrue(load_devices_patch.called)

    @unittest.mock.patch('broadsoft.requestobjects.UserGetListInGroupRequest.UserGetListInGroupRequest.post', side_effect=list_users_mock)
    def test_get_accounts_results(self, post_patch):
        accounts = Account.get_accounts()
        self.assertEqual(1, len(accounts))

        a = accounts[0]
        self.assertEqual('6175551212@broadsoft.mit.edu', a.sip_user_id)
        self.assertEqual('Beaver', a.last_name)
        self.assertEqual('beaver@mit.edu', a.email)
        self.assertEqual('Beaver', a.last_name)
        self.assertEqual('6175551212', a.did)
        self.assertEqual('Tim', a.first_name)
        self.assertEqual('1212', a.extension)

    @unittest.mock.patch('broadsoft.requestobjects.UserGetListInGroupRequest.UserGetListInGroupRequest.list_users')
    def test_get_accounts_passes_broadsoftinstance_to_list_users(self, list_users_patch):
        i = BroadsoftInstance.factory(use_test=True)
        Account.get_accounts(broadsoftinstance=i)
        call = list_users_patch.call_args_list[0]
        args, kwargs = call
        self.assertIsInstance(kwargs['broadsoftinstance'], BroadsoftInstance.TestBroadsoftInstance)

        i = BroadsoftInstance.factory(use_test=False)
        Account.get_accounts(broadsoftinstance=i)
        call = list_users_patch.call_args_list[0]
        args, kwargs = call
        self.assertIsInstance(kwargs['broadsoftinstance'], BroadsoftInstance.BroadsoftInstance)

    @unittest.mock.patch('broadsoft.requestobjects.UserGetListInGroupRequest.UserGetListInGroupRequest.post',
                         side_effect=list_users_mock)
    def test_get_accounts_passes_broadsoftinstance_to_results(self, post_patch):
        i = BroadsoftInstance.factory(use_test=True)
        accounts = Account.get_accounts(broadsoftinstance=i)
        for a in accounts:
            self.assertIsInstance(a.broadsoftinstance, BroadsoftInstance.TestBroadsoftInstance)

        i = BroadsoftInstance.factory(use_test=False)
        accounts = Account.get_accounts(broadsoftinstance=i)
        for a in accounts:
            self.assertIsInstance(a.broadsoftinstance, BroadsoftInstance.BroadsoftInstance)

    def test_split_name(self):
        self.assertEqual(('Tim', 'Beaver'), Account.split_name(name='Tim Beaver'))
        self.assertEqual(('Tim E.', 'Beaver'), Account.split_name(name='Tim E. Beaver'))

    @unittest.mock.patch('mitroles.MitRoles.MitRoles.get_owners_for_did', side_effect=roles_mock)
    @unittest.mock.patch.object(Account, 'provision')
    def test_thaw_from_db_passes_voicemail_mwi(self, account_provision_patch, roles_patch):
        u = fake_users_db_record()
        d = fake_phone_db_record()
        a = Account.thaw_from_db(user_record=u, device_records=[d], voicemail='broadsoft', voicemail_mwi=True)
        self.assertTrue(a.voicemail_mwi)

        a = Account.thaw_from_db(user_record=u, device_records=[d], voicemail='broadsoft', voicemail_mwi=False)
        self.assertFalse(a.voicemail_mwi)

    @unittest.mock.patch.object(BroadsoftRequest, 'post')
    def test_activate_passes_mwi(self, post_patch):
        a = Account(did=6175551212, email='beaver.mit.edu', voicemail_mwi=True)
        [request] = a.activate_voicemail()

        activate = request.commands[0]
        self.assertTrue(activate.use_phone_message_waiting_indicator)

        a = Account(did=6175551212, email='beaver.mit.edu', voicemail_mwi=False)
        [request] = a.activate_voicemail()

        activate = request.commands[0]
        self.assertFalse(activate.use_phone_message_waiting_indicator)

    @unittest.mock.patch('mitroles.MitRoles.MitRoles.get_owners_for_did', side_effect=roles_mock)
    @unittest.mock.patch.object(BroadsoftRequest, 'post')
    def test_thaw_from_db_passes_kwargs(self, post_patch, roles_patch):
        u = fake_users_db_record()
        d = fake_phone_db_record()

        # use_test (True and False)
        a = Account.thaw_from_db(user_record=u, device_records=[d], use_test=True)
        self.assertIsInstance(a.broadsoftinstance, BroadsoftInstance.TestBroadsoftInstance)

        a = Account.thaw_from_db(user_record=u, device_records=[d], use_test=False)
        self.assertIsInstance(a.broadsoftinstance, BroadsoftInstance.BroadsoftInstance)

        # broadsoft instance (test and prod)
        i = BroadsoftInstance.factory(use_test=True)
        a = Account.thaw_from_db(user_record=u, device_records=[d], broadsoftinstance=i)
        self.assertIsInstance(a.broadsoftinstance, BroadsoftInstance.TestBroadsoftInstance)

        i = BroadsoftInstance.factory(use_test=True)
        a = Account.thaw_from_db(user_record=u, device_records=[d], broadsoftinstance=i)
        self.assertIsInstance(a.broadsoftinstance, BroadsoftInstance.BroadsoftInstance)

    @unittest.mock.patch('mitroles.MitRoles.MitRoles.get_owners_for_did', side_effect=roles_mock)
    @unittest.mock.patch.object(BroadsoftRequest, 'post')
    def test_thaw_from_db_skips_inactive_devices(self, post_patch, roles_patch):
        u = fake_users_db_record()
        d1 = fake_phone_db_record()
        d2 = fake_phone_db_record()

        # update d1 and d2 to be different
        d1.description = 'd1'
        d2.description = 'd2'
        d1.active = 'N'

        a = Account.thaw_from_db(user_record=u, device_records=[d1, d2])
        # should only see d2 in devices
        self.assertEqual(1, len(a.devices))
        self.assertEqual('d2', a.devices[0].name)

    @unittest.mock.patch('mitroles.MitRoles.MitRoles.get_owners_for_did', side_effect=roles_mock)
    @unittest.mock.patch.object(Account, 'provision')
    def test_thaw_from_db_skips_provision_when_no_devices(self, provision_patch, roles_patch):
        # no devices, no force, shouldn't be called
        u = fake_users_db_record()
        a = Account.thaw_from_db(user_record=u, device_records=[], force_when_no_devices=False)
        self.assertFalse(provision_patch.called)

        # no devices, force, should be called
        u = fake_users_db_record()
        a = Account.thaw_from_db(user_record=u, device_records=[], force_when_no_devices=True)
        self.assertTrue(provision_patch.called)

    @unittest.mock.patch('mitroles.MitRoles.MitRoles.get_owners_for_did', side_effect=roles_mock)
    @unittest.mock.patch.object(BroadsoftRequest, 'post')
    def test_thaw_from_db_passes_voicemail_type(self, post_patch, roles_patch):
        # broadsoft
        u = fake_users_db_record()
        d = fake_phone_db_record()
        a = Account.thaw_from_db(user_record=u, device_records=[d], voicemail='broadsoft')
        self.assertEqual('broadsoft', a.voicemail)

        # unity
        u = fake_users_db_record()
        d = fake_phone_db_record()
        a = Account.thaw_from_db(user_record=u, device_records=[d], voicemail='unity')
        self.assertEqual('unity', a.voicemail)

    @unittest.mock.patch('mitroles.MitRoles.MitRoles.get_owners_for_did', side_effect=roles_mock)
    @unittest.mock.patch.object(BroadsoftRequest, 'post')
    def test_thaw_from_db_construction(self, post_patch, roles_patch):
        u = fake_users_db_record()
        d1 = fake_phone_db_record()
        d2 = fake_phone_db_record()

        # update d1 and d2 to be different
        d1.description = 'd1'
        d2.description = 'd2'
        d2.hwaddr = 'ddeeff445566'
        d2.phone_type = 'hamburger'

        a = Account.thaw_from_db(user_record=u, device_records=[d1, d2], voicemail='broadsoft')

        self.assertEqual(a.did, '6175551212')
        self.assertEqual(a.kname, 'beaver')
        self.assertEqual(a.email, 'beaver@mit.edu')
        self.assertEqual(a.first_name, 'Tim')
        self.assertEqual(a.last_name, 'Beaver')
        self.assertEqual(a.voicemail, 'broadsoft')
        self.assertEqual(a.sip_password, '123456')
        self.assertTrue(a.voicemail_mwi)
        self.assertEqual(2, len(a.devices))

        # d1
        d = a.devices[0]
        self.assertEqual(d.did, '6175551212')
        self.assertEqual(d.description, 'd1')
        self.assertTrue(d.is_primary)
        self.assertEqual(d.name, 'd1')
        self.assertEqual(d.type, 'batphone')
        self.assertEqual(d.mac_address, 'aabbcc112233')
        self.assertEqual(d.line_port, d.did + '_' + d.mac_address + '_' + str(d.index) + '@' + d.broadsoftinstance.default_domain)

        # d2
        d = a.devices[1]
        self.assertEqual(d.did, '6175551212')
        self.assertEqual(d.description, 'd2')
        self.assertFalse(d.is_primary)
        self.assertEqual(d.name, 'd2')
        self.assertEqual(d.type, 'hamburger')
        self.assertEqual(d.mac_address, 'ddeeff445566')
        self.assertEqual(d.line_port, d.did + '_' + d.mac_address + '_' + str(d.index) + '@' + d.broadsoftinstance.default_domain)
