import unittest.mock
import xml.etree.ElementTree as ET
from broadsoft.requestobjects.UserAddRequest import UserAddRequest
from broadsoft.requestobjects.lib.BroadsoftRequest import BroadsoftRequest


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

    @unittest.mock.patch.object(BroadsoftRequest, 'convert_phone_number')
    def test_did_gets_converted(
            self,
            convert_phone_number_patch
    ):
        u = UserAddRequest(group_id='testgroup', session_id='sesh', kname='beaver', last_name='Beaver',
                           first_name='Tim', email='beaver@mit.edu',
                           did='617 555 1212', sip_password='123456789')
        u.to_xml()
        self.assertTrue(convert_phone_number_patch.called)

    def test_did_format_gets_validated(self):
        u = UserAddRequest(group_id='testgroup', session_id='sesh', kname='beaver', last_name='Beaver',
                           first_name='Tim', email='beaver@mit.edu',
                           did='617555121', sip_password='123456789')
        with self.assertRaises(ValueError):
            u.validate()

        u = UserAddRequest(group_id='testgroup', session_id='sesh', kname='beaver', last_name='Beaver',
                           first_name='Tim', email='beaver@mit.edu',
                           did='61755512111', sip_password='123456789')
        with self.assertRaises(ValueError):
            u.validate()

        u = UserAddRequest(group_id='testgroup', session_id='sesh', kname='beaver', last_name='Beaver',
                           first_name='Tim', email='beaver@mit.edu',
                           did='617555121x', sip_password='123456789')
        with self.assertRaises(ValueError):
            u.validate()

    def test_auto_password_generation(self):
        self.assertFalse("write this")

    def test_validation(self):
        self.assertFalse("write this")

    def test_can_override_default_group_id(self):
        u = UserAddRequest(group_id='blah')
        self.assertEqual('blah', u.group_id)

        u = UserAddRequest()
        self.assertEqual(u.default_group_id, u.group_id)

    def test_derive_email(self):
        u = UserAddRequest(kname='beaver')
        self.assertEqual('beaver@mit.edu', u.email)

        u = UserAddRequest(email='timb@gmail.com')
        self.assertEqual('timb@gmail.com', u.email)

        u = UserAddRequest(email='timb@gmail.com', kname='beaver')
        self.assertEqual('timb@gmail.com', u.email)

    def test_to_xml(self):
        u = UserAddRequest(group_id='testgroup', session_id='sesh', kname='beaver', last_name='Beaver',
                           first_name='Tim', email='beaver@mit.edu',
                           did='617 555 1212', sip_password='123456789')

        target_xml = \
            '<command xmlns="" xsi:type="UserAddRequest17sp4">' + \
            '<serviceProviderId>ENT136</serviceProviderId>' + \
            '<groupId>testgroup</groupId>' + \
            '<userId>beaver@' + u.default_domain + '</userId>' + \
            '<lastName>Beaver</lastName>' + \
            '<firstName>Tim</firstName>' + \
            '<callingLineIdLastName>Beaver</callingLineIdLastName>' + \
            '<callingLineIdFirstName>Tim</callingLineIdFirstName>' + \
            '<phoneNumber>6175551212</phoneNumber>' + \
            '<password>123456789</password>' + \
            '<emailAddress>beaver@mit.edu</emailAddress>' + \
            '</command>'

        xml = u.to_xml()
        command = xml.findall('.//command')[0]
        self.maxDiff = None
        self.assertEqual(target_xml, ET.tostring(command).decode('utf-8'))