import xml.etree.ElementTree as ET

from broadsoft.requestobjects.lib.BroadsoftRequest import BroadsoftRequest


class AuthenticationRequest(BroadsoftRequest):
    command_name = 'AuthenticationRequest'
    prod_user_id = '[unknown]'
    test_user_id = 'admMITapi'

    def __init__(self, use_test=False, **kwargs):
        self.user_id = self.derive_user_id(use_test=use_test)
        BroadsoftRequest.__init__(self, use_test=use_test, **kwargs)

    def derive_user_id(self, use_test=False):
        if use_test:
            return self.test_user_id

        return self.prod_user_id

    def to_xml(self):
        # master is the entire XML document, cmd is the command element inserted within, which this object will be
        # manipulating
        (master, cmd) = BroadsoftRequest.master_to_xml(self)

        uid = ET.SubElement(cmd, 'userId')
        uid.text = self.user_id

        return master

    @staticmethod
    def authenticate(session_id=None, **kwargs):
        a = AuthenticationRequest(**kwargs)
        a.session_id = session_id
        payload = a.post()
        return AuthenticationRequest.extract_auth_token(payload=payload)

    @staticmethod
    def extract_auth_token(payload):
        # when successfully authenticate, auth token is encased inside a <nonce> element in the response payload
        token = payload.findall('./command/nonce')[0]
        return token.text