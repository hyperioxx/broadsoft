import unittest.mock
import xml.etree.ElementTree as ET
from broadsoft.requestobjects.UserAddRequest import UserAddRequest


class TestBroadsoftUserAddRequest(unittest.TestCase):
    def test_build_user_id_from_kname_and_domain(self):
        kname = 'beaver'
        sip_user_id = 'timebeaver@mit.edu'

        u = UserAddRequest(kname=kname)
        self.assertEqual(kname + '@' + u.default_domain, u.sip_user_id)

        u = UserAddRequest(sip_user_id=sip_user_id)
        self.assertEqual(sip_user_id, u.sip_user_id)

        u = UserAddRequest(sip_user_id=sip_user_id, kname=kname)
        self.assertEqual(sip_user_id, u.sip_user_id)

        u = UserAddRequest()
        self.assertIsNone(u.sip_user_id)

    def test_derive_email_from_kname_as_needed(self):
        self.assertFalse("write this")

    def test_did_gets_converted(self):
        self.assertFalse("write this")

    def test_did_format_gets_validated(self):
        self.assertFalse("write this")

    def test_auto_password_generation(self):
        self.assertFalse("write this")

    def test_validation(self):
        self.assertFalse("write this")

    def test_can_override_default_group_id(self):
        u = UserAddRequest(group_id='blah')
        self.assertEqual('blah', u.group_id)

        u = UserAddRequest()
        self.assertEqual(u.default_group_id, u.group_id)

    def test_to_xml(self):
        target_xml = """<?xml version="1.0" encoding="ISO-8859-1"?>
<BroadsoftDocument protocol="OCI" xmlns="C" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
<sessionId xmlns="">sesh</sessionId>
<command xsi:type="UserAddRequest17sp4" xmlns="">
<serviceProviderId>ENT136</serviceProviderId>
<groupId>testgroup</groupId>
<userId>beaver@broadsoft-dev.mit.edu</userId>
<lastName>Beaver</lastName>
<firstName>Tim</firstName>
<callingLineIdLastName>Beaver</callingLineIdLastName>
<callingLineIdFirstName>Tim</callingLineIdFirstName>
<phoneNumber>6175551212</phoneNumber>
<password>123456789</password>
<emailAddress>beaver@mit.edu</emailAddress>
</command>
</BroadsoftDocument>"""

        u = UserAddRequest(group_id='testgroup', session_id='sesh', kname='beaver', last_name='Beaver', first_name='Tim',
                           did='617 555 1212', password='123456789')