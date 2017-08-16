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

        u = UserServiceAssignListRequest(service_pack='powerpack')
        self.assertEqual('powerpack', u.service_pack)

    def test_validate(self):
        # no sip_user_id
        u = UserServiceAssignListRequest(services=['a', 'b'])
        with self.assertRaises(ValueError):
            u.validate()

        u = UserServiceAssignListRequest(service_pack='powerpack')
        with self.assertRaises(ValueError):
            u.validate()

        # no services, has sip_user_id
        u = UserServiceAssignListRequest(sip_user_id='6175551212@mit.edu')
        with self.assertRaises(ValueError):
            u.validate()

    def test_build_command_xml(self):
        u = UserServiceAssignListRequest()
        u.services = ['a']
        u.sip_user_id = '6175551212@broadsoft.mit.edu'
        cmd = u.build_command_xml()
        self.assertEqual(
            ET.tostring(cmd).decode('utf-8'),
            '<command xmlns="" xsi:type="UserServiceAssignListRequest">' +
            '<userId>6175551212@broadsoft.mit.edu</userId>' +
            '<serviceName>a</serviceName>' +
            '</command>'
        )

        u = UserServiceAssignListRequest()
        u.services = ['a','b']
        u.sip_user_id = '6175551212@broadsoft.mit.edu'
        cmd = u.build_command_xml()
        self.assertEqual(
            ET.tostring(cmd).decode('utf-8'),
            '<command xmlns="" xsi:type="UserServiceAssignListRequest">' +
            '<userId>6175551212@broadsoft.mit.edu</userId>' +
            '<serviceName>a</serviceName>' +
            '<serviceName>b</serviceName>' +
            '</command>'
        )

        u = UserServiceAssignListRequest()
        u.service_pack = 'powerpack'
        u.sip_user_id = '6175551212@broadsoft.mit.edu'
        cmd = u.build_command_xml()
        self.assertEqual(
            ET.tostring(cmd).decode('utf-8'),
            '<command xmlns="" xsi:type="UserServiceAssignListRequest">' +
            '<userId>6175551212@broadsoft.mit.edu</userId>' +
            '<servicePackName>powerpack</servicePackName>'
            '</command>'
        )