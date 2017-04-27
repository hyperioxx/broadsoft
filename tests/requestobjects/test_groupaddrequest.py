import unittest.mock
import xml.etree.ElementTree as ET

from broadsoft.requestobjects.GroupAddRequest import GroupAddRequest


class TestBroadsoftGroupAddRequest(unittest.TestCase):
    def test_derive_calling_line_id_name(self):
        gar = GroupAddRequest()
        gar.calling_line_id_name = 'calling line'
        gar.group_id = 'gid'
        gar.group_name = 'gname'

        self.assertEqual(gar.calling_line_id_name, gar.derive_calling_line_id_name())

        gar.calling_line_id_name = None
        self.assertEqual(gar.group_id + ' Line', gar.derive_calling_line_id_name())

        gar.group_id = None
        self.assertEqual(gar.group_name + ' Line', gar.derive_calling_line_id_name())

    def test_derive_build_contact(self):
        gar = GroupAddRequest()
        self.assertFalse(gar.derive_build_contact())

        gar.contact_name = 'test'
        self.assertTrue(gar.derive_build_contact())

        gar.contact_name = None
        gar.contact_email = 'test'
        self.assertTrue(gar.derive_build_contact())

        gar.contact_name = None
        gar.contact_email = None
        gar.contact_number = 'test'
        self.assertTrue(gar.derive_build_contact())

        gar.contact_name = 'test'
        gar.contact_email = None
        gar.contact_number = 'test'
        self.assertTrue(gar.derive_build_contact())

        gar.contact_name = None
        gar.contact_email = 'test'
        gar.contact_number = 'test'
        self.assertTrue(gar.derive_build_contact())

        gar.contact_name = 'test'
        gar.contact_email = 'test'
        gar.contact_number = 'test'
        self.assertTrue(gar.derive_build_contact())

    def test_groupaddrequest_to_xml_requires_groupid(self):
        gar = GroupAddRequest()
        with self.assertRaises(ValueError):
            gar.to_xml()

    @unittest.mock.patch('broadsoft.requestobjects.XmlRequest.XmlRequest.convert_phone_number')
    def test_groupaddrequest_to_xml_calls_convert_phone_number_when_number_present(
            self,
            convert_phone_number_patch
    ):
        gar = GroupAddRequest()
        gar.group_id = 'testgroup'
        gar.contact_number = '617 555 1212'
        gar.to_xml()
        self.assertTrue(convert_phone_number_patch.called)

    def test_groupaddrequest_to_xml_call(self):
        gar = GroupAddRequest()
        gar.calling_line_id_name = 'test line id'
        gar.contact_email = 'beaver@mit.edu'
        gar.contact_name = 'Tim Beaver'
        gar.contact_number = '617 555 1212'
        gar.group_id = 'testgroup'
        gar.group_name = 'test group'
        gar.user_limit = 100
        gar.session_id = 'seshy'

        xml = gar.to_xml()
        self.assertEqual(
            '<BroadsoftDocument protocol="' + gar.protocol + '" xmlns="' + gar.xmlns + '" xmlns:xsi="' + gar.xmlns_xsi + '">' +
            '<sessionId xmlns="">' + gar.session_id + '</sessionId>' +
            '<command xmlns="" xsi:type="' + gar.command_name + '">' +
            '<groupId>' + gar.group_id + '</groupId>' +
            '<defaultDomain>' + gar.default_domain + '</defaultDomain>' +
            '<userLimit>' + str(gar.user_limit) + '</userLimit>' +
            '<groupName>' + gar.group_name + '</groupName>' +
            '<callingLineIdName>' + gar.calling_line_id_name + '</callingLineIdName>' +
            '<timeZone>' + gar.timezone + '</timeZone>'
            '<contact>' +
            '<contactName>' + gar.contact_name + '</contactName>' +
            '<contactNumber>617-555-1212</contactNumber>' +
            '<contactEmail>' + gar.contact_email + '</contactEmail>' +
            '</contact>' +
            '</command>' +
            '</BroadsoftDocument>',
            ET.tostring(element=xml).decode("utf-8")
        )
