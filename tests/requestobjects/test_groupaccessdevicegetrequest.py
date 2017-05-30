import unittest.mock
import xml.etree.ElementTree as ET
from broadsoft.requestobjects.GroupAccessDeviceGetRequest import GroupAccessDeviceGetRequest


class TestBroadsoftGroupAccessDeviceGetRequest(unittest.TestCase):
    def test_validate(self):
        g = GroupAccessDeviceGetRequest()
        with self.assertRaises(ValueError):
            g.validate()

    def test_to_xml(self):
        g = GroupAccessDeviceGetRequest(name='beaverphone')

        x = g.to_xml()
        self.maxDiff = None
        self.assertEqual(
            '<BroadsoftDocument protocol="OCI" xmlns="C" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">' +
                '<sessionId xmlns="">' + g.session_id + '</sessionId>' +
                '<command xmlns="" xsi:type="GroupAccessDeviceGetRequest18sp1">' +
                    '<serviceProviderId>' + g.service_provider + '</serviceProviderId>' +
                    '<groupId>' + g.group_id + '</groupId>' +
                    '<deviceName>' + g.name + '</deviceName>' +
                '</command>' +
            '</BroadsoftDocument>',
            ET.tostring(x).decode('utf-8')
        )

    def test_static_method(self):
        self.assertFalse("develop static tests")

    """
    def test_use_test_gets_passed_to_broadsoftdocument(self):
        g = GroupAccessDeviceGetRequest()
        self.assertEqual(g.prod_api_url, g.api_url)

        g = GroupAccessDeviceGetRequest(use_test=False)
        self.assertEqual(g.prod_api_url, g.api_url)

        g = GroupAccessDeviceGetRequest(use_test=True)
        self.assertEqual(g.test_api_url, g.api_url)

    def test_can_pass_session_id(self):
        g = GroupAccessDeviceGetRequest(session_id='sesh')
        self.assertEqual('sesh', g.session_id)

    def test_can_pass_auth_object(self):
        class FakeAuthObject:
            def __init__(self):
                self.foo = 'var'

        f = FakeAuthObject()
        g = GroupAccessDeviceGetRequest(auth_object=f)
        self.assertEqual(f, g.auth_object)

    def test_can_pass_login_object(self):
        class FakeLoginObject:
            def __init__(self):
                self.foo = 'var'

        f = FakeLoginObject()
        g = GroupAccessDeviceGetRequest(login_object=f)
        self.assertEqual(f, g.login_object)

    @unittest.mock.patch('broadsoft.requestobjects.lib.BroadsoftRequest.AuthenticationRequest.authenticate')
    @unittest.mock.patch('broadsoft.requestobjects.lib.BroadsoftRequest.LoginRequest.login')
    @unittest.mock.patch.object(GroupAccessDeviceGetRequest, 'post', side_effect=return_groups_list)
    def test_list_groups_convert_to_list(
        self,
        post_patch,
        login_patch,
        auth_patch
    ):
        data = GroupAccessDeviceGetRequest.list_groups()
        self.assertEqual(
            [{'Group Name': 'Another Test Group', 'User Limit': '25', 'Group Id': 'anothertestgroup'},
             {'Group Name': None, 'User Limit': '25', 'Group Id': 'sandbox'}],
            data
        )
    """