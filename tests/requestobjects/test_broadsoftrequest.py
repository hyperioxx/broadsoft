import http.cookiejar
import unittest.mock
import xml.etree.ElementTree as ET
from broadsoft.requestobjects.GroupGetListInServiceProviderRequest import GroupGetListInServiceProviderRequest
from broadsoft.requestobjects.GroupAddRequest import GroupAddRequest
from broadsoft.requestobjects.UserAddRequest import UserAddRequest
from broadsoft.requestobjects.lib.BroadsoftRequest import BroadsoftRequest, AuthenticationRequest, LoginRequest

def return_none(*args, **kwargs):
    return None

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
    def test_convert_phone_number(self):
        self.assertEqual('6175551212', BroadsoftRequest.convert_phone_number(number='6175551212', dashes=False))
        self.assertEqual('6175551212', BroadsoftRequest.convert_phone_number(number='617 555 1212', dashes=False))
        self.assertEqual('6175551212', BroadsoftRequest.convert_phone_number(number='(617) 555-1212', dashes=False))
        self.assertEqual('6175551212', BroadsoftRequest.convert_phone_number(number='(617)-555-1212', dashes=False))
        self.assertEqual('617-555-1212', BroadsoftRequest.convert_phone_number(number='6175551212', dashes=True))
        self.assertEqual('617-555-1212', BroadsoftRequest.convert_phone_number(number='617 555 1212', dashes=True))
        self.assertEqual('617-555-1212', BroadsoftRequest.convert_phone_number(number='(617) 555-1212', dashes=True))
        self.assertEqual('617-555-1212', BroadsoftRequest.convert_phone_number(number='(617)-555-1212', dashes=True))

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
            '<?xml version="1.0" encoding="UTF-8"?><command xmlns="" xsi:type="AuthenticationRequest"><userId>' + a.api_user_id + '</userId></command>',
            s
        )

        # with urlencoding
        s = a.to_string(html_encode=True)
        self.assertEqual(
            '&lt;?xml version=&quot;1.0&quot; encoding=&quot;UTF-8&quot;?&gt;&lt;command xmlns=&quot;&quot; xsi:type=&quot;AuthenticationRequest&quot;&gt;&lt;userId&gt;' + a.api_user_id + '&lt;/userId&gt;&lt;/command&gt;',
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
            b.check_error(string_response=fault_return)

        # pass error as string
        with self.assertRaises(RuntimeError):
            b = BroadsoftRequest()
            b.check_error(string_response=error_return)

        # pass valid as string
        b = BroadsoftRequest()
        b.check_error(string_response=valid_return)

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

    def test_need_login(self):
        # with no attached auth or login objects, needs login
        g = GroupGetListInServiceProviderRequest()
        self.assertTrue(g.need_login())

        # with no attached auth object, needs login
        g = GroupGetListInServiceProviderRequest()
        g.login_object = 'test'
        self.assertTrue(g.need_login())

        # with no attached login object, needs login
        g = GroupGetListInServiceProviderRequest()
        g.auth_object = 'test'
        self.assertTrue(g.need_login())

        # with attached login/auth objects, don't need login
        g = GroupGetListInServiceProviderRequest()
        g.auth_object = 'test'
        g.login_object = 'test'
        self.assertFalse(g.need_login())

        # when command name is AuthenticationRequest, don't need login
        a = AuthenticationRequest()
        self.assertFalse(g.need_login())

        # when command name is LoginRequest14sp4, don't need login
        l = LoginRequest()
        self.assertFalse(l.need_login())

    @unittest.mock.patch.object(AuthenticationRequest, 'authenticate')
    @unittest.mock.patch.object(LoginRequest, 'login')
    def test_authenticate_and_login(
            self,
            login_patch,
            auth_patch
    ):
        b = BroadsoftRequest()
        b.authenticate_and_login()
        self.assertTrue(login_patch.called)
        self.assertTrue(auth_patch.called)

    @unittest.mock.patch.object(BroadsoftRequest, 'authenticate_and_login')
    @unittest.mock.patch('requests.post', side_effect=return_xml)
    def test_auto_login(
            self,
            post_patch,
            login_patch
    ):
        # with auto_login true and no attached auth objects, should auto login
        g = GroupGetListInServiceProviderRequest()
        g.post(auto_login=True)
        self.assertTrue(login_patch.called)
        login_patch.called = False

        # with auto_login false, should throw an error (and not login)
        g = GroupGetListInServiceProviderRequest()
        with self.assertRaises(RuntimeError):
            g.post(auto_login=False)
            self.assertFalse(login_patch.called)
        login_patch.called = False

        # with auto_login true and attached login objects, should not login
        class FakeAuth:
            def __init__(self):
                self.content = '<ns0:Envelope xmlns:ns0="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns1="urn:com:broadsoft:webservice"><ns0:Body><processOCIMessageResponse><ns1:processOCIMessageReturn>&lt;?xml version="1.0" encoding="UTF-8"?&gt;\n&lt;BroadsoftDocument protocol="OCI" xmlns="C" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"&gt;&lt;sessionId xmlns=""&gt;None&lt;/sessionId&gt;&lt;command echo="" xsi:type="AuthenticationResponse" xmlns=""&gt;&lt;userId&gt;admMITapi&lt;/userId&gt;&lt;nonce&gt;1493661742798&lt;/nonce&gt;&lt;passwordAlgorithm&gt;MD5&lt;/passwordAlgorithm&gt;&lt;/command&gt;&lt;/BroadsoftDocument&gt;</ns1:processOCIMessageReturn></processOCIMessageResponse></ns0:Body></ns0:Envelope>'
                self.auth_cookie_jar = http.cookiejar.CookieJar()
        a = FakeAuth()
        l = FakeAuth()
        g = GroupGetListInServiceProviderRequest(auth_object=a, login_object=l)
        g.post(auto_login=True)
        self.assertFalse(login_patch.called)
        login_patch.called = False

        # with auto_login false and attached login objects, should not login
        class FakeAuth:
            def __init__(self):
                self.content = '<ns0:Envelope xmlns:ns0="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns1="urn:com:broadsoft:webservice"><ns0:Body><processOCIMessageResponse><ns1:processOCIMessageReturn>&lt;?xml version="1.0" encoding="UTF-8"?&gt;\n&lt;BroadsoftDocument protocol="OCI" xmlns="C" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"&gt;&lt;sessionId xmlns=""&gt;None&lt;/sessionId&gt;&lt;command echo="" xsi:type="AuthenticationResponse" xmlns=""&gt;&lt;userId&gt;admMITapi&lt;/userId&gt;&lt;nonce&gt;1493661742798&lt;/nonce&gt;&lt;passwordAlgorithm&gt;MD5&lt;/passwordAlgorithm&gt;&lt;/command&gt;&lt;/BroadsoftDocument&gt;</ns1:processOCIMessageReturn></processOCIMessageResponse></ns0:Body></ns0:Envelope>'
                self.auth_cookie_jar = http.cookiejar.CookieJar()

        a = FakeAuth()
        l = FakeAuth()
        g = GroupGetListInServiceProviderRequest(auth_object=a, login_object=l)
        g.post(auto_login=False)
        self.assertFalse(login_patch.called)
        login_patch.called = False

    @unittest.mock.patch('nistcreds.NistCreds.NistCreds')
    def test_derive_creds_respects_auto_derive_creds(
            self,
            creds_patch
    ):
        b = BroadsoftRequest(auto_derive_creds=True)
        self.assertTrue(creds_patch.called)
        creds_patch.called = False

        b = BroadsoftRequest(auto_derive_creds=False)
        self.assertFalse(creds_patch.called)

    @unittest.mock.patch('nistcreds.NistCreds.NistCreds.__init__', side_effect=return_none)
    def test_derive_creds(
            self,
            creds_patch
    ):
        # use_test True
        b = BroadsoftRequest(use_test=True)
        call = creds_patch.call_args_list[0]
        args, kwargs = call
        self.assertEqual('test', kwargs['member'])

        # use_test False
        b = BroadsoftRequest(use_test=False)
        call = creds_patch.call_args_list[1]
        args, kwargs = call
        self.assertEqual('prod', kwargs['member'])

    def test_derive_domain_based_on_test_and_prod(self):
        b = BroadsoftRequest(use_test=False)
        self.assertEqual(b.prod_default_domain, b.default_domain)

        b = BroadsoftRequest(use_test=True)
        self.assertEqual(b.test_default_domain, b.default_domain)

    def test_add_and_edit_functions_should_test_for_success(self):
        success_response = '<?xml version="1.0" encoding="UTF-8"?><soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><soapenv:Body><processOCIMessageResponse xmlns=""><ns1:processOCIMessageReturn xmlns:ns1="urn:com:broadsoft:webservice">&lt;?xml version=&quot;1.0&quot; encoding=&quot;ISO-8859-1&quot;?&gt;&lt;BroadsoftDocument protocol=&quot;OCI&quot; xmlns=&quot;C&quot; xmlns:xsi=&quot;http://www.w3.org/2001/XMLSchema-instance&quot;&gt;&lt;sessionId xmlns=&quot;&quot;&gt;Chriss-MacBook-Pro-4.local,2017-05-03 19:23:06.900733,6698568134&lt;/sessionId&gt;&lt;command echo=&quot;&quot; xsi:type=&quot;c:SuccessResponse&quot; xmlns:c=&quot;C&quot; xmlns=&quot;&quot;/&gt;&lt;/BroadsoftDocument&gt;</ns1:processOCIMessageReturn></processOCIMessageResponse></soapenv:Body></soapenv:Envelope>'
        regular_response = '<?xml version="1.0" encoding="UTF-8"?><soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><soapenv:Body><processOCIMessageResponse xmlns=""><ns1:processOCIMessageReturn xmlns:ns1="urn:com:broadsoft:webservice">&lt;?xml version=&quot;1.0&quot; encoding=&quot;ISO-8859-1&quot;?&gt;&lt;BroadsoftDocument protocol=&quot;OCI&quot; xmlns=&quot;C&quot; xmlns:xsi=&quot;http://www.w3.org/2001/XMLSchema-instance&quot;&gt;&lt;sessionId xmlns=&quot;&quot;&gt;Chriss-MacBook-Pro-4.local,2017-05-03 19:23:06.900733,6698568134&lt;/sessionId&gt;&lt;command echo=&quot;&quot; xsi:type=&quot;c:whatever&quot; xmlns:c=&quot;C&quot; xmlns=&quot;&quot;/&gt;&lt;/BroadsoftDocument&gt;</ns1:processOCIMessageReturn></processOCIMessageResponse></soapenv:Body></soapenv:Envelope>'

        # with check_success no and a success payload, should go through without an exception raised
        b = BroadsoftRequest()
        b.check_success = False
        b.check_error(string_response=success_response)

        # with check_success no and a non-success payload, should go through without an exception raised
        b = BroadsoftRequest()
        b.check_success = False
        b.check_error(string_response=regular_response)

        # with check_success yes and a success payload, should go through without an exception raised
        b = BroadsoftRequest()
        b.check_success = True
        b.check_error(string_response=success_response)

        # with check_success yes and a non-success payload, should raise an exception
        b = BroadsoftRequest()
        b.check_success = True
        with self.assertRaises(RuntimeError):
            b.check_error(string_response=regular_response)

    def test_default_group_id(self):
        b = BroadsoftRequest(group_id='blah')
        self.assertEqual('blah', b.group_id)

        b = BroadsoftRequest()
        self.assertEqual(b.default_group_id, b.group_id)

        b = BroadsoftRequest(auto_derive_group_id=False)
        self.assertIsNone(b.group_id)

    def test_to_xml_with_no_contents(self):
        b = BroadsoftRequest()
        x = b.to_xml()
        self.assertEqual(
            '<BroadsoftDocument protocol="OCI" xmlns="C" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">' +
            '<sessionId xmlns="">' + b.session_id + '</sessionId>' +
            '</BroadsoftDocument>',
            ET.tostring(x).decode('utf-8')
        )

    def test_derive_commands(self):
        gg = GroupGetListInServiceProviderRequest()
        ga = GroupAddRequest()
        ga.group_id = 'newgroup'

        # instantiated a BroadsoftRequest object; expect to see contents of BroadsoftRequest.commands
        b = BroadsoftRequest()
        b.commands = [ga, gg]
        self.assertEqual([ga, gg], b.derive_commands())

        # not a BroadsoftRequest object; expect to see self
        self.assertEqual([ga], ga.derive_commands())

    def test_build_command_shell(self):
        # BroadsoftRequest doesn't have a command_name property, so we'll use UserAddRequest
        u = UserAddRequest()
        self.assertEqual(
            '<command xmlns="" xsi:type="' + u.command_name + '" />',
            ET.tostring(u.build_command_shell()).decode('utf-8')
        )

    def test_to_xml_with_attached_commands(self):
        gg = GroupGetListInServiceProviderRequest()
        ga = GroupAddRequest()
        ga.group_id = 'newgroup'

        b = BroadsoftRequest()
        b.commands = [ga, gg]

        x = b.to_xml()
        self.assertEqual(
            '<BroadsoftDocument protocol="OCI" xmlns="C" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">' +
            '<sessionId xmlns="">' + b.session_id + '</sessionId>' +
            '<command xmlns="" xsi:type="GroupAddRequest">' +
                '<serviceProviderId>' + ga.service_provider + '</serviceProviderId>' +
                '<groupId>newgroup</groupId>' +
                '<defaultDomain>' + ga.default_domain + '</defaultDomain>' +
                '<userLimit>' + str(ga.user_limit) + '</userLimit>' +
                '<callingLineIdName>newgroup Line</callingLineIdName>' +
                '<timeZone>' + ga.timezone + '</timeZone>' +
            '</command>' +
            '<command xmlns="" xsi:type="GroupGetListInServiceProviderRequest">' +
                '<serviceProviderId>' + gg.service_provider + '</serviceProviderId>' +
                '<responseSizeLimit>' + str(gg.response_size_limit) + '</responseSizeLimit>' +
            '</command>' +
            '</BroadsoftDocument>',
            ET.tostring(x).decode('utf-8')
        )
