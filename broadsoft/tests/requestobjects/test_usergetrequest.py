import unittest.mock
import xml.etree.ElementTree as ET
from broadsoft.requestobjects.UserGetRequest import UserGetRequest
from broadsoft.requestobjects.lib.BroadsoftRequest import BroadsoftRequest, LogoutRequest


def return_get_failure(*args, **kwargs):
    class Response:
        def __init__(self):
            self.content = """<?xml version="1.0" encoding="UTF-8"?><soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><soapenv:Body><processOCIMessageResponse xmlns=""><ns1:processOCIMessageReturn xmlns:ns1="urn:com:broadsoft:webservice">&lt;?xml version=&quot;1.0&quot; encoding=&quot;ISO-8859-1&quot;?&gt;&lt;BroadsoftDocument protocol=&quot;OCI&quot; xmlns=&quot;C&quot; xmlns:xsi=&quot;http://www.w3.org/2001/XMLSchema-instance&quot;&gt;&lt;sessionId xmlns=&quot;&quot;&gt;oc11-voipmgr-1.mit.edu,2017-08-02 18:58:00.429056,5647647023&lt;/sessionId&gt;&lt;command type=&quot;Error&quot; echo=&quot;&quot; xsi:type=&quot;c:ErrorResponse&quot; xmlns:c=&quot;C&quot; xmlns=&quot;&quot;&gt;&lt;summary&gt;[Error 4008] User not found: 6172251560@broadsoft-dev.mit.edu&lt;/summary&gt;&lt;summaryEnglish&gt;[Error 4008] User not found: 6172251560@broadsoft-dev.mit.edu&lt;/summaryEnglish&gt;&lt;/command&gt;&lt;/BroadsoftDocument&gt;</ns1:processOCIMessageReturn></processOCIMessageResponse></soapenv:Body></soapenv:Envelope>"""
            self.status_code = 200

        def close(self):
            pass

    r = Response()
    return r

class TestBroadsoftUserGetRequest(unittest.TestCase):
    def test_validate(self):
        u = UserGetRequest()
        with self.assertRaises(ValueError):
            u.validate()

    def test_to_xml(self):
        u = UserGetRequest(sip_user_id='6175551212@broadsoft.mit.edu')

        x = u.to_xml()
        self.maxDiff = None
        self.assertEqual(
            '<BroadsoftDocument protocol="OCI" xmlns="C" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">' +
                '<sessionId xmlns="">' + u.broadsoftinstance.session_id + '</sessionId>' +
                '<command xmlns="" xsi:type="UserGetRequest21">' +
                    '<userId>' + u.sip_user_id + '</userId>' +
                '</command>' +
            '</BroadsoftDocument>',
            ET.tostring(x).decode('utf-8')
        )

    def test_skip_fetch_error_should_be_true(self):
        u = UserGetRequest()
        self.assertTrue(u.skip_fetch_error)

    @unittest.mock.patch.object(LogoutRequest, 'logout')
    @unittest.mock.patch.object(BroadsoftRequest, 'authenticate_and_login')
    @unittest.mock.patch('requests.post', side_effect=return_get_failure)
    def test_fetch_with_no_results_ok(self, post_patch, login_patch, logout_patch):
        u = UserGetRequest(sip_user_id='6175551212@broadsoft.mit.edu')
        # not testing for anything here per se, just expecting no exception thrown
        u.post()