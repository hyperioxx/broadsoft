import unittest.mock
import xml.etree.ElementTree as ET

from broadsoft.lib import BroadsoftInstance
from broadsoft.requestobjects.GroupGetListInServiceProviderRequest import GroupGetListInServiceProviderRequest


def return_groups_list(**kwargs):
    return '<ns0:BroadsoftDocument xmlns:ns0="C" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" protocol="OCI"><sessionId>Chriss-MacBook-Pro-4.local,2017-05-02 17:31:34.373071,3810609302</sessionId><command echo="" xsi:type="GroupGetListInServiceProviderResponse"><groupTable><colHeading>Group Id</colHeading><colHeading>Group Name</colHeading><colHeading>User Limit</colHeading><row><col>anothertestgroup</col><col>Another Test Group</col><col>25</col></row><row><col>sandbox</col><col /><col>25</col></row></groupTable></command></ns0:BroadsoftDocument>'


class TestBroadsoftGroupGetListInServiceProviderRequest(unittest.TestCase):
    def test_inherits_service_provider_from_broadsoftinstance(self):
        b = BroadsoftInstance.BroadsoftInstance()
        g = GroupGetListInServiceProviderRequest(broadsoftinstance=b)
        self.assertEqual(g.service_provider, b.service_provider)

    def test_to_xml(self):
        b = BroadsoftInstance.BroadsoftInstance()

        # group id/case insensitive True
        g = GroupGetListInServiceProviderRequest(broadsoftinstance=b)

        x = g.to_xml()
        self.maxDiff = None
        self.assertEqual(
            '<BroadsoftDocument protocol="OCI" xmlns="C" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">' +
                '<sessionId xmlns="">' + g.broadsoftinstance.session_id + '</sessionId>' +
                '<command xmlns="" xsi:type="GroupGetListInServiceProviderRequest">' +
                    '<serviceProviderId>' + b.service_provider + '</serviceProviderId>' +
                    '<responseSizeLimit>' + str(g.response_size_limit) + '</responseSizeLimit>' +
                '</command>' +
            '</BroadsoftDocument>',
            ET.tostring(x).decode('utf-8')
        )

