import unittest.mock
import xml.etree.ElementTree as ET

from broadsoft.requestobjects.AuthenticationRequest import AuthenticationRequest


class TestBroadsoftAuthenticationRequest(unittest.TestCase):
    def test_authenticationrequest_to_xml_call(self):
        a = AuthenticationRequest()
        a.session_id = 'sesh'
        xml = a.to_xml()
        self.assertEqual(
            '<BroadsoftDocument protocol="' + a.protocol + '" xmlns="' + a.xmlns + '" xmlns:xsi="' + a.xmlns_xsi + '">' +
            '<sessionId xmlns="">' + a.session_id + '</sessionId>' +
            '<command xmlns="" xsi:type="' + a.command_name + '">' +
            '<userId>' + a.user_id + '</userId>' +
            '</command>' +
            '</BroadsoftDocument>',
            ET.tostring(element=xml).decode("utf-8")
        )
