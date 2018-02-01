import unittest.mock
import xml.etree.ElementTree as ET

from broadsoft.requestobjects.UserModifyRequest import UserModifyRequest
from broadsoft.requestobjects.lib.BroadsoftRequest import BroadsoftRequest


class TestBroadsoftUserModifyRequest(unittest.TestCase):
    @unittest.mock.patch.object(BroadsoftRequest, 'convert_phone_number')
    @unittest.mock.patch.object(UserModifyRequest, 'validate')
    def test_did_gets_converted_on_build_xml(self,
            validate_patch,
            convert_phone_number_patch
    ):
        u = UserModifyRequest(sip_user_id='6175551212@broadsoft-dev.mit.edu')
        self.assertFalse(convert_phone_number_patch.called)
        u.did = '617-555-1213'
        u.to_xml()
        self.assertTrue(convert_phone_number_patch.called)

    @unittest.mock.patch.object(BroadsoftRequest, 'convert_phone_number')
    @unittest.mock.patch.object(UserModifyRequest, 'validate')
    def test_clid_did_gets_converted(
            self,
            validate_patch,
            convert_phone_number_patch
    ):
        u = UserModifyRequest(sip_user_id='6175551212@broadsoft-dev.mit.edu')
        self.assertFalse(convert_phone_number_patch.called)
        u.clid_did = '617-555-1213'
        u.to_xml()
        self.assertTrue(convert_phone_number_patch.called)

    def test_did_converted_on_init(self):
        u = UserModifyRequest(did='617-555-1212')
        self.assertEqual('6175551212', u.did)

    def test_clid_did_converted_on_init(self):
        u = UserModifyRequest(clid_did='617-555-1212')
        self.assertEqual('6175551212', u.clid_did)

    @unittest.mock.patch.object(UserModifyRequest, 'validate')
    def test_build_command_xml_calls_validate(
            self,
            validate_patch
    ):
        u = UserModifyRequest(sip_user_id='6175551212@broadsoft-dev.mit.edu')
        self.assertFalse(validate_patch.called)
        u.build_command_xml()
        self.assertTrue(validate_patch.called)

    def test_validate(self):
        u = UserModifyRequest()
        with self.assertRaises(ValueError):
            u.validate()

        u = UserModifyRequest(sip_user_id='6175551212@broadsoft-dev.mit.edu', did='61755512121')
        with self.assertRaises(ValueError):
            u.validate()

        u = UserModifyRequest(sip_user_id='6175551212@broadsoft-dev.mit.edu', clid_did='61755512121')
        with self.assertRaises(ValueError):
            u.validate()

    @unittest.mock.patch.object(UserModifyRequest, 'set_drones')
    @unittest.mock.patch.object(BroadsoftRequest, 'prep_attributes')
    def test_prep_attrs_calls_parent_version_and_set_drones(self, prep_patch, drones_patch):
        u = UserModifyRequest(did='6175551212', first_name='Tim', last_name='Beaver')

        # test called by init
        self.assertTrue(prep_patch.called)
        self.assertTrue(drones_patch.called)

        # and when called explicitly
        prep_patch.called = False
        drones_patch.called = False
        u.prep_attributes()
        self.assertTrue(prep_patch.called)
        self.assertTrue(drones_patch.called)

    def test_set_drones_call(self):
        # no value set; should overwrite implicitly
        u = UserModifyRequest(did='6175551212', first_name='Tim', last_name='Beaver')
        self.assertEqual(u.did, u.clid_did)
        self.assertEqual(u.first_name, u.clid_first_name)
        self.assertEqual(u.last_name, u.clid_last_name)

        # change parent vals; leave drones alone; calling set_drones() should overwrite
        u.did = 6175551213
        u.first_name = 'Timmy'
        u.last_name = 'Beav-Beav'
        u.set_drones()
        self.assertEqual(u.did, u.clid_did)
        self.assertEqual(u.first_name, u.clid_first_name)
        self.assertEqual(u.last_name, u.clid_last_name)

        # change parent vals; also set drones explicitly; calling set_drones() should not overwrite
        u.did = 6175551214
        u.first_name = 'Timmy2'
        u.last_name = 'Beav-Beav2'
        u.clid_did = 6175551215
        u.clid_first_name = 'T'
        u.clid_last_name = 'B'
        u.set_drones()
        self.assertNotEquals(u.did, u.clid_did)
        self.assertNotEquals(u.first_name, u.clid_first_name)
        self.assertNotEquals(u.last_name, u.clid_last_name)

    def test_prep_attrs_sets_clid_first_name_and_clid_last_name(self):
        u = UserModifyRequest(did='6175551212', first_name='Tim', last_name='Beaver')
        self.assertEqual(u.clid_first_name, u.first_name)
        self.assertEqual(u.clid_last_name, u.last_name)
        self.assertEqual(u.clid_did, u.did)

        u.first_name = 'Timmy'
        u.last_name = 'Beav-Beav'
        u.did = '6175551213'
        u.prep_attributes()
        self.assertEqual(u.clid_first_name, u.first_name)
        self.assertEqual(u.clid_last_name, u.last_name)
        self.assertEqual(u.clid_did, u.did)

    def test_value_for_include_endpoint(self):
        u = UserModifyRequest(sip_user_id='6175551212@broadsoft-dev.mit.edu', did='6175551212', first_name='Tim',
                              last_name='Beaver')
        self.assertFalse(u.include_endpoint)
        cmd = u.build_command_xml()
        self.assertEqual(
            '<command xmlns="" xsi:type="UserModifyRequest16"><userId>6175551212@broadsoft-dev.mit.edu</userId><lastName>Beaver</lastName><firstName>Tim</firstName><callingLineIdLastName>Beaver</callingLineIdLastName><callingLineIdFirstName>Tim</callingLineIdFirstName><phoneNumber>6175551212</phoneNumber><extension>51212</extension><callingLineIdPhoneNumber>6175551212</callingLineIdPhoneNumber></command>',
            ET.tostring(cmd).decode('utf-8')
        )

        u = UserModifyRequest(sip_user_id='6175551212@broadsoft-dev.mit.edu', did='6175551212', first_name='Tim',
                              last_name='Beaver', include_endpoint=True)
        self.assertTrue(u.include_endpoint)
        cmd = u.build_command_xml()
        self.assertEqual(
            '<command xmlns="" xsi:type="UserModifyRequest16"><userId>6175551212@broadsoft-dev.mit.edu</userId><lastName>Beaver</lastName><firstName>Tim</firstName><callingLineIdLastName>Beaver</callingLineIdLastName><callingLineIdFirstName>Tim</callingLineIdFirstName><phoneNumber>6175551212</phoneNumber><extension>51212</extension><callingLineIdPhoneNumber>6175551212</callingLineIdPhoneNumber><endpoint><accessDeviceEndpoint><accessDevice><deviceLevel>Group</deviceLevel><deviceName>Generic</deviceName></accessDevice></accessDeviceEndpoint></endpoint></command>',
            ET.tostring(cmd).decode('utf-8')
        )

    def test_to_xml(self):
        self.maxDiff = None

        # this one should only build out XML for what we provide.

        # here's a fully populated request
        u = UserModifyRequest(sip_user_id='6175551212@broadsoft-dev.mit.edu', last_name='Beaver',
                              first_name='Tim', clid_first_name='Timothy', clid_last_name='Beaverrr',
                              name_dialing_name="Timmy B", did=6175551212, extension=1212,
                              clid_did=6175551213, old_password='oldp', new_password='newp',
                              email_address='beaver@mit.edu', device_name='beaverphone',
                              line_port='6175551212_lp@broadsoft-dev.mit.edu')

        target_xml = \
            '<command xmlns="" xsi:type="UserModifyRequest16">' + \
                '<userId>6175551212@broadsoft-dev.mit.edu</userId>' + \
                '<lastName>Beaver</lastName>' + \
                '<firstName>Tim</firstName>' + \
                '<callingLineIdLastName>Beaverrr</callingLineIdLastName>' + \
                '<callingLineIdFirstName>Timothy</callingLineIdFirstName>' + \
                '<nameDialingName>Timmy B</nameDialingName>' + \
                '<phoneNumber>6175551212</phoneNumber>' + \
                '<extension>1212</extension>' + \
                '<callingLineIdPhoneNumber>6175551213</callingLineIdPhoneNumber>' + \
                '<oldPassword>oldp</oldPassword>' + \
                '<newPassword>newp</newPassword>' + \
                '<emailAddress>beaver@mit.edu</emailAddress>' + \
            '</command>'

        cmd = u.build_command_xml()
        self.assertEqual(target_xml, ET.tostring(cmd).decode('utf-8'))

        # here's a request with just last name (inherits Generic as device name)
        u = UserModifyRequest(sip_user_id='6175551212@broadsoft-dev.mit.edu', last_name='Beaver')
        target_xml = \
            '<command xmlns="" xsi:type="UserModifyRequest16"><userId>6175551212@broadsoft-dev.mit.edu</userId><lastName>Beaver</lastName><callingLineIdLastName>Beaver</callingLineIdLastName></command>'

        cmd = u.build_command_xml()
        self.assertEqual(target_xml, ET.tostring(cmd).decode('utf-8'))

        # here's a request with just device_name (inherits Generic as device name)
        u = UserModifyRequest(sip_user_id='6175551212@broadsoft-dev.mit.edu', device_name='beaverphone')
        target_xml = \
            '<command xmlns="" xsi:type="UserModifyRequest16"><userId>6175551212@broadsoft-dev.mit.edu</userId></command>'

        cmd = u.build_command_xml()
        self.assertEqual(target_xml, ET.tostring(cmd).decode('utf-8'))

    def test_did_can_be_integer(self):
        def test_to_xml(self):
            u = UserModifyRequest(sip_user_id='6175551212@broadsoft-dev.mit.edu', did='61755512121')
            xml = u.to_xml()

    def test_derive_extension(self):
        # various formats of did
        u = UserModifyRequest()
        u.did = '6175551212'
        u.derive_extension()
        self.assertEqual('51212', u.extension)

        u = UserModifyRequest()
        u.did = '617-555-1212'
        u.derive_extension()
        self.assertEqual('51212', u.extension)

        u = UserModifyRequest()
        u.did = 6175551212
        u.derive_extension()
        self.assertEqual('51212', u.extension)

        # doesn't clobber extension when explicitly set
        u = UserModifyRequest()
        u.did = '617-555-1212'
        u.extension = '551234'
        u.derive_extension()
        self.assertEqual('551234', u.extension)

        # can override number of digits
        u = UserModifyRequest()
        u.did = 6175551212
        u.derive_extension(digits=6)
        self.assertEqual('551212', u.extension)

    @unittest.mock.patch.object(UserModifyRequest, 'derive_extension')
    def test_build_command_xml_calls_derive_extension(
            self,
            derive_extension_patch
    ):
        u = UserModifyRequest()
        u.sip_user_id = 'test'
        u.did = 6175551212
        u.clid_did = 6175551212
        u.build_command_xml()
        self.assertTrue(derive_extension_patch.called)

    @unittest.mock.patch.object(UserModifyRequest, 'derive_extension')
    def test_init_calls_derive_extension(
            self,
            derive_extension_patch
    ):
        u = UserModifyRequest()
        self.assertTrue(derive_extension_patch.called)
