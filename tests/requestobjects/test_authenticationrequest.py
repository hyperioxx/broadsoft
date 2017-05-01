import unittest.mock
import xml.etree.ElementTree as ET

from broadsoft.requestobjects.AuthenticationRequest import AuthenticationRequest


def return_xml(*args, **kwargs):
    class Response:
        def __init__(self):
            self.content = '<?xml version="1.0" encoding="UTF-8"?><soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><soapenv:Body><processOCIMessageResponse xmlns=""><ns1:processOCIMessageReturn xmlns:ns1="urn:com:broadsoft:webservice">&lt;?xml version=&quot;1.0&quot; encoding=&quot;UTF-8&quot;?&gt;\n&lt;BroadsoftDocument protocol=&quot;OCI&quot; xmlns=&quot;C&quot; xmlns:xsi=&quot;http://www.w3.org/2001/XMLSchema-instance&quot;&gt;&lt;sessionId xmlns=&quot;&quot;&gt;sesh&lt;/sessionId&gt;&lt;command echo=&quot;&quot; xsi:type=&quot;AuthenticationResponse&quot; xmlns=&quot;&quot;&gt;&lt;userId&gt;admMITapi&lt;/userId&gt;&lt;nonce&gt;1493647455426&lt;/nonce&gt;&lt;passwordAlgorithm&gt;MD5&lt;/passwordAlgorithm&gt;&lt;/command&gt;&lt;/BroadsoftDocument&gt;</ns1:processOCIMessageReturn></processOCIMessageResponse></soapenv:Body></soapenv:Envelope>'

    r = Response()
    return r


class TestBroadsoftAuthenticationRequest(unittest.TestCase):
    def test_authenticationrequest_to_xml_call(self):
        a = AuthenticationRequest()
        a.session_id = 'sesh'
        xml = a.to_xml()
        self.assertEqual(
            '<BroadsoftDocument protocol="OCI" xmlns="C" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">' +
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

    @unittest.mock.patch('requests.post', side_effect=return_xml)
    def test_authenticate_call_passes_session_id(
            self,
            post_patch
    ):
        session_id = 'test_authenticate_call_passes_session_id'
        AuthenticationRequest.authenticate(session_id=session_id)

        call = post_patch.call_args_list[0]
        args, kwargs = call

        self.assertTrue(
            '&lt;sessionId xmlns=""&gt;' + session_id + '&lt;/sessionId&gt;' in kwargs['data']
        )

    def test_derive_username_for_prod_and_dev(self):
        a = AuthenticationRequest()
        self.assertEqual(a.prod_user_id, a.derive_user_id())
        self.assertEqual(a.prod_user_id, a.derive_user_id(use_test=False))
        self.assertEqual(a.test_user_id, a.derive_user_id(use_test=True))

    def test_use_test_passed_to_derive_user_id_from_init(self):
        a = AuthenticationRequest()
        self.assertEqual(a.prod_user_id, a.user_id)

        a = AuthenticationRequest(use_test=False)
        self.assertEqual(a.prod_user_id, a.user_id)

        a = AuthenticationRequest(use_test=True)
        self.assertEqual(a.test_user_id, a.user_id)

    @unittest.mock.patch('requests.post', side_effect=return_xml)
    def test_authenticate_use_test_gets_passed_to_broadsoftdocument(
            self,
            post_patch
    ):
        # when calling AuthenticationRequest.__init__
        a = AuthenticationRequest()
        self.assertEqual(a.prod_url, a.api_url)

        a = AuthenticationRequest(use_test=False)
        self.assertEqual(a.prod_url, a.api_url)

        a = AuthenticationRequest(use_test=True)
        self.assertEqual(a.test_url, a.api_url)

        # when calling AuthenticationRequest.authenticate
        a = AuthenticationRequest.authenticate(session_id='test')
        call = post_patch.call_args_list[0]
        args, kwargs = call
        self.assertEqual(AuthenticationRequest.prod_url, kwargs['url'])

        a = AuthenticationRequest.authenticate(session_id='test', use_test=False)
        call = post_patch.call_args_list[1]
        args, kwargs = call
        self.assertEqual(AuthenticationRequest.prod_url, kwargs['url'])

        a = AuthenticationRequest.authenticate(session_id='test', use_test=True)
        call = post_patch.call_args_list[2]
        args, kwargs = call
        self.assertEqual(AuthenticationRequest.test_url, kwargs['url'])

    def test_can_pass_session_id(self):
        a = AuthenticationRequest(session_id='sesh')
        self.assertEqual('sesh', a.session_id)
