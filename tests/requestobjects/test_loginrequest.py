import unittest.mock
from broadsoft.requestobjects.lib.BroadsoftRequest import LoginRequest
import xml.etree.ElementTree as ET


def return_xml(*args, **kwargs):
    class Response:
        def __init__(self):
            self.content = '<?xml version="1.0" encoding="UTF-8"?><soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><soapenv:Body><processOCIMessageResponse xmlns=""><ns1:processOCIMessageReturn xmlns:ns1="urn:com:broadsoft:webservice">&lt;?xml version=&quot;1.0&quot; encoding=&quot;UTF-8&quot;?&gt;\n&lt;BroadsoftDocument protocol=&quot;OCI&quot; xmlns=&quot;C&quot; xmlns:xsi=&quot;http://www.w3.org/2001/XMLSchema-instance&quot;&gt;&lt;sessionId xmlns=&quot;&quot;&gt;sesh&lt;/sessionId&gt;&lt;command echo=&quot;&quot; xsi:type=&quot;AuthenticationResponse&quot; xmlns=&quot;&quot;&gt;&lt;userId&gt;admMITapi&lt;/userId&gt;&lt;nonce&gt;1493647455426&lt;/nonce&gt;&lt;passwordAlgorithm&gt;MD5&lt;/passwordAlgorithm&gt;&lt;/command&gt;&lt;/BroadsoftDocument&gt;</ns1:processOCIMessageReturn></processOCIMessageResponse></soapenv:Body></soapenv:Envelope>'

    r = Response()
    return r


class TestBroadsoftLoginRequest(unittest.TestCase):
    @unittest.mock.patch('requests.post', side_effect=return_xml)
    def test_login_request_passes_use_test(
            self,
            post_patch
    ):
        class FakeAuth:
            def __init__(self):
                self.nonce = 'nonce'

        a = FakeAuth()

        l = LoginRequest.authenticate_and_login(use_test=True, auth_object=a)
        self.assertTrue(l.use_test)

        l = LoginRequest.authenticate_and_login(use_test=False, auth_object=a)
        self.assertFalse(l.use_test)

    def test_build_signed_password(self):
        class FakeAuth:
            def __init__(self):
                self.nonce = 'nonce'

        a = FakeAuth()
        l = LoginRequest(auth_object=a)

        from hashlib import sha1, md5
        nonce = a.nonce
        password = l.api_password

        s = sha1()
        s.update(password.encode())
        sha_pwd = s.hexdigest()
        concat_pwd = nonce + ':' + sha_pwd
        m = md5()
        m.update(concat_pwd.encode())
        signed_pwd = m.hexdigest()

        self.assertEqual(
            l.build_signed_password(),
            signed_pwd
        )

    def test_to_xml(self):
        class FakeAuth:
            def __init__(self):
                self.nonce = 'nonce'

        a = FakeAuth()
        l = LoginRequest(auth_object=a)

        from hashlib import sha1, md5
        nonce = a.nonce
        password = l.api_password

        s = sha1()
        s.update(password.encode())
        sha_pwd = s.hexdigest()
        concat_pwd = nonce + ':' + sha_pwd
        m = md5()
        m.update(concat_pwd.encode())
        signed_pwd = m.hexdigest()

        xml = l.to_xml()
        cmd = xml.findall('.//command')[0]

        self.assertEqual(
            '<command xmlns="" xsi:type="LoginRequest14sp4">' +
            '<userId>' + l.api_user_id + '</userId>' +
            '<signedPassword>' + signed_pwd + '</signedPassword>' +
            '</command>',
            ET.tostring(cmd).decode('utf-8')
        )
