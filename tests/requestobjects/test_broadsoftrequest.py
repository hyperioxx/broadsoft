import unittest.mock
import xml.etree.ElementTree as ET

from broadsoft.requestobjects.AuthenticationRequest import AuthenticationRequest
from broadsoft.requestobjects.lib.BroadsoftRequest import BroadsoftRequest


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

    def test_post_call(self):
        # with extract_payload true
        # with extract_payload false
        self.assertFalse("write this")

    def test_find_error_in_post_call(self):
        self.assertFalse("write this")

    def test_extract_payload_from_response(self):
        self.assertFalse("write this")

    def test_run_call(self):
        self.assertFalse("write this")