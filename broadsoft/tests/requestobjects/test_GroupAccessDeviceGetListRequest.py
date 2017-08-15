import unittest.mock
import xml.etree.ElementTree as ET

import broadsoft.requestobjects.lib.BroadsoftRequest
from broadsoft.requestobjects.lib.BroadsoftRequest import instance_factory
from broadsoft.requestobjects.GroupAccessDeviceGetListRequest import GroupAccessDeviceGetListRequest


def return_device_get(*args, **kwargs):
    xml = """<ns0:BroadsoftDocument xmlns:ns0="C" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" protocol="OCI"><sessionId>Chriss-MacBook-Pro-4.local,2017-08-14 19:25:38.239458,9172042794</sessionId><command echo="" xsi:type="GroupAccessDeviceGetResponse18sp1"><deviceType>Generic SIP Phone</deviceType><protocol>SIP 2.0</protocol><macAddress>aabbcc112233</macAddress><description>Time Beaver</description><numberOfPorts><unlimited>true</unlimited></numberOfPorts><numberOfAssignedPorts>1</numberOfAssignedPorts><status>Online</status><configurationMode>Default</configurationMode><transportProtocol>Unspecified</transportProtocol><useCustomUserNamePassword>true</useCustomUserNamePassword><userName>6175551212@broadsoft-dev.mit.edu</userName></command></ns0:BroadsoftDocument>"""
    return ET.fromstring(xml)

def return_device_list(*args, **kwargs):
    xml = """<ns0:BroadsoftDocument xmlns:ns0="C" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" protocol="OCI"><sessionId>Chriss-MacBook-Pro-4.local,2017-08-14 18:37:22.390663,8095457306</sessionId><command echo="" xsi:type="GroupAccessDeviceGetListResponse"><accessDeviceTable><colHeading>Device Name</colHeading><colHeading>Device Type</colHeading><colHeading>Available Ports</colHeading><colHeading>Net Address</colHeading><colHeading>MAC Address</colHeading><colHeading>Status</colHeading><colHeading>Version</colHeading><row><col>Tim Beaver</col><col>Generic SIP Phone</col><col>Unlimited</col><col /><col>aabbcc112233</col><col>Online</col><col /></row></accessDeviceTable></command></ns0:BroadsoftDocument>"""
    return ET.fromstring(xml)

def return_user_did(*args, **kwargs):
    xml = """<ns0:BroadsoftDocument xmlns:ns0="C" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" protocol="OCI"><sessionId>Chriss-MacBook-Pro-4.local,2017-08-14 19:26:15.349941,6839135561</sessionId><command echo="" xsi:type="UserGetResponse21"><serviceProviderId>MIT-SP</serviceProviderId><groupId>MIT-GP</groupId><lastName>Beaver</lastName><firstName>Tim</firstName><callingLineIdLastName>Beaver</callingLineIdLastName><callingLineIdFirstName>Tim</callingLineIdFirstName><hiraganaLastName>Beaver</hiraganaLastName><hiraganaFirstName>Tim</hiraganaFirstName><phoneNumber>6175551212</phoneNumber><extension>80550</extension><language>English</language><timeZone>America/New_York</timeZone><timeZoneDisplayName>(GMT-04:00) (US) Eastern Time</timeZoneDisplayName><defaultAlias>6175551212@broadsoft-dev.mit.edu</defaultAlias><accessDeviceEndpoint><accessDevice><deviceLevel>Group</deviceLevel><deviceName>Tim Beaver</deviceName></accessDevice><linePort>6175551212_aabbcc112233_1@broadsoft-dev.mit.edu</linePort><staticRegistrationCapable>true</staticRegistrationCapable><useDomain>true</useDomain><supportVisualDeviceManagement>false</supportVisualDeviceManagement></accessDeviceEndpoint><emailAddress>beaver@mit.edu</emailAddress><countryCode>1</countryCode></command></ns0:BroadsoftDocument>"""
    return ET.fromstring(xml)


def return_none(*args, **kwargs):
    return None

class TestBroadsoftGroupAccessDeviceGetListRequest(unittest.TestCase):
    def test_to_xml_with_all_attrs(self):
        b = broadsoft.requestobjects.lib.BroadsoftRequest.BroadsoftInstance()
        g = GroupAccessDeviceGetListRequest(broadsoftinstance=b)
        g.device_name = 'dn'
        g.mac_address = 'ma'
        g.net_address = 'na'
        g.device_type = 'dt'
        g.device_version = 'dv'

        x = g.to_xml()
        self.maxDiff = None
        self.assertEqual(
            """<BroadsoftDocument protocol="OCI" xmlns="C" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><sessionId xmlns="">""" + b.session_id + """</sessionId><command xmlns="" xsi:type="GroupAccessDeviceGetListRequest"><serviceProviderId>ENT136</serviceProviderId><groupId>MIT-GP</groupId><responseSizeLimit>100000</responseSizeLimit><searchCriteriaDeviceName><mode>Equal To</mode><value>dn</value><isCaseInsensitive>true</isCaseInsensitive></searchCriteriaDeviceName><searchCriteriaDeviceMACAddress><mode>Equal To</mode><value>ma</value><isCaseInsensitive>true</isCaseInsensitive></searchCriteriaDeviceMACAddress><searchCriteriaDeviceNetAddress><mode>Equal To</mode><value>na</value><isCaseInsensitive>true</isCaseInsensitive></searchCriteriaDeviceNetAddress><searchCriteriaExactDeviceType><mode>Equal To</mode><value>Generic SIP Phone</value><isCaseInsensitive>true</isCaseInsensitive></searchCriteriaExactDeviceType><searchCriteriaAccessDeviceVersion><mode>Equal To</mode><value>dv</value><isCaseInsensitive>true</isCaseInsensitive></searchCriteriaAccessDeviceVersion></command></BroadsoftDocument>""",
            ET.tostring(x).decode('utf-8')
        )

    def test_to_xml_with_some_attrs(self):
        b = broadsoft.requestobjects.lib.BroadsoftRequest.BroadsoftInstance()
        g = GroupAccessDeviceGetListRequest(broadsoftinstance=b)
        g.mac_address = 'ma'
        g.net_address = 'na'

        x = g.to_xml()
        self.maxDiff = None
        self.assertEqual(
            """<BroadsoftDocument protocol="OCI" xmlns="C" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><sessionId xmlns="">""" + b.session_id + """</sessionId><command xmlns="" xsi:type="GroupAccessDeviceGetListRequest"><serviceProviderId>ENT136</serviceProviderId><groupId>MIT-GP</groupId><responseSizeLimit>100000</responseSizeLimit><searchCriteriaDeviceMACAddress><mode>Equal To</mode><value>ma</value><isCaseInsensitive>true</isCaseInsensitive></searchCriteriaDeviceMACAddress><searchCriteriaDeviceNetAddress><mode>Equal To</mode><value>na</value><isCaseInsensitive>true</isCaseInsensitive></searchCriteriaDeviceNetAddress></command></BroadsoftDocument>""",
            ET.tostring(x).decode('utf-8')
        )

    @unittest.mock.patch.object(GroupAccessDeviceGetListRequest, 'post', side_effect=return_device_list)
    def test_find_device_by_mac_call(self, find_device_by_mac_patch):
        # by default pass converted version of data
        d = GroupAccessDeviceGetListRequest.find_device_by_mac(mac_address='aabbcc112233')
        self.assertEqual(
            [{'Device Name': 'Tim Beaver', 'Version': None, 'Device Type': 'Generic SIP Phone', 'Status': 'Online',
              'Available Ports': 'Unlimited', 'Net Address': None, 'MAC Address': 'aabbcc112233'}],
            d
        )

        # pass return_raw false
        d = GroupAccessDeviceGetListRequest.find_device_by_mac(mac_address='aabbcc112233', return_raw=False)
        self.assertEqual(
            [{'Device Name': 'Tim Beaver', 'Version': None, 'Device Type': 'Generic SIP Phone', 'Status': 'Online',
              'Available Ports': 'Unlimited', 'Net Address': None, 'MAC Address': 'aabbcc112233'}],
            d
        )

        # pass return_raw true
        d = GroupAccessDeviceGetListRequest.find_device_by_mac(mac_address='aabbcc112233', return_raw=True)
        xml = """<ns0:BroadsoftDocument xmlns:ns0="C" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" protocol="OCI"><sessionId>Chriss-MacBook-Pro-4.local,2017-08-14 18:37:22.390663,8095457306</sessionId><command echo="" xsi:type="GroupAccessDeviceGetListResponse"><accessDeviceTable><colHeading>Device Name</colHeading><colHeading>Device Type</colHeading><colHeading>Available Ports</colHeading><colHeading>Net Address</colHeading><colHeading>MAC Address</colHeading><colHeading>Status</colHeading><colHeading>Version</colHeading><row><col>Tim Beaver</col><col>Generic SIP Phone</col><col>Unlimited</col><col /><col>aabbcc112233</col><col>Online</col><col /></row></accessDeviceTable></command></ns0:BroadsoftDocument>"""
        self.assertEqual(ET.tostring(d).decode('utf-8'), xml)

    @unittest.mock.patch.object(GroupAccessDeviceGetListRequest, 'post', side_effect=return_device_list)
    @unittest.mock.patch.object(GroupAccessDeviceGetListRequest, '__init__', side_effect=return_none)
    def test_find_device_by_mac_passes_kwargs(self, get_list_init_patch, find_device_by_mac_patch):
        # pass broadsoft instance
        i = instance_factory(instance='test')
        d = GroupAccessDeviceGetListRequest.find_device_by_mac(mac_address='aabbcc112233', broadsoftinstance=i)
        args, kwargs = get_list_init_patch.call_args_list[0]
        self.assertIn('broadsoftinstance', kwargs)
        self.assertEqual(kwargs['broadsoftinstance'].__dict__, i.__dict__)

    @unittest.mock.patch('broadsoft.requestobjects.UserGetRequest.UserGetRequest.get_user',
                         side_effect=return_user_did)
    @unittest.mock.patch('broadsoft.requestobjects.GroupAccessDeviceGetRequest.GroupAccessDeviceGetRequest.get_device',
                         side_effect=return_device_get)
    @unittest.mock.patch.object(GroupAccessDeviceGetListRequest, 'post', side_effect=return_device_list)
    def test_find_device_by_mac_and_did_call(self, find_device_by_mac_patch, get_device_patch, get_user_patch):
        # pass matching did
        d = GroupAccessDeviceGetListRequest.find_device_by_mac_and_did(mac_address='aabbcc112233', did=6175551212)
        self.assertEqual(
            d,
            {'Version': None, 'Net Address': None, 'MAC Address': 'aabbcc112233', 'Device Name': 'Tim Beaver',
             'Status': 'Online', 'Device Type': 'Generic SIP Phone', 'Available Ports': 'Unlimited'}
        )

        # pass non-matching did
        d = GroupAccessDeviceGetListRequest.find_device_by_mac_and_did(mac_address='aabbcc112233', did=6175552323)
        self.assertIsNone(d)

    @unittest.mock.patch('broadsoft.requestobjects.UserGetRequest.UserGetRequest.get_user',
                         side_effect=return_user_did)
    @unittest.mock.patch('broadsoft.requestobjects.GroupAccessDeviceGetRequest.GroupAccessDeviceGetRequest.get_device')
    @unittest.mock.patch.object(GroupAccessDeviceGetListRequest, 'post', side_effect=return_device_list)
    @unittest.mock.patch.object(GroupAccessDeviceGetListRequest, '__init__', side_effect=return_none)
    def test_find_device_by_mac_and_did_passes_kwargs(self, find_device_init_patch, find_device_by_mac_patch, get_device_patch, get_user_patch):
        # pass broadsoft instance
        i = instance_factory(instance='test')
        d = GroupAccessDeviceGetListRequest.find_device_by_mac_and_did(mac_address='aabbcc112233', did=6175551212, broadsoftinstance=i)

        args, kwargs = find_device_init_patch.call_args_list[0]
        self.assertIn('broadsoftinstance', kwargs)
        self.assertEqual(kwargs['broadsoftinstance'].__dict__, i.__dict__)

        args, kwargs = get_device_patch.call_args_list[0]
        self.assertIn('broadsoftinstance', kwargs)
        self.assertEqual(kwargs['broadsoftinstance'].__dict__, i.__dict__)

        args, kwargs = get_user_patch.call_args_list[0]
        self.assertIn('broadsoftinstance', kwargs)
        self.assertEqual(kwargs['broadsoftinstance'].__dict__, i.__dict__)
