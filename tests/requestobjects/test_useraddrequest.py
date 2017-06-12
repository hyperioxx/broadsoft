import unittest.mock
import xml.etree.ElementTree as ET
from broadsoft.lib import BroadsoftInstance
from broadsoft.requestobjects.UserAddRequest import UserAddRequest
from broadsoft.requestobjects.lib.BroadsoftRequest import BroadsoftRequest


class TestBroadsoftUserAddRequest(unittest.TestCase):
    @unittest.mock.patch.object(BroadsoftRequest, 'convert_phone_number')
    @unittest.mock.patch.object(UserAddRequest, 'validate')
    def test_did_gets_converted(
            self,
            validate_patch,
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

    def test_validation(self):
        """
        u = UserAddRequest(group_id='testgroup', session_id='sesh', last_name='Beaver',
                           first_name='Tim', email='beaver@mit.edu', sip_user_id='beaver@broadsoft-dev.mit.edu',
                           did='6175551212')
        """

        # no last_name
        u = UserAddRequest(group_id='testgroup', session_id='sesh',
                           first_name='Tim', email='beaver@mit.edu', sip_user_id='beaver@broadsoft-dev.mit.edu',
                           did='6175551212', sip_password='password')
        with self.assertRaises(ValueError):
            u.validate()

        # no first_name
        u = UserAddRequest(group_id='testgroup', session_id='sesh', last_name='Beaver',
                           email='beaver@mit.edu', sip_user_id='beaver@broadsoft-dev.mit.edu',
                           did='6175551212', sip_password='password')
        with self.assertRaises(ValueError):
            u.validate()

        # no did
        u = UserAddRequest(group_id='testgroup', session_id='sesh', last_name='Beaver',
                           first_name='Tim', email='beaver@mit.edu', sip_user_id='beaver@broadsoft-dev.mit.edu',
                           sip_password='password')
        with self.assertRaises(ValueError):
            u.validate()

        # no password
        u = UserAddRequest(group_id='testgroup', session_id='sesh', last_name='Beaver',
                           first_name='Tim', email='beaver@mit.edu', sip_user_id='beaver@broadsoft-dev.mit.edu',
                           did=6175551212)
        with self.assertRaises(ValueError):
            u.validate()

    def test_can_override_default_group_id(self):
        i = BroadsoftInstance.factory()
        u = UserAddRequest(group_id='blah', broadsoftinstance=i)
        self.assertEqual('blah', u.group_id)

        u = UserAddRequest(broadsoftinstance=i)
        self.assertEqual(i.group_id, u.group_id)

    def test_derive_email(self):
        u = UserAddRequest(kname='beaver')
        self.assertEqual('beaver@mit.edu', u.email)

        u = UserAddRequest(email='timb@gmail.com')
        self.assertEqual('timb@gmail.com', u.email)

        u = UserAddRequest(email='timb@gmail.com', kname='beaver')
        self.assertEqual('timb@gmail.com', u.email)

    def test_can_override_timezone(self):
        u = UserAddRequest()
        self.assertEqual(BroadsoftRequest.default_timezone, u.timezone)

        u = UserAddRequest(timezone='blah')
        self.assertEqual('blah', u.timezone)

    def test_to_xml(self):
        # with sip_password
        u = UserAddRequest(group_id='testgroup', session_id='sesh', kname='beaver', last_name='Beaver',
                           first_name='Tim', email='beaver@mit.edu', sip_user_id='6175551212@broadsoft.mit.edu',
                           did='617 555 1212', sip_password='123456789', broadsoftinstance=BroadsoftInstance.factory())

        target_xml = \
            '<command xmlns="" xsi:type="UserAddRequest17sp4">' + \
            '<serviceProviderId>ENT136</serviceProviderId>' + \
            '<groupId>testgroup</groupId>' + \
            '<userId>6175551212@broadsoft.mit.edu</userId>' + \
            '<lastName>Beaver</lastName>' + \
            '<firstName>Tim</firstName>' + \
            '<callingLineIdLastName>Beaver</callingLineIdLastName>' + \
            '<callingLineIdFirstName>Tim</callingLineIdFirstName>' + \
            '<phoneNumber>6175551212</phoneNumber>' + \
            '<password>123456789</password>' + \
            '<timeZone>' + u.timezone + '</timeZone>' + \
            '<emailAddress>beaver@mit.edu</emailAddress>' + \
            '</command>'

        xml = u.to_xml()
        command = xml.findall('.//command')[0]
        self.maxDiff = None
        self.assertEqual(target_xml, ET.tostring(command).decode('utf-8'))

    def test_did_can_be_integer(self):
        def test_to_xml(self):
            u = UserAddRequest(group_id='testgroup', session_id='sesh', kname='beaver', last_name='Beaver',
                               first_name='Tim', email='beaver@mit.edu',
                               did=6175551212, sip_password='123456789')
            xml = u.to_xml()
