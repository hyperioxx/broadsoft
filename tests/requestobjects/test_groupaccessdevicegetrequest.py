import unittest.mock
import xml.etree.ElementTree as ET

from broadsoft.lib import BroadsoftInstance
from broadsoft.requestobjects.GroupAccessDeviceGetRequest import GroupAccessDeviceGetRequest
from broadsoft.requestobjects.lib.BroadsoftRequest import BroadsoftRequest


def return_none(**kwargs):
    return None


class TestBroadsoftGroupAccessDeviceGetRequest(unittest.TestCase):
    def test_validate(self):
        g = GroupAccessDeviceGetRequest()
        with self.assertRaises(ValueError):
            g.validate()

    def test_to_xml(self):
        g = GroupAccessDeviceGetRequest(name='beaverphone', broadsoftinstance=BroadsoftInstance.factory())

        x = g.to_xml()
        self.maxDiff = None
        self.assertEqual(
            '<BroadsoftDocument protocol="OCI" xmlns="C" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">' +
                '<sessionId xmlns="">' + g.broadsoftinstance.session_id + '</sessionId>' +
                '<command xmlns="" xsi:type="GroupAccessDeviceGetRequest18sp1">' +
                    '<serviceProviderId>' + g.service_provider + '</serviceProviderId>' +
                    '<groupId>' + g.group_id + '</groupId>' +
                    '<deviceName>' + g.name + '</deviceName>' +
                '</command>' +
            '</BroadsoftDocument>',
            ET.tostring(x).decode('utf-8')
        )
