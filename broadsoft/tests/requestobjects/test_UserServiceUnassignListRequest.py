import unittest.mock
import xml.etree.ElementTree as ET
from broadsoft.requestobjects.UserServiceUnassignListRequest import UserServiceUnassignListRequest


class TestBroadsoftUserServiceUnassignListRequest(unittest.TestCase):
    def test_assign_services(self):
        u = UserServiceUnassignListRequest(services=['a','b'])
        self.assertEqual(['a','b'], u.services)

        u = UserServiceUnassignListRequest(services='a')
        self.assertEqual(['a'], u.services)

        u = UserServiceUnassignListRequest()
        self.assertEqual([], u.services)

        u = UserServiceUnassignListRequest(service_pack='powerpack')
        self.assertEqual('powerpack', u.service_pack)

    def test_validate(self):
        # no sip_user_id
        u = UserServiceUnassignListRequest(services=['a', 'b'])
        with self.assertRaises(ValueError):
            u.validate()

        u = UserServiceUnassignListRequest(service_pack='powerpack')
        with self.assertRaises(ValueError):
            u.validate()

        # no services, has sip_user_id
        u = UserServiceUnassignListRequest(sip_user_id='6175551212@mit.edu')
        with self.assertRaises(ValueError):
            u.validate()

    def test_build_command_xml(self):
        # services as list length 1
        u = UserServiceUnassignListRequest()
        u.services = ['a']
        u.sip_user_id = '6175551212@broadsoft.mit.edu'
        cmd = u.build_command_xml()
        self.assertEqual(
            ET.tostring(cmd).decode('utf-8'),
            '<command xmlns="" xsi:type="UserServiceUnassignListRequest">' +
            '<userId>6175551212@broadsoft.mit.edu</userId>' +
            '<serviceName>a</serviceName>' +
            '</command>'
        )

        # services as list length 2
        u = UserServiceUnassignListRequest()
        u.services = ['a','b']
        u.sip_user_id = '6175551212@broadsoft.mit.edu'
        cmd = u.build_command_xml()
        self.assertEqual(
            ET.tostring(cmd).decode('utf-8'),
            '<command xmlns="" xsi:type="UserServiceUnassignListRequest">' +
            '<userId>6175551212@broadsoft.mit.edu</userId>' +
            '<serviceName>a</serviceName>' +
            '<serviceName>b</serviceName>' +
            '</command>'
        )

        # default blank services
        u = UserServiceUnassignListRequest()
        u.service_pack = 'powerpack'
        u.sip_user_id = '6175551212@broadsoft.mit.edu'
        cmd = u.build_command_xml()
        self.assertEqual(
            ET.tostring(cmd).decode('utf-8'),
            '<command xmlns="" xsi:type="UserServiceUnassignListRequest">' +
            '<userId>6175551212@broadsoft.mit.edu</userId>' +
            '<servicePackName>powerpack</servicePackName>'
            '</command>'
        )

        # explicitly set services to None
        u = UserServiceUnassignListRequest()
        u.services = None
        u.service_pack = 'powerpack'
        u.sip_user_id = '6175551212@broadsoft.mit.edu'
        cmd = u.build_command_xml()
        self.assertEqual(
            ET.tostring(cmd).decode('utf-8'),
            '<command xmlns="" xsi:type="UserServiceUnassignListRequest">' +
            '<userId>6175551212@broadsoft.mit.edu</userId>' +
            '<servicePackName>powerpack</servicePackName>'
            '</command>'
        )
