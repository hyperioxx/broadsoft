import unittest
import unittest.mock
import broadsoft.requestobjects.lib.BroadsoftRequest
from broadsoft.lib.BroadsoftObject import BroadsoftObject
from broadsoft.Device import Device
from broadsoft.requestobjects.lib.BroadsoftRequest import BroadsoftRequest
from broadsoft.requestobjects.UserAddRequest import UserAddRequest
import xml.etree.ElementTree as ET


def return_none(*args, **kwargs):
    return None


class TestBroadsoftObject(unittest.TestCase):
    @unittest.mock.patch.object(BroadsoftObject, 'prep_attributes')
    def test_pass_broadsoftinstance(
            self, prep_attributes_patch
    ):
        b = BroadsoftObject(broadsoftinstance='a')
        self.assertEqual('a', b.broadsoftinstance)

    def test_derive_broadsoftinstance(self):
        self.assertIsInstance(
            BroadsoftObject.derive_broadsoft_instance(instance='prod'),
            broadsoft.requestobjects.lib.BroadsoftRequest.BroadsoftInstance)

        self.assertIsInstance(
            BroadsoftObject.derive_broadsoft_instance(instance='test'),
            broadsoft.requestobjects.lib.BroadsoftRequest.TestBroadsoftInstance)

    @unittest.mock.patch.object(BroadsoftObject, 'derive_broadsoft_instance')
    def test_init_calls_derive_broadsoftinstance(
            self, derive_broadsoft_instance_patch):
        # implicit instance
        b = BroadsoftObject()
        self.assertTrue(derive_broadsoft_instance_patch.called)
        call = derive_broadsoft_instance_patch.call_args_list[0]
        args, kwargs = call
        self.assertEqual(kwargs['instance'], 'prod')
        derive_broadsoft_instance_patch.called = False

        # test instance
        b = BroadsoftObject(instance='test')
        self.assertTrue(derive_broadsoft_instance_patch.called)
        call = derive_broadsoft_instance_patch.call_args_list[1]
        args, kwargs = call
        self.assertEqual(kwargs['instance'], 'test')
        derive_broadsoft_instance_patch.called = False

        # prod instance
        b = BroadsoftObject(instance='prod')
        self.assertTrue(derive_broadsoft_instance_patch.called)
        call = derive_broadsoft_instance_patch.call_args_list[2]
        args, kwargs = call
        self.assertEqual(kwargs['instance'], 'prod')
        derive_broadsoft_instance_patch.called = False

    @unittest.mock.patch.object(BroadsoftRequest, 'authenticate_and_login')
    @unittest.mock.patch.object(BroadsoftRequest, '__init__', side_effect=return_none)
    def test_login_passes_broadsoftinstance(self, init_patch, auth_patch):
        i = broadsoft.requestobjects.lib.BroadsoftRequest.instance_factory(instance='test')
        o = BroadsoftObject(broadsoftinstance=i)
        o.login()

        call = init_patch.call_args_list[0]
        args, kwargs = call
        self.assertIsInstance(kwargs['broadsoftinstance'],
                              broadsoft.requestobjects.lib.BroadsoftRequest.TestBroadsoftInstance)

    @unittest.mock.patch('broadsoft.requestobjects.lib.BroadsoftRequest.LogoutRequest.logout')
    def test_logout_passes_broadsoftinstance(self, logout_patch):
        i = broadsoft.requestobjects.lib.BroadsoftRequest.instance_factory(instance='test')
        o = BroadsoftObject(broadsoftinstance=i)
        o.logout()

        call = logout_patch.call_args_list[0]
        args, kwargs = call
        self.assertIsInstance(kwargs['broadsoftinstance'],
                              broadsoft.requestobjects.lib.BroadsoftRequest.TestBroadsoftInstance)

    @unittest.mock.patch.object(BroadsoftObject, 'check_if_object_fetched')
    @unittest.mock.patch.object(BroadsoftObject, 'prep_attributes')
    def test_from_xml_calls_prep_attributes_and_check_if_object_fetched(
            self, prep_attributes_patch, check_if_object_fetched_patch
    ):
        b = BroadsoftObject()
        prep_attributes_patch.called = False
        check_if_object_fetched_patch.called = False

        b.from_xml()
        self.assertTrue(prep_attributes_patch.called)
        self.assertTrue(check_if_object_fetched_patch.called)

    def test_check_if_object_fetched_call(self):
        # failed call, should be set to False
        xml = """<ns0:BroadsoftDocument xmlns:ns0="C" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" protocol="OCI"><sessionId>VPN-18-101-101-100.MIT.EDU,2017-08-02 21:54:52.755707,2221805120</sessionId><command echo="" type="Error" xsi:type="c:ErrorResponse"><summary>[Error 4008] User not found: 6175551212@broadsoft-dev.mit.edu</summary><summaryEnglish>[Error 4008] User not found: 6175551212@broadsoft-dev.mit.edu</summaryEnglish></command></ns0:BroadsoftDocument>"""
        xml = ET.fromstring(xml)
        b = BroadsoftObject()
        b.xml = xml
        b.check_if_object_fetched()
        self.assertFalse(b.fetched)

        # successful call, should be set to True
        xml = """<ns0:BroadsoftDocument xmlns:ns0="C" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" protocol="OCI"><sessionId>VPN-18-101-101-100.MIT.EDU,2017-08-02 22:15:09.487547,7641180547</sessionId><command echo="" xsi:type="UserGetResponse21"><serviceProviderId>MIT-SP</serviceProviderId><groupId>MIT-GP</groupId><lastName>Hall</lastName><firstName>Lecture</firstName><callingLineIdLastName>Hall</callingLineIdLastName><callingLineIdFirstName>Lecture</callingLineIdFirstName><hiraganaLastName>Hall</hiraganaLastName><hiraganaFirstName>Lecture</hiraganaFirstName><phoneNumber>6172251563</phoneNumber><extension>51563</extension><language>English</language><timeZone>America/New_York</timeZone><timeZoneDisplayName>(GMT-04:00) (US) Eastern Time</timeZoneDisplayName><defaultAlias>6172251563@broadsoft-dev.mit.edu</defaultAlias><accessDeviceEndpoint><accessDevice><deviceLevel>Group</deviceLevel><deviceName>E51-335</deviceName></accessDevice><linePort>6172251563_64167f01b5a0_1@broadsoft-dev.mit.edu</linePort><staticRegistrationCapable>true</staticRegistrationCapable><useDomain>true</useDomain><supportVisualDeviceManagement>false</supportVisualDeviceManagement></accessDeviceEndpoint><emailAddress>peterb@mit.edu</emailAddress><countryCode>1</countryCode></command></ns0:BroadsoftDocument>"""
        xml = ET.fromstring(xml)
        b = BroadsoftObject()
        b.xml = xml
        b.check_if_object_fetched()
        self.assertTrue(b.fetched)

    @unittest.mock.patch.object(BroadsoftRequest, 'post')
    @unittest.mock.patch.object(Device, 'overwrite')
    def test_implicit_overwrite_respected(self, overwrite_patch, post_patch):
        # doing this with a Device since raw BroadsoftObject doesn't have an overwrite or build_provision_request method

        # with default value for implicit overwrite (False)
        d = Device(mac_address='aabbcc112233', did=6175551212)
        d.provision()
        self.assertFalse(overwrite_patch.called)
        overwrite_patch.called = False

        # with False for implicit overwrite
        d = Device(mac_address='aabbcc112233', did=6175551212, implicit_overwrite=False)
        self.assertFalse(overwrite_patch.called)
        d.provision()
        overwrite_patch.called = False

        # with True for implicit overwrite
        d = Device(mac_address='aabbcc112233', did=6175551212, implicit_overwrite=True)
        d.provision()
        self.assertTrue(overwrite_patch.called)
