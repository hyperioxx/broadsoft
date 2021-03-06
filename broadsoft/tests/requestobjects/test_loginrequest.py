import unittest.mock
import xml.etree.ElementTree as ET

import broadsoft.requestobjects.lib.BroadsoftRequest
from broadsoft.requestobjects.lib.BroadsoftRequest import LoginRequest


def return_none(*args, **kwargs):
    return None


def return_xml(*args, **kwargs):
    class Response:
        def __init__(self):
            self.content = '<?xml version="1.0" encoding="UTF-8"?><soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><soapenv:Body><processOCIMessageResponse xmlns=""><ns1:processOCIMessageReturn xmlns:ns1="urn:com:broadsoft:webservice">&lt;?xml version=&quot;1.0&quot; encoding=&quot;UTF-8&quot;?&gt;\n&lt;BroadsoftDocument protocol=&quot;OCI&quot; xmlns=&quot;C&quot; xmlns:xsi=&quot;http://www.w3.org/2001/XMLSchema-instance&quot;&gt;&lt;sessionId xmlns=&quot;&quot;&gt;sesh&lt;/sessionId&gt;&lt;command echo=&quot;&quot; xsi:type=&quot;AuthenticationResponse&quot; xmlns=&quot;&quot;&gt;&lt;userId&gt;admMITapi&lt;/userId&gt;&lt;nonce&gt;1493647455426&lt;/nonce&gt;&lt;passwordAlgorithm&gt;MD5&lt;/passwordAlgorithm&gt;&lt;/command&gt;&lt;/BroadsoftDocument&gt;</ns1:processOCIMessageReturn></processOCIMessageResponse></soapenv:Body></soapenv:Envelope>'

    r = Response()
    return r


class TestBroadsoftLoginRequest(unittest.TestCase):
    def test_build_signed_password(self):
        class FakeAuth:
            def __init__(self):
                self.nonce = 'nonce'

        a = FakeAuth()
        i = broadsoft.requestobjects.lib.BroadsoftRequest.instance_factory()
        i.auth_object = a
        l = LoginRequest(broadsoftinstance=i)
        l.api_password = 'password'

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
        i = broadsoft.requestobjects.lib.BroadsoftRequest.instance_factory()
        i.auth_object = a
        l = LoginRequest(broadsoftinstance=i)
        # want to override fetching of uid/pw via creds
        l.api_user_id = 'userid'
        l.api_password = 'password'

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

        self.maxDiff = None
        xml = l.to_xml()
        self.assertEqual(
            '<BroadsoftDocument protocol="OCI" xmlns="C" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">' +
            '<sessionId xmlns="">' + l.broadsoftinstance.session_id + '</sessionId>'
            '<command xmlns="" xsi:type="LoginRequest14sp4">' +
            '<userId>' + l.api_user_id + '</userId>' +
            '<signedPassword>' + signed_pwd + '</signedPassword>' +
            '</command>' +
            '</BroadsoftDocument>',
            ET.tostring(xml).decode('utf-8')
        )

    @unittest.mock.patch('nistcreds.NistCreds.NistCreds.__init__', side_effect=return_none)
    def test_derive_creds(
            self,
            creds_patch
    ):
        # default (prod) instance
        l = LoginRequest(
            broadsoftinstance=broadsoft.requestobjects.lib.BroadsoftRequest.instance_factory())
        # will throw error since mocking creds fetch
        try:
            l.build_command_xml()
        except AttributeError:
            pass
        call = creds_patch.call_args_list[0]
        args, kwargs = call
        self.assertEqual('prod', kwargs['member'])

        # prod instance
        l = LoginRequest(broadsoftinstance=broadsoft.requestobjects.lib.BroadsoftRequest.instance_factory(instance='prod'))
        # will throw error since mocking creds fetch
        try:
            l.build_command_xml()
        except AttributeError:
            pass
        call = creds_patch.call_args_list[1]
        args, kwargs = call
        self.assertEqual('prod', kwargs['member'])

        # test instance
        l = LoginRequest(broadsoftinstance=broadsoft.requestobjects.lib.BroadsoftRequest.instance_factory(instance='test'))
        # will throw error since mocking creds fetch
        try:
            l.build_command_xml()
        except AttributeError:
            pass
        call = creds_patch.call_args_list[2]
        args, kwargs = call
        self.assertEqual('test', kwargs['member'])

        # test instance
        l = LoginRequest(
            broadsoftinstance=broadsoft.requestobjects.lib.BroadsoftRequest.instance_factory(instance='dev'))
        # will throw error since mocking creds fetch
        try:
            l.build_command_xml()
        except AttributeError:
            pass
        call = creds_patch.call_args_list[3]
        args, kwargs = call
        self.assertEqual('dev', kwargs['member'])
