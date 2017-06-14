import unittest.mock
import xml.etree.ElementTree as ET
from broadsoft.requestobjects.UserSharedCallAppearanceAddEndpointRequest import UserSharedCallAppearanceAddEndpointRequest
from broadsoft.requestobjects.lib.BroadsoftRequest import BroadsoftRequest


class TestBroadsoftUserSharedCallAddEndpointRequest(unittest.TestCase):
    def test_validate(self):
        u = UserSharedCallAppearanceAddEndpointRequest()
        with self.assertRaises(ValueError):
            u.validate()

    def test_build_command_xml(self):
        u = UserSharedCallAppearanceAddEndpointRequest(device_name='beaverphone',
                                                       sip_user_id='6175551212@broadsoft.mit.edu',
                                                       line_port='6175551212_beaverphone@broadsoft.mit.edu')

        self.maxDiff = None
        xml = u.to_xml()
        cmd = xml.findall('command')[0]
        self.assertEqual(
            '<command xmlns="" xsi:type="UserSharedCallAppearanceAddEndpointRequest14sp2">' +
            '<userId>6175551212@broadsoft.mit.edu</userId>' +
            '<accessDeviceEndpoint>' +
                '<accessDevice>' +
                    '<deviceLevel>Group</deviceLevel>' +
                    '<deviceName>beaverphone</deviceName>' +
                '</accessDevice>' +
                '<linePort>6175551212_beaverphone@broadsoft.mit.edu</linePort>' +
            '</accessDeviceEndpoint>' +
            '<isActive>true</isActive>' +
            '<allowOrigination>true</allowOrigination>' +
            '<allowTermination>true</allowTermination>' +
            '</command>',
            ET.tostring(cmd).decode('utf-8')
        )
