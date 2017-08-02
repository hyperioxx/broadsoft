import unittest.mock
import xml.etree.ElementTree as ET

import broadsoft.requestobjects.lib.BroadsoftRequest
from broadsoft.requestobjects.GroupAccessDeviceGetRequest import GroupAccessDeviceGetRequest
from broadsoft.requestobjects.lib.BroadsoftRequest import BroadsoftRequest, LogoutRequest


def return_get_failure(*args, **kwargs):
    class Response:
        def __init__(self):
            self.content = """<?xml version="1.0" encoding="UTF-8"?><soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><soapenv:Body><processOCIMessageResponse xmlns=""><ns1:processOCIMessageReturn xmlns:ns1="urn:com:broadsoft:webservice">&lt;?xml version=&quot;1.0&quot; encoding=&quot;ISO-8859-1&quot;?&gt;&lt;BroadsoftDocument protocol=&quot;OCI&quot; xmlns=&quot;C&quot; xmlns:xsi=&quot;http://www.w3.org/2001/XMLSchema-instance&quot;&gt;&lt;sessionId xmlns=&quot;&quot;&gt;oc11-voipmgr-1.mit.edu,2017-08-02 21:29:39.751978,8258370762&lt;/sessionId&gt;&lt;command type=&quot;Error&quot; echo=&quot;&quot; xsi:type=&quot;c:ErrorResponse&quot; xmlns:c=&quot;C&quot; xmlns=&quot;&quot;&gt;&lt;summary&gt;[Error 4505] Access Device not found: blah&lt;/summary&gt;&lt;summaryEnglish&gt;[Error 4505] Access Device not found: blah&lt;/summaryEnglish&gt;&lt;/command&gt;&lt;/BroadsoftDocument&gt;</ns1:processOCIMessageReturn></processOCIMessageResponse></soapenv:Body></soapenv:Envelope>"""
            self.status_code = 200

        def close(self):
            pass

    r = Response()
    return r


def return_none(**kwargs):
    return None


class TestBroadsoftGroupAccessDeviceGetRequest(unittest.TestCase):
    def test_validate(self):
        g = GroupAccessDeviceGetRequest()
        with self.assertRaises(ValueError):
            g.validate()

    def test_to_xml(self):
        g = GroupAccessDeviceGetRequest(name='beaverphone', broadsoftinstance=broadsoft.requestobjects.lib.BroadsoftRequest.instance_factory())

        x = g.to_xml()
        self.maxDiff = None
        self.assertEqual(
            '<BroadsoftDocument protocol="OCI" xmlns="C" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">' +
                '<sessionId xmlns="">' + g.broadsoftinstance.session_id + '</sessionId>' +
                '<command xmlns="" xsi:type="GroupAccessDeviceGetRequest18sp1">' +
                    '<serviceProviderId>' + g.broadsoftinstance.service_provider + '</serviceProviderId>' +
                    '<groupId>' + g.group_id + '</groupId>' +
                    '<deviceName>' + g.name + '</deviceName>' +
                '</command>' +
            '</BroadsoftDocument>',
            ET.tostring(x).decode('utf-8')
        )

    def test_skip_fetch_error_should_be_true(self):
        g = GroupAccessDeviceGetRequest()
        self.assertTrue(g.skip_fetch_error)

    @unittest.mock.patch.object(LogoutRequest, 'logout')
    @unittest.mock.patch.object(BroadsoftRequest, 'authenticate_and_login')
    @unittest.mock.patch('requests.post', side_effect=return_get_failure)
    def test_fetch_with_no_results_ok(self, post_patch, login_patch, logout_patch):
        g = GroupAccessDeviceGetRequest(name='blah')
        # not testing for anything here per se, just expecting no exception thrown
        g.post()
