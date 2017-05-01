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

    def test_extract_auth_token(self):
        payload = '<ns0:BroadsoftDocument xmlns:ns0="C" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" protocol="OCI"><sessionId>sesh</sessionId><command echo="" xsi:type="AuthenticationResponse"><userId>admMITapi</userId><nonce>1493647455426</nonce><passwordAlgorithm>MD5</passwordAlgorithm></command></ns0:BroadsoftDocument>'
        payload = ET.fromstring(text=payload)
        self.assertEqual(
            '1493647455426',
            AuthenticationRequest.extract_auth_token(payload=payload)
        )

    def test_authenticate_call(self):
        self.assertFalse("write this")