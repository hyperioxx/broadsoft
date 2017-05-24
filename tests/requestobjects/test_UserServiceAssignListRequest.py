import unittest.mock
import xml.etree.ElementTree as ET
from broadsoft.requestobjects.UserServiceAssignListRequest import UserServiceAssignListRequest


class TestBroadsoftUserServiceAssignListRequest(unittest.TestCase):
    def test_assign_services(self):
        u = UserServiceAssignListRequest(services=['a','b'])
        self.assertEqual(['a','b'], u.services)

        u = UserServiceAssignListRequest(services='a')
        self.assertEqual(['a'], u.services)

        u = UserServiceAssignListRequest()
        self.assertEqual([], u.services)

    def test_derive_sip_user_id_at_init(self):
        # derives from did when not specified
        u = UserServiceAssignListRequest(did='617-555-1212')
        self.assertEqual('6175551212@' + u.default_domain, u.sip_user_id)

        # when specified, wins
        u = UserServiceAssignListRequest(did='617-555-1212', sip_user_id='beaver@mit.edu')
        self.assertEqual('beaver@mit.edu', u.sip_user_id)

    def test_derive_sip_user_id_at_build_command_xml(self):
        # derives from did when not specified
        u = UserServiceAssignListRequest()
        u.services = ['a']
        u.did = '617-555-1212'
        u.build_command_xml()
        self.assertEqual('6175551212@' + u.default_domain, u.sip_user_id)

        # when specified, wins
        u = UserServiceAssignListRequest()
        u.services = ['a']
        u.did = '617-555-1212'
        u.sip_user_id = 'beaver@mit.edu'
        u.build_command_xml()
        self.assertEqual('beaver@mit.edu', u.sip_user_id)

    def test_validate(self):
        # no DID or sip_user_id
        u = UserServiceAssignListRequest(services=['a', 'b'])
        with self.assertRaises(ValueError):
            u.validate()

        # no services, has did
        u = UserServiceAssignListRequest(did=6175551212)
        with self.assertRaises(ValueError):
            u.validate()

        # no services, has sip_user_id
        u = UserServiceAssignListRequest(sip_user_id='6175551212@mit.edu')
        with self.assertRaises(ValueError):
            u.validate()

    def test_build_command_xml(self):
        u = UserServiceAssignListRequest()
        u.services = ['a']
        u.did = 6175551212
        cmd = u.build_command_xml()
        self.assertEqual(
            ET.tostring(cmd).decode('utf-8'),
            '<command xmlns="" xsi:type="UserServiceAssignListRequest">' +
            '<userId>6175551212@' + u.default_domain + '</userId>' +
            '<serviceName>a</serviceName>' +
            '</command>'
        )

        u = UserServiceAssignListRequest()
        u.services = ['a','b']
        u.did = 6175551212
        cmd = u.build_command_xml()
        self.assertEqual(
            ET.tostring(cmd).decode('utf-8'),
            '<command xmlns="" xsi:type="UserServiceAssignListRequest">' +
            '<userId>6175551212@' + u.default_domain + '</userId>' +
            '<serviceName>a</serviceName>' +
            '<serviceName>b</serviceName>' +
            '</command>'
        )