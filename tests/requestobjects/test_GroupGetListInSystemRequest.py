import unittest.mock
import xml.etree.ElementTree as ET
from broadsoft.requestobjects.GroupGetListInSystemRequest import GroupGetListInSystemRequest


class TestBroadsoftGroupGetListInSystemRequest(unittest.TestCase):
    def test_GroupGetListInSystemRequest_to_xml(self):
        # group id/case insensitive True
        g = GroupGetListInSystemRequest()
        g.group_id = 'group1'
        g.group_id_mode = 'Starts With'
        g.group_id_case_insensitive = True

        x = g.to_xml()
        self.assertEqual(
            '<BroadsoftDocument protocol="OCI" xmlns="C" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">' +
                '<sessionId xmlns="">None</sessionId>' +
                '<command xmlns="" xsi:type="GroupGetListInSystemRequest">' +
                    '<responseSizeLimit>None</responseSizeLimit>' +
                    '<searchCriteriaGroupId>' +
                        '<mode>' + g.group_id_mode + '</mode>' +
                        '<value>' + g.group_id + '</value>' +
                        '<isCaseInsensitive>true</isCaseInsensitive>' +
                    '</searchCriteriaGroupId>' +
                '</command>' +
            '</BroadsoftDocument>',
            ET.tostring(x).decode('utf-8')
        )

        # group name/case insensitive False
        g = GroupGetListInSystemRequest()
        g.group_name = 'group1'
        g.group_name_mode = 'Starts With'
        g.group_name_case_insensitive = False

        x = g.to_xml()
        self.assertEqual(
            '<BroadsoftDocument protocol="OCI" xmlns="C" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">' +
                '<sessionId xmlns="">None</sessionId>' +
                '<command xmlns="" xsi:type="GroupGetListInSystemRequest">' +
                    '<responseSizeLimit>None</responseSizeLimit>' +
                    '<searchCriteriaGroupName>' +
                        '<mode>' + g.group_name_mode + '</mode>' +
                        '<value>' + g.group_name + '</value>' +
                        '<isCaseInsensitive>false</isCaseInsensitive>' +
                    '</searchCriteriaGroupName>' +
                '</command>' +
            '</BroadsoftDocument>',
            ET.tostring(x).decode('utf-8')
        )

        # service provider/case insensitive True
        self.maxDiff = None
        g = GroupGetListInSystemRequest()
        g.service_provider = 'group1'
        g.service_provider_mode = 'Starts With'
        g.service_provider_case_insensitive = True

        x = g.to_xml()
        self.assertEqual(
            '<BroadsoftDocument protocol="OCI" xmlns="C" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">' +
            '<sessionId xmlns="">None</sessionId>' +
            '<command xmlns="" xsi:type="GroupGetListInSystemRequest">' +
            '<responseSizeLimit>None</responseSizeLimit>' +
            '<searchCriteriaExactServiceProvider>' +
            '<mode>' + g.service_provider_mode + '</mode>' +
            '<value>' + g.service_provider + '</value>' +
            '<isCaseInsensitive>true</isCaseInsensitive>' +
            '</searchCriteriaExactServiceProvider>' +
            '</command>' +
            '</BroadsoftDocument>',
            ET.tostring(x).decode('utf-8')
        )

        # multiple criteria with mixed case insensitivity
        g = GroupGetListInSystemRequest()
        g.group_id = 'gid'
        g.group_id_mode = 'Starts With'
        g.group_id_case_insensitive = True
        g.group_name = 'gname'
        g.group_name_mode = 'Starts With'
        g.group_name_case_insensitive = False

        x = g.to_xml()
        self.assertEqual(
            '<BroadsoftDocument protocol="OCI" xmlns="C" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">' +
            '<sessionId xmlns="">None</sessionId>' +
            '<command xmlns="" xsi:type="GroupGetListInSystemRequest">' +
            '<responseSizeLimit>None</responseSizeLimit>' +
            '<searchCriteriaGroupId>' +
            '<mode>' + g.group_id_mode + '</mode>' +
            '<value>' + g.group_id + '</value>' +
            '<isCaseInsensitive>true</isCaseInsensitive>' +
            '</searchCriteriaGroupId>' +
            '<searchCriteriaGroupName>' +
            '<mode>' + g.group_name_mode + '</mode>' +
            '<value>' + g.group_name + '</value>' +
            '<isCaseInsensitive>false</isCaseInsensitive>' +
            '</searchCriteriaGroupName>' +
            '</command>' +
            '</BroadsoftDocument>',
            ET.tostring(x).decode('utf-8')
        )