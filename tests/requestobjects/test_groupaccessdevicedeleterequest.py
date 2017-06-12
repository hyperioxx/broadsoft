import unittest.mock
import xml.etree.ElementTree as ET
from broadsoft.requestobjects.GroupAccessDeviceDeleteRequest import GroupAccessDeviceDeleteRequest
from broadsoft.requestobjects.lib.BroadsoftRequest import BroadsoftRequest


class TestBroadsoftGroupAccessDeviceDeleteRequest(unittest.TestCase):
    def test_validate(self):
        u = GroupAccessDeviceDeleteRequest()
        with self.assertRaises(ValueError):
            u.validate()

    def test_to_xml(self):
        d = GroupAccessDeviceDeleteRequest(
            device_name='dname'
        )

        x = d.to_xml()
        self.maxDiff = None
        self.assertEqual(
            '<BroadsoftDocument protocol="OCI" xmlns="C" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">' +
                '<sessionId xmlns="">' + d.session_id + '</sessionId>' +
                '<command xmlns="" xsi:type="GroupAccessDeviceDeleteRequest">' +
                    '<serviceProviderId>' + d.service_provider + '</serviceProviderId>' +
                    '<groupId>' + d.group_id + '</groupId>' +
                    '<deviceName>' + d.device_name + '</deviceName>' +
                '</command>' +
            '</BroadsoftDocument>',
            ET.tostring(x).decode('utf-8')
        )

    @unittest.mock.patch.object(BroadsoftRequest, 'extract_payload')
    @unittest.mock.patch('broadsoft.requestobjects.lib.BroadsoftRequest.LogoutRequest.logout')
    @unittest.mock.patch.object(BroadsoftRequest, 'check_error')
    @unittest.mock.patch('requests.post')
    @unittest.mock.patch('broadsoft.requestobjects.lib.SoapEnvelope.SoapEnvelope.to_string')
    @unittest.mock.patch.object(BroadsoftRequest, 'to_string')
    @unittest.mock.patch.object(BroadsoftRequest, 'authenticate_and_login')
    def test_can_pass_session_id(
            self, login_patch, ro_to_string_patch, envelop_to_string_patch, requests_post_patch, check_error_patch,
            logout_patch, extract_payload_patch
    ):
        g = GroupAccessDeviceDeleteRequest(session_id='sesh')
        self.assertEqual('sesh', g.session_id)

    @unittest.mock.patch.object(BroadsoftRequest, 'extract_payload')
    @unittest.mock.patch('broadsoft.requestobjects.lib.BroadsoftRequest.LogoutRequest.logout')
    @unittest.mock.patch.object(BroadsoftRequest, 'check_error')
    @unittest.mock.patch('requests.post')
    @unittest.mock.patch('broadsoft.requestobjects.lib.SoapEnvelope.SoapEnvelope.to_string')
    @unittest.mock.patch.object(BroadsoftRequest, 'to_string')
    @unittest.mock.patch.object(BroadsoftRequest, 'authenticate_and_login')
    def test_can_pass_auth_object(
            self, login_patch, ro_to_string_patch, envelop_to_string_patch, requests_post_patch, check_error_patch,
            logout_patch, extract_payload_patch
    ):
        class FakeAuthObject:
            def __init__(self):
                self.foo = 'var'

        f = FakeAuthObject()
        g = GroupAccessDeviceDeleteRequest(auth_object=f)
        self.assertEqual(f, g.auth_object)

    @unittest.mock.patch.object(BroadsoftRequest, 'extract_payload')
    @unittest.mock.patch('broadsoft.requestobjects.lib.BroadsoftRequest.LogoutRequest.logout')
    @unittest.mock.patch.object(BroadsoftRequest, 'check_error')
    @unittest.mock.patch('requests.post')
    @unittest.mock.patch('broadsoft.requestobjects.lib.SoapEnvelope.SoapEnvelope.to_string')
    @unittest.mock.patch.object(BroadsoftRequest, 'to_string')
    @unittest.mock.patch.object(BroadsoftRequest, 'authenticate_and_login')
    def test_can_pass_login_object(
            self, login_patch, ro_to_string_patch, envelop_to_string_patch, requests_post_patch, check_error_patch,
            logout_patch, extract_payload_patch
    ):
        class FakeLoginObject:
            def __init__(self):
                self.foo = 'var'

        f = FakeLoginObject()
        g = GroupAccessDeviceDeleteRequest(login_object=f)
        self.assertEqual(f, g.login_object)
