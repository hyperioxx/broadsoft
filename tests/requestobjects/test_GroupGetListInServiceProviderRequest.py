import unittest.mock
import xml.etree.ElementTree as ET
from broadsoft.requestobjects.GroupGetListInServiceProviderRequest import GroupGetListInServiceProviderRequest

def return_groups_list(**kwargs):
    return '<ns0:BroadsoftDocument xmlns:ns0="C" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" protocol="OCI"><sessionId>Chriss-MacBook-Pro-4.local,2017-05-02 17:31:34.373071,3810609302</sessionId><command echo="" xsi:type="GroupGetListInServiceProviderResponse"><groupTable><colHeading>Group Id</colHeading><colHeading>Group Name</colHeading><colHeading>User Limit</colHeading><row><col>anothertestgroup</col><col>Another Test Group</col><col>25</col></row><row><col>sandbox</col><col /><col>25</col></row></groupTable></command></ns0:BroadsoftDocument>'

class TestBroadsoftGroupGetListInServiceProviderRequest(unittest.TestCase):
    def test_to_xml(self):
        # group id/case insensitive True
        g = GroupGetListInServiceProviderRequest()

        x = g.to_xml()
        self.maxDiff = None
        self.assertEqual(
            '<BroadsoftDocument protocol="OCI" xmlns="C" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">' +
                '<sessionId xmlns="">' + g.session_id + '</sessionId>' +
                '<command xmlns="" xsi:type="GroupGetListInServiceProviderRequest">' +
                    '<serviceProviderId>' + g.service_provider + '</serviceProviderId>' +
                    '<responseSizeLimit>' + str(g.response_size_limit) + '</responseSizeLimit>' +
                '</command>' +
            '</BroadsoftDocument>',
            ET.tostring(x).decode('utf-8')
        )

    def test_use_test_gets_passed_to_broadsoftdocument(self):
        g = GroupGetListInServiceProviderRequest()
        self.assertEqual(g.prod_api_url, g.api_url)

        g = GroupGetListInServiceProviderRequest(use_test=False)
        self.assertEqual(g.prod_api_url, g.api_url)

        g = GroupGetListInServiceProviderRequest(use_test=True)
        self.assertEqual(g.test_api_url, g.api_url)

    def test_can_pass_session_id(self):
        g = GroupGetListInServiceProviderRequest(session_id='sesh')
        self.assertEqual('sesh', g.session_id)

    def test_can_pass_auth_object(self):
        class FakeAuthObject:
            def __init__(self):
                self.foo = 'var'

        f = FakeAuthObject()
        g = GroupGetListInServiceProviderRequest(auth_object=f)
        self.assertEqual(f, g.auth_object)

    def test_can_pass_login_object(self):
        class FakeLoginObject:
            def __init__(self):
                self.foo = 'var'

        f = FakeLoginObject()
        g = GroupGetListInServiceProviderRequest(login_object=f)
        self.assertEqual(f, g.login_object)

    @unittest.mock.patch('broadsoft.requestobjects.AuthenticationRequest.AuthenticationRequest.authenticate')
    @unittest.mock.patch('broadsoft.requestobjects.LoginRequest.LoginRequest.login')
    @unittest.mock.patch.object(GroupGetListInServiceProviderRequest, 'post', side_effect=return_groups_list)
    def test_list_groups_convert_to_list(
        self,
        post_patch,
        login_patch,
        auth_patch
    ):
        data = GroupGetListInServiceProviderRequest.list_groups()
        self.assertEqual(
            [{'Group Name': 'Another Test Group', 'User Limit': '25', 'Group Id': 'anothertestgroup'},
             {'Group Name': None, 'User Limit': '25', 'Group Id': 'sandbox'}],
            data
        )
