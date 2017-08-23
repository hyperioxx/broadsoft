import unittest
import unittest.mock
import xml.etree.ElementTree as ET
from broadsoft.requestobjects.GroupAccessDeviceDeleteRequest import GroupAccessDeviceDeleteRequest
from broadsoft.requestobjects.lib.BroadsoftRequest import BroadsoftRequest


class TestBroadsoftGroupAccessDeviceDeleteRequest(unittest.TestCase):
    # GroupAccessDevice is for creating Identity Profiles. We expect to always use the Generic one.
    @unittest.skip
    def test_validate(self):
        u = GroupAccessDeviceDeleteRequest()
        with self.assertRaises(ValueError):
            u.validate()

    # GroupAccessDevice is for creating Identity Profiles. We expect to always use the Generic one.
    @unittest.skip
    def test_to_xml(self):
        d = GroupAccessDeviceDeleteRequest(
            device_name='dname'
        )

        x = d.to_xml()
        self.maxDiff = None
        self.assertEqual(
            '<BroadsoftDocument protocol="OCI" xmlns="C" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">' +
                '<sessionId xmlns="">' + d.broadsoftinstance.session_id + '</sessionId>' +
                '<command xmlns="" xsi:type="GroupAccessDeviceDeleteRequest">' +
                    '<serviceProviderId>' + d.broadsoftinstance.service_provider + '</serviceProviderId>' +
                    '<groupId>' + d.group_id + '</groupId>' +
                    '<deviceName>' + d.device_name + '</deviceName>' +
                '</command>' +
            '</BroadsoftDocument>',
            ET.tostring(x).decode('utf-8')
        )
