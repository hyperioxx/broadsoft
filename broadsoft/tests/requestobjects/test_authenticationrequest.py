import http.cookiejar
import unittest.mock
import xml.etree.ElementTree as ET

import broadsoft.requestobjects.lib.BroadsoftRequest
from broadsoft.requestobjects.lib.BroadsoftRequest import AuthenticationRequest


def return_none(*args, **kwargs):
    return None


def return_xml(*args, **kwargs):
    class Response:
        def __init__(self):
            self.content = '<?xml version="1.0" encoding="UTF-8"?><soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><soapenv:Body><processOCIMessageResponse xmlns=""><ns1:processOCIMessageReturn xmlns:ns1="urn:com:broadsoft:webservice">&lt;?xml version=&quot;1.0&quot; encoding=&quot;UTF-8&quot;?&gt;\n&lt;BroadsoftDocument protocol=&quot;OCI&quot; xmlns=&quot;C&quot; xmlns:xsi=&quot;http://www.w3.org/2001/XMLSchema-instance&quot;&gt;&lt;sessionId xmlns=&quot;&quot;&gt;sesh&lt;/sessionId&gt;&lt;command echo=&quot;&quot; xsi:type=&quot;AuthenticationResponse&quot; xmlns=&quot;&quot;&gt;&lt;userId&gt;admMITapi&lt;/userId&gt;&lt;nonce&gt;1493647455426&lt;/nonce&gt;&lt;passwordAlgorithm&gt;MD5&lt;/passwordAlgorithm&gt;&lt;/command&gt;&lt;/BroadsoftDocument&gt;</ns1:processOCIMessageReturn></processOCIMessageResponse></soapenv:Body></soapenv:Envelope>'
            self.cookies = http.cookiejar.CookieJar()
            self.status_code = 200

        def close(self):
            pass

    r = Response()
    return r


class TestBroadsoftAuthenticationRequest(unittest.TestCase):
    def test_authenticationrequest_to_xml_call(self):
        i = broadsoft.requestobjects.lib.BroadsoftRequest.instance_factory()
        i.session_id = 'sesh'
        a = AuthenticationRequest(broadsoftinstance=i)
        xml = a.to_xml()
        self.assertEqual(
            '<BroadsoftDocument protocol="OCI" xmlns="C" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">' +
            '<sessionId xmlns="">' + a.broadsoftinstance.session_id + '</sessionId>' +
            '<command xmlns="" xsi:type="' + a.command_name + '">' +
            '<userId>' + a.api_user_id + '</userId>' +
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

    @unittest.mock.patch('requests.post', side_effect=return_xml)
    def test_authenticate_call_stores_jsession_cookie(
            self,
            post_patch
    ):
        a = AuthenticationRequest.authenticate(broadsoftinstance=broadsoft.requestobjects.lib.BroadsoftRequest.instance_factory())
        self.assertIsNotNone(a.auth_cookie_jar)
        self.assertEqual('CookieJar', a.auth_cookie_jar.__class__.__name__)

    @unittest.mock.patch('nistcreds.NistCreds.NistCreds.__init__', side_effect=return_none)
    def test_derive_creds(
            self,
            creds_patch
    ):
        # implicit value for instance, should look up prod
        a = AuthenticationRequest(
            broadsoftinstance=broadsoft.requestobjects.lib.BroadsoftRequest.instance_factory())
        a.build_command_xml()
        call = creds_patch.call_args_list[0]
        args, kwargs = call
        self.assertEqual('prod', kwargs['member'])

        # instance is prod
        a = AuthenticationRequest(
            broadsoftinstance=broadsoft.requestobjects.lib.BroadsoftRequest.instance_factory(instance='prod'))
        a.build_command_xml()
        call = creds_patch.call_args_list[1]
        args, kwargs = call
        self.assertEqual('prod', kwargs['member'])

        # instance is test
        a = AuthenticationRequest(
            broadsoftinstance=broadsoft.requestobjects.lib.BroadsoftRequest.instance_factory(instance='test'))
        a.build_command_xml()
        call = creds_patch.call_args_list[2]
        args, kwargs = call
        self.assertEqual('test', kwargs['member'])

        # instance is test
        a = AuthenticationRequest(
            broadsoftinstance=broadsoft.requestobjects.lib.BroadsoftRequest.instance_factory(instance='dev'))
        a.build_command_xml()
        call = creds_patch.call_args_list[3]
        args, kwargs = call
        self.assertEqual('dev', kwargs['member'])
