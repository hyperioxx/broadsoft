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
                '<endpoint>' + \
                    '<accessDeviceEndpoint>' + \
                        '<accessDevice>' + \
                            '<deviceLevel>Group</deviceLevel>' + \
                            '<deviceName>Generic</deviceName>' + \
                        '</accessDevice>' + \
                        '<linePort>6175551212_lp@broadsoft-dev.mit.edu</linePort>' + \
                    '</accessDeviceEndpoint>' + \
                '</endpoint>' + \
            '</command>'

        cmd = u.build_command_xml()
        self.assertEqual(target_xml, ET.tostring(cmd).decode('utf-8'))

        # here's a request with just last name (inherits Generic as device name)
        u = UserModifyRequest(sip_user_id='6175551212@broadsoft-dev.mit.edu', last_name='Beaver')
        target_xml = \
            '<command xmlns="" xsi:type="UserModifyRequest16"><userId>6175551212@broadsoft-dev.mit.edu</userId><lastName>Beaver</lastName><firstName>(None)</firstName><endpoint><accessDeviceEndpoint><accessDevice><deviceLevel>Group</deviceLevel><deviceName>Generic</deviceName></accessDevice></accessDeviceEndpoint></endpoint></command>'

        cmd = u.build_command_xml()
        self.assertEqual(target_xml, ET.tostring(cmd).decode('utf-8'))

        # here's a request with just device_name (inherits Generic as device name)
        u = UserModifyRequest(sip_user_id='6175551212@broadsoft-dev.mit.edu', device_name='beaverphone')
        target_xml = \
            '<command xmlns="" xsi:type="UserModifyRequest16"><userId>6175551212@broadsoft-dev.mit.edu</userId><lastName>(None)</lastName><firstName>(None)</firstName><endpoint><accessDeviceEndpoint><accessDevice><deviceLevel>Group</deviceLevel><deviceName>Generic</deviceName></accessDevice></accessDeviceEndpoint></endpoint></command>'

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
