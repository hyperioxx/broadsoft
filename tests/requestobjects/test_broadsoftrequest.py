import unittest.mock
import xml.etree.ElementTree as ET
from broadsoft.requestobjects.BroadsoftRequest import BroadsoftRequest
from broadsoft.requestobjects.AuthenticationRequest import AuthenticationRequest


class TestBroadsoftRequest(unittest.TestCase):
    def test_to_xml_call(self):
        x = BroadsoftRequest()
        x.default_domain = 'dd'
        x.encoding = 'piglatin'
        x.protocol = 'gopher'
        x.session_id = 'seshy'
        x.version = '2.5'
        x.xmlns = 'PG13'
        x.xmlns_xsi = "http://youtube.com"

        (xml, cmd) = x.master_to_xml()
        self.assertEqual(
            '<BroadsoftDocument protocol="' + x.protocol + '" xmlns="' + x.xmlns + '" xmlns:xsi="' + x.xmlns_xsi + '"><sessionId xmlns="">' + x.session_id + '</sessionId></BroadsoftDocument>',
            ET.tostring(element=xml).decode("utf-8")
        )

    def test_convert_phone_number(self):
        self.assertEqual('617-555-1212', BroadsoftRequest.convert_phone_number(number='6175551212'))
        self.assertEqual('617-555-1212', BroadsoftRequest.convert_phone_number(number='617 555 1212'))
        self.assertEqual('617-555-1212', BroadsoftRequest.convert_phone_number(number='(617) 555-1212'))
        self.assertEqual('617-555-1212', BroadsoftRequest.convert_phone_number(number='(617)-555-1212'))

    def test_generate_session_id(self):
        self.assertFalse("write this")

    def test_to_string(self):
        # to_string() lives in XmlRequest, but can never be called by it since there's no to_xml() for this parent
        # object. so we test with AuthenticationRequest

        a = AuthenticationRequest()
        a.session_id = 'sesh'

        # without urlencoding
        s = a.to_string(html_encode=False)
        self.assertEqual(
            '<?xml version="1.0" encoding="UTF-8"?><BroadsoftDocument protocol="OCI" xmlns="C" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><sessionId xmlns="">sesh</sessionId><command xmlns="" xsi:type="AuthenticationRequest"><userId>admMITapi</userId></command></BroadsoftDocument>',
            s
        )

        # with urlencoding
        s = a.to_string(html_encode=True)
        self.assertEqual(
            '&lt;?xml version=&quot;1.0&quot; encoding=&quot;UTF-8&quot;?&gt;&lt;BroadsoftDocument protocol=&quot;OCI&quot; xmlns=&quot;C&quot; xmlns:xsi=&quot;http://www.w3.org/2001/XMLSchema-instance&quot;&gt;&lt;sessionId xmlns=&quot;&quot;&gt;sesh&lt;/sessionId&gt;&lt;command xmlns=&quot;&quot; xsi:type=&quot;AuthenticationRequest&quot;&gt;&lt;userId&gt;admMITapi&lt;/userId&gt;&lt;/command&gt;&lt;/BroadsoftDocument&gt;',
            s
        )

    def test_post_call(self):
        self.assertFalse("write this")