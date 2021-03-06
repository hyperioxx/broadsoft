import unittest.mock
import xml.etree.ElementTree as ET
from broadsoft.requestobjects.UserDeleteRequest import UserDeleteRequest
from broadsoft.requestobjects.lib.BroadsoftRequest import BroadsoftRequest


class TestBroadsoftUserDeleteRequest(unittest.TestCase):
    def test_validate(self):
        u = UserDeleteRequest()
        with self.assertRaises(ValueError):
            u.validate()

    def test_to_xml(self):
        u = UserDeleteRequest(sip_user_id='6175551212@broadsoft.mit.edu')

        x = u.to_xml()
        self.maxDiff = None
        self.assertEqual(
            '<BroadsoftDocument protocol="OCI" xmlns="C" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">' +
                '<sessionId xmlns="">' + u.broadsoftinstance.session_id + '</sessionId>' +
                '<command xmlns="" xsi:type="UserDeleteRequest">' +
                    '<userId>' + u.sip_user_id + '</userId>' +
                '</command>' +
            '</BroadsoftDocument>',
            ET.tostring(x).decode('utf-8')
        )
