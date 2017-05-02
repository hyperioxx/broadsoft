import unittest.mock
import xml.etree.ElementTree as ET

from broadsoft.requestobjects.LoginRequest import LoginRequest


def return_xml(*args, **kwargs):
    class Response:
        def __init__(self):
            self.content = '<?xml version="1.0" encoding="UTF-8"?><soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><soapenv:Body><processOCIMessageResponse xmlns=""><ns1:processOCIMessageReturn xmlns:ns1="urn:com:broadsoft:webservice">&lt;?xml version=&quot;1.0&quot; encoding=&quot;UTF-8&quot;?&gt;\n&lt;BroadsoftDocument protocol=&quot;OCI&quot; xmlns=&quot;C&quot; xmlns:xsi=&quot;http://www.w3.org/2001/XMLSchema-instance&quot;&gt;&lt;sessionId xmlns=&quot;&quot;&gt;sesh&lt;/sessionId&gt;&lt;command echo=&quot;&quot; xsi:type=&quot;AuthenticationResponse&quot; xmlns=&quot;&quot;&gt;&lt;userId&gt;admMITapi&lt;/userId&gt;&lt;nonce&gt;1493647455426&lt;/nonce&gt;&lt;passwordAlgorithm&gt;MD5&lt;/passwordAlgorithm&gt;&lt;/command&gt;&lt;/BroadsoftDocument&gt;</ns1:processOCIMessageReturn></processOCIMessageResponse></soapenv:Body></soapenv:Envelope>'

    r = Response()
    return r


class TestBroadsoftLoginRequest(unittest.TestCase):
    def test_login_request(self):
        self.assertFalse("write this")
