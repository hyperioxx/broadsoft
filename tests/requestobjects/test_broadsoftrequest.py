import http.cookiejar
import unittest
import unittest.mock
import xml.etree.ElementTree as ET

from broadsoft.lib import BroadsoftInstance
from broadsoft.requestobjects.GroupAddRequest import GroupAddRequest
from broadsoft.requestobjects.GroupGetListInServiceProviderRequest import GroupGetListInServiceProviderRequest
from broadsoft.requestobjects.UserAddRequest import UserAddRequest
from broadsoft.requestobjects.lib.BroadsoftRequest import BroadsoftRequest, AuthenticationRequest, LoginRequest, \
    LogoutRequest


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
        self.assertEqual('6175551212', BroadsoftRequest.convert_phone_number(number='+1-617-555-1212', dashes=False))
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
        self.assertRegex(b.broadsoftinstance.session_id, r'^.+?,\d{4}\-\d{2}\-\d{2} \d{2}:\d{2}:\d{2}\.\d+,\d{10}$')

    def test_to_string(self):
        # to_string() lives in XmlRequest, but can never be called by it since there's no to_xml() for this parent
        # object. so we test with AuthenticationRequest

        i = BroadsoftInstance.factory()
        i.session_id = 'sesh'
        a = AuthenticationRequest(broadsoftinstance=i)

        # without urlencoding
        s = a.to_string(html_encode=False)
        self.assertEqual(
            '<?xml version="1.0" encoding="UTF-8"?><BroadsoftDocument protocol="OCI" xmlns="C" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><sessionId xmlns="">sesh</sessionId><command xmlns="" xsi:type="AuthenticationRequest"><userId>' + a.api_user_id + '</userId></command></BroadsoftDocument>',
            s
        )

        # with urlencoding
        s = a.to_string(html_encode=True)
        self.assertEqual(
            '&lt;?xml version=&quot;1.0&quot; encoding=&quot;UTF-8&quot;?&gt;&lt;BroadsoftDocument protocol=&quot;OCI&quot; xmlns=&quot;C&quot; xmlns:xsi=&quot;http://www.w3.org/2001/XMLSchema-instance&quot;&gt;&lt;sessionId xmlns=&quot;&quot;&gt;sesh&lt;/sessionId&gt;&lt;command xmlns=&quot;&quot; xsi:type=&quot;AuthenticationRequest&quot;&gt;&lt;userId&gt;' + a.api_user_id + '&lt;/userId&gt;&lt;/command&gt;&lt;/BroadsoftDocument&gt;',
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
        i = BroadsoftInstance.factory()
        i.session_id = 'sesh'
        a = AuthenticationRequest(broadsoftinstance=i)
        # last_response should start out unpopulated
        self.assertIsNone(a.last_response)
        p = a.post(extract_payload=True)
        self.assertEqual(
            '<ns0:BroadsoftDocument xmlns:ns0="C" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" protocol="OCI"><sessionId>None</sessionId><command echo="" xsi:type="AuthenticationResponse"><userId>admMITapi</userId><nonce>1493661742798</nonce><passwordAlgorithm>MD5</passwordAlgorithm></command></ns0:BroadsoftDocument>',
            ET.tostring(p).decode('utf-8')
        )
        # should also have populated last_response
        self.assertIsNotNone(a.last_response)

        # with extract_payload False
        i = BroadsoftInstance.factory()
        i.session_id = 'sesh'
        a = AuthenticationRequest(broadsoftinstance=i)
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
        i = BroadsoftInstance.factory()
        i.session_id = 'sesh'
        a = AuthenticationRequest(broadsoftinstance=i)
        with self.assertRaises(RuntimeError):
            a.post()

    def test_derive_url_for_test_and_prod_envs(self):
        test_i = BroadsoftInstance.factory(use_test=True)
        prod_i = BroadsoftInstance.factory(use_test=False)
        default_i = BroadsoftInstance.factory()

        # use_test is default
        b = BroadsoftRequest(broadsoftinstance=default_i)
        self.assertEqual(b.broadsoftinstance.api_url, default_i.api_url)

        # use_test is False
        b = BroadsoftRequest(broadsoftinstance=prod_i)
        self.assertEqual(b.broadsoftinstance.api_url, prod_i.api_url)

        # use_test is True
        b = BroadsoftRequest(broadsoftinstance=test_i)
        self.assertEqual(b.broadsoftinstance.api_url, test_i.api_url)

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
        i = BroadsoftInstance.factory()
        i.auth_object = f
        i.login_object = f
        g = GroupGetListInServiceProviderRequest(broadsoftinstance=i)
        g.post()

        call = post_patch.call_args_list[0]
        args, kwargs = call
        self.assertIsNotNone(kwargs['cookies'])

    @unittest.mock.patch('requests.post', side_effect=return_xml)
    def test_derive_session_id_notices_when_auth_object_attached(
            self,
            post_patch
    ):
        i = BroadsoftInstance.factory()
        a = AuthenticationRequest.authenticate(broadsoftinstance=i)
        i.auth_object = a
        b = BroadsoftRequest(broadsoftinstance=i)
        self.assertEqual(a.broadsoftinstance.session_id, b.broadsoftinstance.session_id)

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
        i = BroadsoftInstance.factory()
        i.login_object = 'test'
        g = GroupGetListInServiceProviderRequest(broadsoftinstance=i)
        self.assertTrue(g.need_login())

        # with no attached login object, needs login
        i = BroadsoftInstance.factory()
        i.auth_object = 'test'
        g = GroupGetListInServiceProviderRequest(broadsoftinstance=i)
        self.assertTrue(g.need_login())

        # with attached login/auth objects, don't need login
        i = BroadsoftInstance.factory()
        i.auth_object = 'test'
        i.login_object = 'test'
        g = GroupGetListInServiceProviderRequest(broadsoftinstance=i)
        self.assertFalse(g.need_login())

        # when command name is AuthenticationRequest, don't need login
        a = AuthenticationRequest()
        self.assertFalse(a.need_login())

        # when command name is LoginRequest14sp4, don't need login
        l = LoginRequest()
        self.assertFalse(l.need_login())

        # when command name is LogoutRequest, don't need login
        l = LogoutRequest()
        self.assertFalse(l.need_login())

        # when command is BroadsoftRequest, and no auth/login object, need login
        b = BroadsoftRequest()
        self.assertTrue(b.need_login())

        # when command is BroadsoftRequest, and is auth/login object, don't need login
        i = BroadsoftInstance.factory()
        i.auth_object = 'test'
        i.login_object = 'test'
        b = BroadsoftRequest(broadsoftinstance=i)
        self.assertFalse(b.need_login())

    @unittest.mock.patch.object(AuthenticationRequest, 'authenticate')
    @unittest.mock.patch.object(LoginRequest, 'login')
    def test_authenticate_and_login(
            self,
            login_patch,
            auth_patch
    ):
        b = BroadsoftRequest(broadsoftinstance=BroadsoftInstance.factory())
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
        # with no attached auth objects, should auto login
        g = GroupGetListInServiceProviderRequest(broadsoftinstance=BroadsoftInstance.factory())
        g.post()
        self.assertTrue(login_patch.called)
        login_patch.called = False

        # with auto_login true and attached login objects, should not login
        class FakeAuth:
            def __init__(self):
                self.content = '<ns0:Envelope xmlns:ns0="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns1="urn:com:broadsoft:webservice"><ns0:Body><processOCIMessageResponse><ns1:processOCIMessageReturn>&lt;?xml version="1.0" encoding="UTF-8"?&gt;\n&lt;BroadsoftDocument protocol="OCI" xmlns="C" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"&gt;&lt;sessionId xmlns=""&gt;None&lt;/sessionId&gt;&lt;command echo="" xsi:type="AuthenticationResponse" xmlns=""&gt;&lt;userId&gt;admMITapi&lt;/userId&gt;&lt;nonce&gt;1493661742798&lt;/nonce&gt;&lt;passwordAlgorithm&gt;MD5&lt;/passwordAlgorithm&gt;&lt;/command&gt;&lt;/BroadsoftDocument&gt;</ns1:processOCIMessageReturn></processOCIMessageResponse></ns0:Body></ns0:Envelope>'
                self.auth_cookie_jar = http.cookiejar.CookieJar()
        a = FakeAuth()
        l = FakeAuth()
        i = BroadsoftInstance.factory()
        i.auth_object = a
        i.login_object = l
        g = GroupGetListInServiceProviderRequest(broadsoftinstance=i)
        g.post()
        self.assertFalse(login_patch.called)
        login_patch.called = False

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
        i = BroadsoftInstance.factory()
        b = BroadsoftRequest(group_id='blah', broadsoftinstance=i)
        self.assertEqual('blah', b.group_id)

        b = BroadsoftRequest(broadsoftinstance=i)
        self.assertEqual(i.default_group_id, b.group_id)

    def test_to_xml_with_no_contents(self):
        b = BroadsoftRequest()
        x = b.to_xml()
        self.assertEqual(
            '<BroadsoftDocument protocol="OCI" xmlns="C" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">' +
            '<sessionId xmlns="">' + b.broadsoftinstance.session_id + '</sessionId>' +
            '</BroadsoftDocument>',
            ET.tostring(x).decode('utf-8')
        )

    def test_derive_commands(self):
        gg = GroupGetListInServiceProviderRequest(broadsoftinstance=BroadsoftInstance.factory())
        ga = GroupAddRequest(broadsoftinstance=BroadsoftInstance.factory())
        ga.group_id = 'newgroup'

        # instantiated a BroadsoftRequest object; expect to see contents of BroadsoftRequest.commands
        b = BroadsoftRequest(broadsoftinstance=BroadsoftInstance.factory())
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
        gg = GroupGetListInServiceProviderRequest(broadsoftinstance=BroadsoftInstance.factory())
        ga = GroupAddRequest(broadsoftinstance=BroadsoftInstance.factory())
        ga.default_domain = 'broadsoft.mit.edu'
        ga.group_id = 'newgroup'

        b = BroadsoftRequest(broadsoftinstance=BroadsoftInstance.factory())
        b.commands = [ga, gg]

        x = b.to_xml()
        self.assertEqual(
            '<BroadsoftDocument protocol="OCI" xmlns="C" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">' +
            '<sessionId xmlns="">' + b.broadsoftinstance.session_id + '</sessionId>' +
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

    def test_convert_booleans_when_present(self):
        class FakeRequest(BroadsoftRequest):
            booleans = ['a', 'b', 'c']

            def __init__(self):
                self.a = True
                self.b = False
                self.c = 'hi'

        f = FakeRequest()
        f.convert_booleans()

        self.assertEqual('true', f.a)
        self.assertEqual('false', f.b)
        self.assertEqual('true', f.c)

    def test_convert_booleans_when_not_present(self):
        class FakeRequest(BroadsoftRequest):
            def __init__(self):
                self.a = True
                self.b = False
                self.c = 'hi'

        f = FakeRequest()

        # should invoke without error or effect
        f.convert_booleans()
        self.assertTrue(f.a)
        self.assertFalse(f.b)
        self.assertEqual('hi', f.c)

    @unittest.mock.patch.object(BroadsoftRequest, 'convert_booleans')
    def test_to_xml_calls_convert_booleans(
            self,
            convert_booleans_patch
    ):
        b = BroadsoftRequest()
        b.to_xml()
        self.assertTrue(convert_booleans_patch.called)

    def test_need_logout(self):
        class FakeRequest(BroadsoftRequest):
            command_name = 'BogusRequest'

            def __init__(self, **kwargs):
                self.a = True
                self.b = False
                self.c = 'hi'
                BroadsoftRequest.__init__(self, **kwargs)

            def build_command_xml(self):
                cmd = self.build_command_shell()
                return cmd

        logout_i = BroadsoftInstance.factory()
        logout_i.auto_logout = True

        no_logout_i = BroadsoftInstance.factory()
        no_logout_i.auto_logout = False

        # with a non-login related function, need_logout() depends on broadsoftinstance.auto_logout
        f = FakeRequest(broadsoftinstance=logout_i)
        self.assertTrue(f.need_logout())

        f = FakeRequest(broadsoftinstance=no_logout_i)
        self.assertFalse(f.need_logout())

        # with a login related function, need_logout() is always False
        l = LoginRequest(broadsoftinstance=logout_i)
        self.assertFalse(l.need_logout())

        l = LoginRequest(broadsoftinstance=no_logout_i)
        self.assertFalse(l.need_logout())

    def test_extract_payload_returns_none_for_empty_results(self):
        response = '<?xml version="1.0" encoding="UTF-8"?><soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><soapenv:Body><processOCIMessageResponse xmlns=""><ns1:processOCIMessageReturn xmlns:ns1="urn:com:broadsoft:webservice"></ns1:processOCIMessageReturn></processOCIMessageResponse></soapenv:Body></soapenv:Envelope>'
        self.assertIsNone(BroadsoftRequest.extract_payload(response=response))

    @unittest.mock.patch.object(LogoutRequest, 'logout')
    @unittest.mock.patch.object(BroadsoftRequest, 'need_logout')
    @unittest.mock.patch.object(BroadsoftRequest, 'authenticate_and_login')
    @unittest.mock.patch('requests.post', side_effect=return_xml)
    def test_need_logout_patch_called(
            self,
            post_patch,
            login_patch,
            need_logout_patch,
            logout_patch
    ):
        # should call need_logout
        g = GroupGetListInServiceProviderRequest(broadsoftinstance=BroadsoftInstance.factory())
        g.post()
        self.assertTrue(need_logout_patch.called)

    def test_is_auth_suite(self):
        # BroadsoftRequest is no
        b = BroadsoftRequest(broadsoftinstance=BroadsoftInstance.factory())
        self.assertFalse(b.is_auth_suite())

        # LoginRequest is yes
        lo = LoginRequest(broadsoftinstance=BroadsoftInstance.factory())
        self.assertTrue(lo.is_auth_suite())

        # LogoutRequest is yes
        lo = LogoutRequest(broadsoftinstance=BroadsoftInstance.factory())
        self.assertTrue(lo.is_auth_suite())

        # AuthenticationRequest is yes
        a = AuthenticationRequest(broadsoftinstance=BroadsoftInstance.factory())
        self.assertTrue(a.is_auth_suite())

        # new one with command_name is no
        class FakeRequest(BroadsoftRequest):
            command_name = 'BogusRequest'

            def __init__(self, **kwargs):
                self.a = True
                self.b = False
                self.c = 'hi'
                BroadsoftRequest.__init__(self, **kwargs)

            def build_command_xml(self):
                cmd = self.build_command_shell()
                return cmd
        f = FakeRequest()
        self.assertFalse(f.is_auth_suite())

    @unittest.mock.patch.object(BroadsoftRequest, 'convert_booleans')
    def test_embedded_commands_get_convert_booleans_called(
            self,
            convert_booleans_patch
    ):
        b = BroadsoftRequest(broadsoftinstance=BroadsoftInstance.factory())
        g = GroupGetListInServiceProviderRequest(broadsoftinstance=BroadsoftInstance.factory())
        u = UserAddRequest(did=6175551212, sip_user_id='6175551212@broadsoft.mit.edu', first_name='tim',
                           last_name='beaver', sip_password='password', broadsoftinstance=BroadsoftInstance.factory())
        b.commands = [g,u]
        b.to_xml()

        # expect to see 3 calls to convert_booleans: one for BroadsoftRequest, and one for each of the
        # two nested commands
        self.assertEqual(3, len(convert_booleans_patch.call_args_list))

    def test_apply_broadsoft_instance(self):
        # none of the BroadsoftInstance properties set
        bi = BroadsoftInstance.BroadsoftInstance()
        b = BroadsoftRequest(broadsoftinstance=bi)
        self.assertEqual(b.broadsoftinstance.api_url, bi.api_url)
        self.assertEqual(b.broadsoftinstance.creds_member, bi.creds_member)
        self.assertEqual(b.service_provider, bi.service_provider)
        self.assertEqual(b.group_id, bi.group_id)

        # all of the BroadsoftInstance properties set
        bi = BroadsoftInstance.BroadsoftInstance()
        b = BroadsoftRequest(broadsoftinstance=bi, service_provider='3', group_id='4')
        self.assertEqual(b.service_provider, '3')
        self.assertEqual(b.group_id, '4')

        # when forced should overwrite
        bi = BroadsoftInstance.BroadsoftInstance()
        b = BroadsoftRequest(broadsoftinstance=bi, service_provider='3', group_id='4')
        b.apply_broadsoftinstance(force=True)
        self.assertEqual(b.service_provider, bi.service_provider)
        self.assertEqual(b.group_id, bi.group_id)

    @unittest.mock.patch.object(BroadsoftRequest, 'apply_broadsoftinstance')
    def test_apply_broadsoft_instance_in_prep_attributes(
            self, apply_broadsoftinstance_patch):
        bi = BroadsoftInstance.BroadsoftInstance()
        b = BroadsoftRequest(broadsoftinstance=bi)
        apply_broadsoftinstance_patch.called = False
        b.prep_attributes()
        self.assertTrue(apply_broadsoftinstance_patch.called)

    def test_broadsoftinstance_needed(self):
        # has broadsoftinstance set
        b = BroadsoftRequest(broadsoftinstance=BroadsoftInstance.factory())
        self.assertFalse(b.broadsoftinstance_needed())

        # has a relevant property set
        for p in BroadsoftRequest.broadsoftinstance_properties:
            b = BroadsoftRequest()
            setattr(b, p, 'blah')
            self.assertFalse(b.broadsoftinstance_needed())

        # otherwise
        b = BroadsoftRequest()
        b.broadsoftinstance = None
        for p in BroadsoftRequest.broadsoftinstance_properties:
            setattr(b, p, None)
        self.assertTrue(b.broadsoftinstance_needed())

    def test_when_no_broadsoftinstance_or_relevant_attributes_set_use_default_broadsoft_instance(self):
        b = BroadsoftRequest()
        self.assertIsInstance(b.broadsoftinstance, BroadsoftInstance.BroadsoftInstance)
