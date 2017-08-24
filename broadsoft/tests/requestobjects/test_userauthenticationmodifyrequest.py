import unittest.mock
import xml.etree.ElementTree as ET

from broadsoft.requestobjects.UserAuthenticationModifyRequest import UserAuthenticationModifyRequest
from broadsoft.requestobjects.lib.BroadsoftRequest import BroadsoftRequest
from broadsoft.requestobjects.lib.BroadsoftRequest import instance_factory


class TestBroadsoftUserAuthenticationModifyRequest(unittest.TestCase):
    @unittest.mock.patch.object(BroadsoftRequest, 'convert_phone_number')
    @unittest.mock.patch.object(UserAuthenticationModifyRequest, 'validate')
    def test_did_gets_converted_on_build_xml(self,
            validate_patch,
            convert_phone_number_patch
    ):
        u = UserAuthenticationModifyRequest(sip_user_id='6175551212@broadsoft-dev.mit.edu')
        self.assertFalse(convert_phone_number_patch.called)
        u.did = '617-555-1213'
        u.to_xml()
        self.assertTrue(convert_phone_number_patch.called)

    def test_did_converted_on_init(self):
        u = UserAuthenticationModifyRequest(did='617-555-1212')
        self.assertEqual('6175551212', u.did)

    @unittest.mock.patch.object(UserAuthenticationModifyRequest, 'validate')
    def test_build_command_xml_calls_validate(
            self,
            validate_patch
    ):
        u = UserAuthenticationModifyRequest(sip_user_id='6175551212@broadsoft-dev.mit.edu')
        self.assertFalse(validate_patch.called)
        u.build_command_xml()
        self.assertTrue(validate_patch.called)

    def test_validate(self):
        u = UserAuthenticationModifyRequest()
        with self.assertRaises(ValueError):
            u.validate()

        # no password
        u = UserAuthenticationModifyRequest(sip_user_id='6175551212@broadsoft-dev.mit.edu', did='61755512121')
        with self.assertRaises(ValueError):
            u.validate()

        # no did
        u = UserAuthenticationModifyRequest(sip_user_id='6175551212@broadsoft-dev.mit.edu', new_password='gaga')
        with self.assertRaises(ValueError):
            u.validate()

        # bad did
        u = UserAuthenticationModifyRequest(sip_user_id='6175551212@broadsoft-dev.mit.edu', new_password='gaga', did='abc')
        with self.assertRaises(ValueError):
            u.validate()

        # no sip user id
        u = UserAuthenticationModifyRequest(did='6175551212', new_password='gaga')
        with self.assertRaises(ValueError):
            u.validate()

    def test_to_xml(self):
        self.maxDiff = None

        # this one should only build out XML for what we provide.

        # here's a fully populated request
        u = UserAuthenticationModifyRequest(sip_user_id='6175551212@broadsoft-dev.mit.edu', did=6175551212,
                                            new_password='newp')

        target_xml = \
            '<command xmlns="" xsi:type="UserAuthenticationModifyRequest">' + \
                '<userId>6175551212@broadsoft-dev.mit.edu</userId>' + \
                '<userName>6175551212</userName>' + \
                '<newPassword>newp</newPassword>' + \
            '</command>'

        cmd = u.build_command_xml()
        self.assertEqual(target_xml, ET.tostring(cmd).decode('utf-8'))

    @unittest.mock.patch.object(BroadsoftRequest, 'post')
    @unittest.mock.patch.object(BroadsoftRequest, '__init__', side_effect=None)
    def test_set_credentials_passes_broadsoft_instance(self, init_patch, post_patch):
        i = instance_factory(instance='prod')
        UserAuthenticationModifyRequest.set_credentials(new_password='gaga', did=6175551212,
                                                        sip_user_id='6175551212@broadsoft-dev.mit.edu',
                                                        broadsoftinstance=i)

        for call in init_patch.call_args_list:
            args, kwargs = call
            self.assertEqual(kwargs['broadsoftinstance'].api_url, i.api_url)
