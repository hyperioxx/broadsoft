import unittest.mock
import xml.etree.ElementTree as ET
from broadsoft.requestobjects.UserSharedCallAppearanceGetRequest import UserSharedCallAppearanceGetRequest


class TestBroadsoftUserSharedCallAppearanceGetRequest(unittest.TestCase):
    def test_did_gets_converted_at_init(self):
        u = UserSharedCallAppearanceGetRequest(did=6175551212)
        self.assertEqual('6175551212', u.did)

        u = UserSharedCallAppearanceGetRequest(did='617-555-1212')
        self.assertEqual('6175551212', u.did)

    def test_did_gets_converted_at_build_command_xml(self):
        u = UserSharedCallAppearanceGetRequest()
        u.did = 6175551212
        u.build_command_xml()
        self.assertEqual('6175551212', u.did)

        u = UserSharedCallAppearanceGetRequest()
        u.did = '617-555-1212'
        u.build_command_xml()
        self.assertEqual('6175551212', u.did)

    def test_sip_user_id_derived_at_init(self):
        u = UserSharedCallAppearanceGetRequest(did=6175551212)
        self.assertEqual('6175551212@' + u.default_domain, u.sip_user_id)

        u = UserSharedCallAppearanceGetRequest(did=6175551212, sip_user_id='beaver@mit.edu')
        self.assertEqual('beaver@mit.edu', u.sip_user_id)

    def test_sip_user_id_derived_at_build_command_xml(self):
        u = UserSharedCallAppearanceGetRequest()
        u.did = 6175551212
        u.build_command_xml()
        self.assertEqual('6175551212@' + u.default_domain, u.sip_user_id)

        u = UserSharedCallAppearanceGetRequest()
        u.did = 6175551212
        u.sip_user_id = 'beaver@mit.edu'
        u.build_command_xml()
        self.assertEqual('beaver@mit.edu', u.sip_user_id)

    def test_validate(self):
        u = UserSharedCallAppearanceGetRequest()
        with self.assertRaises(ValueError):
            u.validate()

    def test_to_xml(self):
        u = UserSharedCallAppearanceGetRequest(did=6175551212)

        x = u.to_xml()
        self.maxDiff = None
        self.assertEqual(
            '<BroadsoftDocument protocol="OCI" xmlns="C" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">' +
                '<sessionId xmlns="">' + u.session_id + '</sessionId>' +
                '<command xmlns="" xsi:type="UserSharedCallAppearanceGetRequest16sp2">' +
                    '<userId>' + u.sip_user_id + '</userId>' +
                '</command>' +
            '</BroadsoftDocument>',
            ET.tostring(x).decode('utf-8')
        )

    def test_static_method(self):
        self.assertFalse("once we have a from_xml() for this, develop below")

    """
    def test_use_test_gets_passed_to_broadsoftdocument(self):
        g = UserSharedCallAppearanceGetRequest()
        self.assertEqual(g.prod_api_url, g.api_url)

        g = UserSharedCallAppearanceGetRequest(use_test=False)
        self.assertEqual(g.prod_api_url, g.api_url)

        g = UserSharedCallAppearanceGetRequest(use_test=True)
        self.assertEqual(g.test_api_url, g.api_url)

    def test_can_pass_session_id(self):
        g = UserSharedCallAppearanceGetRequest(session_id='sesh')
        self.assertEqual('sesh', g.session_id)

    def test_can_pass_auth_object(self):
        class FakeAuthObject:
            def __init__(self):
                self.foo = 'var'

        f = FakeAuthObject()
        g = UserSharedCallAppearanceGetRequest(auth_object=f)
        self.assertEqual(f, g.auth_object)

    def test_can_pass_login_object(self):
        class FakeLoginObject:
            def __init__(self):
                self.foo = 'var'

        f = FakeLoginObject()
        g = UserSharedCallAppearanceGetRequest(login_object=f)
        self.assertEqual(f, g.login_object)

    @unittest.mock.patch('broadsoft.requestobjects.lib.BroadsoftRequest.AuthenticationRequest.authenticate')
    @unittest.mock.patch('broadsoft.requestobjects.lib.BroadsoftRequest.LoginRequest.login')
    @unittest.mock.patch.object(UserSharedCallAppearanceGetRequest, 'post', side_effect=return_groups_list)
    def test_list_groups_convert_to_list(
        self,
        post_patch,
        login_patch,
        auth_patch
    ):
        data = UserSharedCallAppearanceGetRequest.list_groups()
        self.assertEqual(
            [{'Group Name': 'Another Test Group', 'User Limit': '25', 'Group Id': 'anothertestgroup'},
             {'Group Name': None, 'User Limit': '25', 'Group Id': 'sandbox'}],
            data
        )
    """