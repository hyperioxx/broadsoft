import xml.etree.ElementTree as ET
from broadsoft.requestobjects.lib.BroadsoftRequest import BroadsoftRequest
from hashlib import sha1, md5


class LoginRequest(BroadsoftRequest):
    command_name = 'LoginRequest14sp4'

    def __init__(self, use_test=False, **kwargs):
        BroadsoftRequest.__init__(self, use_test=use_test, **kwargs)

    def build_signed_password(self):
        # the signedPassword is convoluted
        # first, SHA encrypt password
        s = sha1()
        s.update(self.api_password.encode())
        sha_pwd = s.hexdigest()

        # now, combine the SHA passwd with the "nonce" value returned by the AuthenticationRequest and md5 it
        concat_pwd = self.auth_object.nonce + ':' + sha_pwd
        m = md5()
        m.update(concat_pwd.encode())
        signed_pwd = m.hexdigest()

        return signed_pwd

    def to_xml(self):
        # master is the entire XML document, cmd is the command element inserted within, which this object will be
        # manipulating
        (master, cmd) = BroadsoftRequest.master_to_xml(self)

        uid = ET.SubElement(cmd, 'userId')
        uid.text = self.api_user_id

        pwd = ET.SubElement(cmd, 'signedPassword')
        pwd.text = self.build_signed_password()

        return master

    @staticmethod
    def login(**kwargs):
        l = LoginRequest(**kwargs)
        l.post()
        return l