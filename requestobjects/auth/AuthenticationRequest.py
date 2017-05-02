import xml.etree.ElementTree as ET
from broadsoft.requestobjects.lib.BroadsoftRequest import BroadsoftRequest


class AuthenticationRequest(BroadsoftRequest):
    command_name = 'AuthenticationRequest'

    def __init__(self, use_test=False, **kwargs):
        self.auth_cookie_jar = None
        self.nonce = None
        BroadsoftRequest.__init__(self, use_test=use_test, **kwargs)

    def to_xml(self):
        # master is the entire XML document, cmd is the command element inserted within, which this object will be
        # manipulating
        (master, cmd) = BroadsoftRequest.master_to_xml(self)

        uid = ET.SubElement(cmd, 'userId')
        uid.text = self.api_user_id

        return master

    @staticmethod
    def authenticate(**kwargs):
        a = AuthenticationRequest(**kwargs)
        payload = a.post()
        a.auth_cookie_jar = a.last_response.cookies
        a.nonce = AuthenticationRequest.extract_auth_token(payload=payload)
        return a

    @staticmethod
    def extract_auth_token(payload):
        # when successfully authenticate, auth token is encased inside a <nonce> element in the response payload
        token = payload.findall('./command/nonce')[0]
        return token.text