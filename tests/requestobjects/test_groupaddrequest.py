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
        self.assertEqual(gar.group_name + ' Line', gar.derive_calling_line_id_name())

        gar.group_name = None
        self.assertEqual(gar.group_id + ' Line', gar.derive_calling_line_id_name())

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

    @unittest.mock.patch('broadsoft.requestobjects.lib.BroadsoftRequest.BroadsoftRequest.convert_phone_number')
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
            '<BroadsoftDocument protocol="OCI" xmlns="C" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">' +
            '<sessionId xmlns="">' + gar.session_id + '</sessionId>' +
            '<command xmlns="" xsi:type="' + gar.command_name + '">' +
            '<serviceProviderId>' + gar.service_provider + '</serviceProviderId>' +
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

    def test_use_test_gets_passed_to_broadsoftdocument(self):
        g = GroupAddRequest()
        self.assertEqual(g.prod_api_url, g.api_url)

        g = GroupAddRequest(use_test=False)
        self.assertEqual(g.prod_api_url, g.api_url)

        g = GroupAddRequest(use_test=True)
        self.assertEqual(g.test_api_url, g.api_url)

    def test_can_pass_session_id(self):
        g = GroupAddRequest(session_id='sesh')
        self.assertEqual('sesh', g.session_id)

    def test_can_pass_auth_object(self):
        class FakeAuthObject:
            def __init__(self):
                self.foo = 'var'

        f = FakeAuthObject()
        g = GroupAddRequest(auth_object=f)
        self.assertEqual(f, g.auth_object)

    def test_can_pass_login_object(self):
        class FakeLoginObject:
            def __init__(self):
                self.foo = 'var'

        f = FakeLoginObject()
        g = GroupAddRequest(login_object=f)
        self.assertEqual(f, g.login_object)
