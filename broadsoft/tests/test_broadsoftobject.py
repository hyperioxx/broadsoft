import unittest
import unittest.mock
import broadsoft.requestobjects.lib.BroadsoftRequest
from broadsoft.lib.BroadsoftObject import BroadsoftObject
from broadsoft.Device import Device
from broadsoft.Account import Account
from broadsoft.requestobjects.lib.BroadsoftRequest import BroadsoftRequest
from broadsoft.requestobjects.UserAddRequest import UserAddRequest
import xml.etree.ElementTree as ET
from broadsoft.requestobjects.lib.BroadsoftRequest import instance_factory


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
    @unittest.mock.patch.object(Account, 'overwrite')
    @unittest.mock.patch.object(Device, 'overwrite')
    def test_implicit_overwrite_respected(self, device_overwrite_patch, account_overwrite_patch, post_patch):
        i = instance_factory(instance='test')

        # doing this with a Device since raw BroadsoftObject doesn't have an overwrite or build_provision_request method

        # with default value for implicit overwrite (False)
        d = Device(mac_address='aabbcc112233', did=6175551212, broadsoftinstance=i)
        d.provision()
        self.assertFalse(device_overwrite_patch.called)
        device_overwrite_patch.called = False

        # with False for implicit overwrite
        d = Device(mac_address='aabbcc112233', did=6175551212, implicit_overwrite=False, broadsoftinstance=i)
        self.assertFalse(device_overwrite_patch.called)
        d.provision()
        device_overwrite_patch.called = False

        # with True for implicit overwrite
        d = Device(mac_address='aabbcc112233', did=6175551212, implicit_overwrite=True, broadsoftinstance=i)
        d.provision()
        self.assertTrue(device_overwrite_patch.called)

        # doing it again with an Account

        # with default value for implicit overwrite (False)
        a = Account(did=6175551212, sip_user_id='6175551212@broadsoft-dev.mit.edu', email='beaver@mit.edu', broadsoftinstance=i)
        a.provision()
        self.assertFalse(account_overwrite_patch.called)
        account_overwrite_patch.called = False

        # with False for implicit overwrite
        a = Account(did=6175551212, sip_user_id='6175551212@broadsoft-dev.mit.edu', email='beaver@mit.edu', implicit_overwrite=False, broadsoftinstance=i)
        self.assertFalse(account_overwrite_patch.called)
        a.provision()
        account_overwrite_patch.called = False

        # with True for implicit overwrite
        a = Account(did=6175551212, sip_user_id='6175551212@broadsoft-dev.mit.edu', email='beaver@mit.edu', implicit_overwrite=True, broadsoftinstance=i)
        a.provision()
        self.assertTrue(account_overwrite_patch.called)

    def test_skip_if_exists_set_attr(self):
        # Account should default to no
        a = Account()
        self.assertFalse(a.skip_if_exists)

        # Device should default to yes
        d = Device()
        self.assertTrue(d.skip_if_exists)

        # Can override Account
        a = Account(skip_if_exists=True)
        self.assertTrue(a.skip_if_exists)

        # Can override Device
        d = Device(skip_if_exists=False)
        self.assertFalse(d.skip_if_exists)

    def test_device_should_skip_error(self):
        d = Device(skip_if_exists=True)
        self.assertFalse(d.should_skip_error(error='blah'))
        self.assertTrue(d.should_skip_error(error='the SOAP server threw an error: [Error 4500] Access Device already exists: 6173000066_1 :: [Error 4500] Access Device already exists: 6173000066_1 :: None'))

        d = Device(skip_if_exists=False)
        self.assertFalse(d.should_skip_error(error='blah'))
        self.assertFalse(d.should_skip_error(
            error='the SOAP server threw an error: [Error 4500] Access Device already exists: 6173000066_1 :: [Error 4500] Access Device already exists: 6173000066_1 :: None'))

    def test_account_should_skip_error(self):
        a = Account(skip_if_exists=True)
        self.assertFalse(a.should_skip_error(error='blah'))
        self.assertTrue(a.should_skip_error(
            error='the SOAP server threw an error: [Error 4200] User already exists: 6175551212@broadsoft-dev.mit.edu :: [Error 4200] User already exists: 6175551212@broadsoft-dev.mit.edu :: None'))

        a = Account(skip_if_exists=False)
        self.assertFalse(a.should_skip_error(error='blah'))
        self.assertFalse(a.should_skip_error(
            error='the SOAP server threw an error: [Error 4200] User already exists: 6175551212@broadsoft-dev.mit.edu :: [Error 4200] User already exists: 6175551212@broadsoft-dev.mit.edu :: None'))

    @unittest.mock.patch('broadsoft.requestobjects.lib.BroadsoftRequest.BroadsoftRequest.post',
                         side_effect=RuntimeError('the SOAP server threw an error: [Error 4500] Access Device already exists: 6173000066_1 :: [Error 4500] Access Device already exists: 6173000066_1 :: None'))
    def test_skip_if_exists_for_device(self, post_patch):
        # this should not throw an error
        d = Device(skip_if_exists=True)
        d.provision()

        # this should throw an error
        d = Device(skip_if_exists=False)
        with self.assertRaises(RuntimeError):
            d.provision()

    @unittest.mock.patch(
        'broadsoft.requestobjects.UserSharedCallAppearanceGetRequest.UserSharedCallAppearanceGetRequest.get_devices')
    @unittest.mock.patch.object(Account, 'activate_voicemail')
    @unittest.mock.patch.object(Account, 'set_device_passwords')
    @unittest.mock.patch.object(Account, 'attach_default_devices')
    @unittest.mock.patch.object(Account, 'generate_sip_password')
    @unittest.mock.patch('broadsoft.requestobjects.lib.BroadsoftRequest.BroadsoftRequest.post',
                         side_effect=RuntimeError(
                             'the SOAP server threw an error: [Error 4200] User already exists: 6175551212@broadsoft-dev.mit.edu :: [Error 4200] User already exists: 6175551212@broadsoft-dev.mit.edu :: None'))
    def test_skip_if_exists_for_account(self, post_patch, gen_pwd_patch, attach_devices_patch, set_pwd_patch,
                                        vmail_patch, get_devices_patch):
        # this should not throw an error
        a = Account(did=6175551212, skip_if_exists=True, email='beaver@mit.edu')
        a.provision()

        # this should throw an error
        a = Account(did=6175551212, skip_if_exists=False, email='beaver@mit.edu')
        with self.assertRaises(RuntimeError):
            a.provision()

    @unittest.mock.patch('broadsoft.requestobjects.UserSharedCallAppearanceGetRequest.UserSharedCallAppearanceGetRequest.get_devices')
    def test_paginate_request(self, get_devices_patch):
        import math

        a = Account()
        a.did = 6175551212
        a.kname = 'beaver'
        a.email = 'beaver@mit.edu'
        a.first_name = 'Time'
        a.last_name = 'Beaver'
        a.voicemail = 'broadsoft'
        a.sip_password = 'blah'
        a.voicemail_mwi = True
        a.prep_attributes()
        a.generate_sip_password()
        a.attach_default_devices()

        req = a.build_provision_request()
        reqs = a.paginate_request(request=req)

        expected_fragments = math.ceil(len(req.commands) / BroadsoftRequest.max_commands_per_request)
        self.assertEqual(expected_fragments, len(reqs))

        for r in reqs:
            self.assertLessEqual(len(r.commands), BroadsoftRequest.max_commands_per_request)
            self.assertIsInstance(r, BroadsoftRequest)

    @unittest.mock.patch.object(BroadsoftObject, 'paginate_request')
    @unittest.mock.patch.object(BroadsoftRequest, 'post')
    @unittest.mock.patch.object(Account, 'overwrite')
    def test_provision_should_paginate_large_command_set(self, overwrite_patch, post_patch, paginate_patch):
        a = Account()
        a.did = 6175551212
        a.kname = 'beaver'
        a.email = 'beaver@mit.edu'
        a.first_name = 'Time'
        a.last_name = 'Beaver'
        a.voicemail = 'broadsoft'
        a.sip_password = 'blah'
        a.voicemail_mwi = True
        a.prep_attributes()
        a.generate_sip_password()
        a.attach_default_devices()
        a.provision()

        self.assertTrue(paginate_patch.called)

    def test_paginate_should_not_mangle_non_compound_request(self):
        from broadsoft.requestobjects.GroupAccessDeviceAddRequest import GroupAccessDeviceAddRequest
        g = GroupAccessDeviceAddRequest()

        b = BroadsoftObject()
        reqs = b.paginate_request(request=g)
        self.assertEqual([g], reqs)

    def test_need_to_test_logging_stuff(self):
        # can pass logging level
        # get passed when we create Device, Voicemail
        # multiple calls to setup_logging() doesn't overload the handlers
        self.assertFalse("write this")

    def test_derive_logging_level_object(self):
        self.assertFalse("write this")
