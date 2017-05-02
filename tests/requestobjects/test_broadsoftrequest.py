import http.cookiejar
import unittest.mock
import xml.etree.ElementTree as ET

from broadsoft.requestobjects.auth.AuthenticationRequest import AuthenticationRequest
from broadsoft.requestobjects.GroupGetListInServiceProviderRequest import GroupGetListInServiceProviderRequest
from broadsoft.requestobjects.lib.BroadsoftRequest import BroadsoftRequest


def return_xml(*args, **kwargs):
    class Response:
        def __init__(self):
            self.content = '<ns0:Envelope xmlns:ns0="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns1="urn:com:broadsoft:webservice"><ns0:Body><processOCIMessageResponse><ns1:processOCIMessageReturn>&lt;?xml version="1.0" encoding="UTF-8"?&gt;\n&lt;BroadsoftDocument protocol="OCI" xmlns="C" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"&gt;&lt;sessionId xmlns=""&gt;None&lt;/sessionId&gt;&lt;command echo="" xsi:type="AuthenticationResponse" xmlns=""&gt;&lt;userId&gt;admMITapi&lt;/userId&gt;&lt;nonce&gt;1493661742798&lt;/nonce&gt;&lt;passwordAlgorithm&gt;MD5&lt;/passwordAlgorithm&gt;&lt;/command&gt;&lt;/BroadsoftDocument&gt;</ns1:processOCIMessageReturn></processOCIMessageResponse></ns0:Body></ns0:Envelope>'
            self.cookies = http.cookiejar.CookieJar()

    r = Response()
    return r


def return_xml_error(*args, **kwargs):
    class Response:
        def __init__(self):
            self.content = '<ns0:Envelope xmlns:ns0="http://schemas.xmlsoap.org/soap/envelope/"><ns0:Body><ns0:Fault><faultcode>soapenv:Server.generalException</faultcode><faultstring>INVALID_REQUEST</faultstring><faultactor>ProvisioningService</faultactor><detail><string>Cannot process any request before user is logged in.</string></detail></ns0:Fault></ns0:Body></ns0:Envelope>'
            self.cookies = http.cookiejar.CookieJar()

    r = Response()
    return r


class TestBroadsoftRequest(unittest.TestCase):
    def test_to_xml_call(self):
        x = BroadsoftRequest()
        x.default_domain = 'dd'
        x.session_id = 'seshy'

        (xml, cmd) = x.master_to_xml()
        self.assertEqual(
            '<BroadsoftDocument protocol="OCI" xmlns="C" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><sessionId xmlns="">' + x.session_id + '</sessionId></BroadsoftDocument>',
            ET.tostring(element=xml).decode("utf-8")
        )

    def test_convert_phone_number(self):
        self.assertEqual('617-555-1212', BroadsoftRequest.convert_phone_number(number='6175551212'))
        self.assertEqual('617-555-1212', BroadsoftRequest.convert_phone_number(number='617 555 1212'))
        self.assertEqual('617-555-1212', BroadsoftRequest.convert_phone_number(number='(617) 555-1212'))
        self.assertEqual('617-555-1212', BroadsoftRequest.convert_phone_number(number='(617)-555-1212'))

    def test_generate_session_id(self):
        b = BroadsoftRequest()
        self.assertRegex(b.session_id, r'^.+?,\d{4}\-\d{2}\-\d{2} \d{2}:\d{2}:\d{2}\.\d+,\d{10}$')

    def test_pass_session_id(self):
        b = BroadsoftRequest(session_id='sesh')
        self.assertEqual('sesh', b.session_id)

    def test_to_string(self):
        # to_string() lives in XmlRequest, but can never be called by it since there's no to_xml() for this parent
        # object. so we test with AuthenticationRequest

        a = AuthenticationRequest()
        a.session_id = 'sesh'

        # without urlencoding
        s = a.to_string(html_encode=False)
        self.assertEqual(
            '<?xml version="1.0" encoding="UTF-8"?><BroadsoftDocument protocol="OCI" xmlns="C" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><sessionId xmlns="">sesh</sessionId><command xmlns="" xsi:type="AuthenticationRequest"><userId>' + a.prod_api_user_id + '</userId></command></BroadsoftDocument>',
            s
        )

        # with urlencoding
        s = a.to_string(html_encode=True)
        self.assertEqual(
            '&lt;?xml version=&quot;1.0&quot; encoding=&quot;UTF-8&quot;?&gt;&lt;BroadsoftDocument protocol=&quot;OCI&quot; xmlns=&quot;C&quot; xmlns:xsi=&quot;http://www.w3.org/2001/XMLSchema-instance&quot;&gt;&lt;sessionId xmlns=&quot;&quot;&gt;sesh&lt;/sessionId&gt;&lt;command xmlns=&quot;&quot; xsi:type=&quot;AuthenticationRequest&quot;&gt;&lt;userId&gt;' + a.prod_api_user_id + '&lt;/userId&gt;&lt;/command&gt;&lt;/BroadsoftDocument&gt;',
            s
        )

    def test_extract_payload(self):
        # sending string
        response = '<?xml version="1.0" encoding="UTF-8"?><soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><soapenv:Body><processOCIMessageResponse xmlns=""><ns1:processOCIMessageReturn xmlns:ns1="urn:com:broadsoft:webservice">&lt;?xml version=&quot;1.0&quot; encoding=&quot;UTF-8&quot;?&gt;\n&lt;BroadsoftDocument protocol=&quot;OCI&quot; xmlns=&quot;C&quot; xmlns:xsi=&quot;http://www.w3.org/2001/XMLSchema-instance&quot;&gt;&lt;sessionId xmlns=&quot;&quot;&gt;sesh&lt;/sessionId&gt;&lt;command echo=&quot;&quot; xsi:type=&quot;AuthenticationResponse&quot; xmlns=&quot;&quot;&gt;&lt;userId&gt;admMITapi&lt;/userId&gt;&lt;nonce&gt;1493647455426&lt;/nonce&gt;&lt;passwordAlgorithm&gt;MD5&lt;/passwordAlgorithm&gt;&lt;/command&gt;&lt;/BroadsoftDocument&gt;</ns1:processOCIMessageReturn></processOCIMessageResponse></soapenv:Body></soapenv:Envelope>'
        payload = BroadsoftRequest.extract_payload(response=response)
        self.assertEqual(
            '<ns0:BroadsoftDocument xmlns:ns0="C" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" protocol="OCI"><sessionId>sesh</sessionId><command echo="" xsi:type="AuthenticationResponse"><userId>admMITapi</userId><nonce>1493647455426</nonce><passwordAlgorithm>MD5</passwordAlgorithm></command></ns0:BroadsoftDocument>',
            ET.tostring(element=payload).decode('utf-8')
        )

        # sending encoded
        response = '<?xml version="1.0" encoding="UTF-8"?><soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><soapenv:Body><processOCIMessageResponse xmlns=""><ns1:processOCIMessageReturn xmlns:ns1="urn:com:broadsoft:webservice">&lt;?xml version=&quot;1.0&quot; encoding=&quot;UTF-8&quot;?&gt;\n&lt;BroadsoftDocument protocol=&quot;OCI&quot; xmlns=&quot;C&quot; xmlns:xsi=&quot;http://www.w3.org/2001/XMLSchema-instance&quot;&gt;&lt;sessionId xmlns=&quot;&quot;&gt;sesh&lt;/sessionId&gt;&lt;command echo=&quot;&quot; xsi:type=&quot;AuthenticationResponse&quot; xmlns=&quot;&quot;&gt;&lt;userId&gt;admMITapi&lt;/userId&gt;&lt;nonce&gt;1493647455426&lt;/nonce&gt;&lt;passwordAlgorithm&gt;MD5&lt;/passwordAlgorithm&gt;&lt;/command&gt;&lt;/BroadsoftDocument&gt;</ns1:processOCIMessageReturn></processOCIMessageResponse></soapenv:Body></soapenv:Envelope>'
        response = response.encode('utf-8')
        payload = BroadsoftRequest.extract_payload(response=response)
        self.assertEqual(
            '<ns0:BroadsoftDocument xmlns:ns0="C" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" protocol="OCI"><sessionId>sesh</sessionId><command echo="" xsi:type="AuthenticationResponse"><userId>admMITapi</userId><nonce>1493647455426</nonce><passwordAlgorithm>MD5</passwordAlgorithm></command></ns0:BroadsoftDocument>',
            ET.tostring(element=payload).decode('utf-8')
        )

    @unittest.mock.patch('requests.post', side_effect=return_xml)
    def test_post_return_values(
            self,
            post_patch
    ):
        # to_string() lives in XmlRequest, but can never be called by it since there's no to_xml() for this parent
        # object. so we test with AuthenticationRequest

        # with extract_payload True
        self.maxDiff = None
        a = AuthenticationRequest()
        # last_response should start out unpopulated
        self.assertIsNone(a.last_response)
        a.session_id = 'sesh'
        p = a.post(extract_payload=True)
        self.assertEqual(
            '<ns0:BroadsoftDocument xmlns:ns0="C" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" protocol="OCI"><sessionId>None</sessionId><command echo="" xsi:type="AuthenticationResponse"><userId>admMITapi</userId><nonce>1493661742798</nonce><passwordAlgorithm>MD5</passwordAlgorithm></command></ns0:BroadsoftDocument>',
            ET.tostring(p).decode('utf-8')
        )
        # should also have populated last_response
        self.assertIsNotNone(a.last_response)

        # with extract_payload False
        a = AuthenticationRequest()
        a.session_id = 'sesh'
        p = a.post(extract_payload=False)
        self.assertEqual(
            '<ns0:Envelope xmlns:ns0="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns1="urn:com:broadsoft:webservice"><ns0:Body><processOCIMessageResponse><ns1:processOCIMessageReturn>&lt;?xml version="1.0" encoding="UTF-8"?&gt;\n&lt;BroadsoftDocument protocol="OCI" xmlns="C" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"&gt;&lt;sessionId xmlns=""&gt;None&lt;/sessionId&gt;&lt;command echo="" xsi:type="AuthenticationResponse" xmlns=""&gt;&lt;userId&gt;admMITapi&lt;/userId&gt;&lt;nonce&gt;1493661742798&lt;/nonce&gt;&lt;passwordAlgorithm&gt;MD5&lt;/passwordAlgorithm&gt;&lt;/command&gt;&lt;/BroadsoftDocument&gt;</ns1:processOCIMessageReturn></processOCIMessageResponse></ns0:Body></ns0:Envelope>',
            ET.tostring(p).decode('utf-8')
        )

    def test_check_error(self):
        fault_return = '<ns0:Envelope xmlns:ns0="http://schemas.xmlsoap.org/soap/envelope/"><ns0:Body><ns0:Fault><faultcode>soapenv:Server.generalException</faultcode><faultstring>INVALID_REQUEST</faultstring><faultactor>ProvisioningService</faultactor><detail><string>Cannot process any request before user is logged in.</string></detail></ns0:Fault></ns0:Body></ns0:Envelope>'
        error_return = """<?xml version="1.0" encoding="UTF-8"?><soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><soapenv:Body><processOCIMessageResponse xmlns=""><ns1:processOCIMessageReturn xmlns:ns1="urn:com:broadsoft:webservice">&lt;?xml version=&quot;1.0&quot; encoding=&quot;UTF-8&quot;?&gt;
&lt;BroadsoftDocument protocol=&quot;OCI&quot; xmlns=&quot;C&quot; xmlns:xsi=&quot;http://www.w3.org/2001/XMLSchema-instance&quot;&gt;&lt;sessionId xmlns=&quot;&quot;&gt;Chriss-MacBook-Pro-4.local,2017-05-02 15:02:04.406815,5088044364&lt;/sessionId&gt;&lt;command type=&quot;Error&quot; echo=&quot;&quot; xsi:type=&quot;c:ErrorResponse&quot; xmlns:c=&quot;C&quot; xmlns=&quot;&quot;&gt;&lt;summary&gt;[Error 6004] OCI XML Request validation error&lt;/summary&gt;&lt;summaryEnglish&gt;[Error 6004] OCI XML Request validation error&lt;/summaryEnglish&gt;&lt;detail&gt;&lt;![CDATA[Invalid xsi:type qname: 'LoginRequest' in element BroadsoftDocument@C
&lt;command xsi:type=&quot;LoginRequest&quot; echo=&quot;DA556300AF67EF366CA5540F85BF0717&quot; xmlns:xsi=&quot;http://www.w3.org/2001/XMLSchema-instance&quot;&gt;&lt;userId&gt;admMITapi&lt;/userId&gt;&lt;signedPassword&gt;e00f8bf77e8c4115b6f9b3fc31a47cff&lt;/signedPassword&gt;&lt;/command&gt;

]]&gt;&lt;/detail&gt;&lt;/command&gt;&lt;/BroadsoftDocument&gt;</ns1:processOCIMessageReturn></processOCIMessageResponse></soapenv:Body></soapenv:Envelope>
"""
        valid_return = '<ns0:Envelope xmlns:ns0="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns1="urn:com:broadsoft:webservice"><ns0:Body><processOCIMessageResponse><ns1:processOCIMessageReturn>&lt;?xml version="1.0" encoding="UTF-8"?&gt;\n&lt;BroadsoftDocument protocol="OCI" xmlns="C" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"&gt;&lt;sessionId xmlns=""&gt;None&lt;/sessionId&gt;&lt;command echo="" xsi:type="AuthenticationResponse" xmlns=""&gt;&lt;userId&gt;admMITapi&lt;/userId&gt;&lt;nonce&gt;1493661742798&lt;/nonce&gt;&lt;passwordAlgorithm&gt;MD5&lt;/passwordAlgorithm&gt;&lt;/command&gt;&lt;/BroadsoftDocument&gt;</ns1:processOCIMessageReturn></processOCIMessageResponse></ns0:Body></ns0:Envelope>'

        # pass fault as string
        with self.assertRaises(RuntimeError):
            b = BroadsoftRequest()
            b.check_error(response=fault_return)

        # pass error as string
        with self.assertRaises(RuntimeError):
            b = BroadsoftRequest()
            b.check_error(response=error_return)

        # pass valid as string
        b = BroadsoftRequest()
        b.check_error(response=valid_return)

    @unittest.mock.patch('requests.post', side_effect=return_xml_error)
    def test_find_error_in_post_call(
            self,
            post_patch
    ):
        # to_string() lives in XmlRequest, but can never be called by it since there's no to_xml() for this parent
        # object. so we test with AuthenticationRequest
        a = AuthenticationRequest()
        a.session_id = 'sesh'
        with self.assertRaises(RuntimeError):
            a.post()

    def test_derive_url_for_test_and_prod_envs(self):
        # default value for use_test
        b = BroadsoftRequest()
        self.assertEqual(b.api_url, b.prod_api_url)

        # use_test is False
        b = BroadsoftRequest(use_test=False)
        self.assertEqual(b.api_url, b.prod_api_url)

        # use_test is True
        b = BroadsoftRequest(use_test=True)
        self.assertEqual(b.api_url, b.test_api_url)

    @unittest.mock.patch('requests.post', side_effect=return_xml)
    def test_passing_cookies_when_present(
            self,
            post_patch
    ):
        class FakeAuth:
            def __init__(self):
                self.content = '<ns0:Envelope xmlns:ns0="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns1="urn:com:broadsoft:webservice"><ns0:Body><processOCIMessageResponse><ns1:processOCIMessageReturn>&lt;?xml version="1.0" encoding="UTF-8"?&gt;\n&lt;BroadsoftDocument protocol="OCI" xmlns="C" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"&gt;&lt;sessionId xmlns=""&gt;None&lt;/sessionId&gt;&lt;command echo="" xsi:type="AuthenticationResponse" xmlns=""&gt;&lt;userId&gt;admMITapi&lt;/userId&gt;&lt;nonce&gt;1493661742798&lt;/nonce&gt;&lt;passwordAlgorithm&gt;MD5&lt;/passwordAlgorithm&gt;&lt;/command&gt;&lt;/BroadsoftDocument&gt;</ns1:processOCIMessageReturn></processOCIMessageResponse></ns0:Body></ns0:Envelope>'
                self.auth_cookie_jar = http.cookiejar.CookieJar()

        f = FakeAuth()
        g = GroupGetListInServiceProviderRequest(auth_object=f, login_object=f)
        g.post()

        call = post_patch.call_args_list[0]
        args, kwargs = call
        self.assertIsNotNone(kwargs['cookies'])

    @unittest.mock.patch('requests.post', side_effect=return_xml)
    def test_derive_session_id_notices_when_auth_object_attached(
            self,
            post_patch
    ):
        a = AuthenticationRequest.authenticate()
        b = BroadsoftRequest(auth_object=a)
        self.assertEqual(a.session_id, b.session_id)

    def test_convert_results_table(self):
        xml = '<groupTable><colHeading>Group Id</colHeading><colHeading>Group Name</colHeading><colHeading>User Limit</colHeading><row><col>anothertestgroup</col><col>Another Test Group</col><col>25</col></row><row><col>sandbox</col><col /><col>25</col></row></groupTable>'
        xml = ET.fromstring(xml)
        data = BroadsoftRequest.convert_results_table(xml=xml)
        self.assertEqual(
            [{'Group Id': 'anothertestgroup', 'Group Name': 'Another Test Group', 'User Limit': '25'}, {'Group Id': 'sandbox', 'Group Name': None, 'User Limit': '25'}],
            data
        )
