import unittest.mock
import xml.etree.ElementTree as ET
from broadsoft.requestobjects.GroupAccessDeviceModifyRequest import GroupAccessDeviceModifyRequest
from broadsoft.requestobjects.lib.BroadsoftRequest import BroadsoftRequest


class TestBroadsoftGroupAccessDeviceModifyRequest(unittest.TestCase):
    def test_validation(self):
        g = GroupAccessDeviceModifyRequest()
        with self.assertRaises(ValueError):
            g.validate()

    def test_group_id_inheritance(self):
        # defaults to default set in BroadsoftRequest
        g = GroupAccessDeviceModifyRequest()
        self.assertEqual(g.default_group_id, g.group_id)

        # can also override
        g = GroupAccessDeviceModifyRequest(group_id='gid')
        self.assertEqual('gid', g.group_id)

    def test_convert_mac_address(self):
        g = GroupAccessDeviceModifyRequest()
        g.mac_address = 'aa:bb:cc:dd:ee:ff'
        g.convert_mac_address()
        self.assertEqual('aabbccddeeff', g.mac_address)

        g.mac_address = '1111.2222.3333'
        g.convert_mac_address()
        self.assertEqual('111122223333', g.mac_address)

    @unittest.mock.patch.object(GroupAccessDeviceModifyRequest, 'convert_mac_address')
    def test_mac_address_gets_converted_on_init(
            self,
            convert_mac_address_patch
    ):
        # not called when no mac addr
        g = GroupAccessDeviceModifyRequest()
        self.assertFalse(convert_mac_address_patch.called)

        # called when mac addr present
        g = GroupAccessDeviceModifyRequest(mac_address='aa:bb:cc:dd:ee:ff')
        self.assertTrue(convert_mac_address_patch.called)

    @unittest.mock.patch.object(GroupAccessDeviceModifyRequest, 'convert_mac_address')
    def test_mac_address_gets_converted_on_build_command_xml(
            self,
            convert_mac_address_patch
    ):
        g = GroupAccessDeviceModifyRequest(device_name='dname', description='desc', group_id='testgroup')

        # expect convert not to be called yet
        self.assertFalse(convert_mac_address_patch.called)

        g.mac_address = 'aa:bb:cc:11:22:33'

        # now when we build to xml, expect it to be called
        g.build_command_xml()
        self.assertTrue(convert_mac_address_patch.called)

    def test_to_xml(self):
        # with a mac address
        g = GroupAccessDeviceModifyRequest(device_name='dname', mac_address='aabbcc112233',
                                        description='desc', group_id='testgroup', ip_address='18.18.18.18',
                                        port='1054')

        target_xml = \
            '<command xmlns="" xsi:type="GroupAccessDeviceModifyRequest14">' + \
            '<serviceProviderId>ENT136</serviceProviderId>' + \
            '<groupId>testgroup</groupId>' + \
            '<deviceName>dname</deviceName>' + \
            '<macAddress>aabbcc112233</macAddress>' + \
            '<description>desc</description>' + \
            '<protocol>SIP 2.0</protocol>' + \
            '<netAddress>18.18.18.18</netAddress>' + \
            '<port>1054</port>' + \
            '<configurationMode>Default</configurationMode>' + \
            '<transportProtocol>Unspecified</transportProtocol>' + \
            '</command>'

        cmd = g.build_command_xml()
        self.maxDiff = None
        self.assertEqual(target_xml, ET.tostring(cmd).decode('utf-8'))

        # without a mac address
        g = GroupAccessDeviceModifyRequest(device_name='dname',
                                        description='desc', group_id='testgroup', ip_address='18.18.18.18',
                                        port='1054')

        target_xml = \
            '<command xmlns="" xsi:type="GroupAccessDeviceModifyRequest14">' + \
            '<serviceProviderId>ENT136</serviceProviderId>' + \
            '<groupId>testgroup</groupId>' + \
            '<deviceName>dname</deviceName>' + \
            '<description>desc</description>' + \
            '<protocol>SIP 2.0</protocol>' + \
            '<netAddress>18.18.18.18</netAddress>' + \
            '<port>1054</port>' + \
            '<configurationMode>Default</configurationMode>' + \
            '<transportProtocol>Unspecified</transportProtocol>' + \
            '</command>'

        cmd = g.build_command_xml()
        self.maxDiff = None
        self.assertEqual(target_xml, ET.tostring(cmd).decode('utf-8'))

        # with just sip_user_name and sip_password
        g = GroupAccessDeviceModifyRequest(device_name='dname', sip_user_name='6175551212@mit.edu',
                                           sip_password='password')

        target_xml = \
            '<command xmlns="" xsi:type="GroupAccessDeviceModifyRequest14">' + \
            '<serviceProviderId>ENT136</serviceProviderId>' + \
            '<groupId>mit</groupId>' + \
            '<deviceName>dname</deviceName>' + \
            '<protocol>SIP 2.0</protocol>' + \
            '<configurationMode>Default</configurationMode>' + \
            '<transportProtocol>Unspecified</transportProtocol>' + \
            '<useCustomUserNamePassword>true</useCustomUserNamePassword>' + \
            '<accessDeviceCredentials>' + \
            '<userName>' + g.sip_user_name + '</userName>' + \
            '<password>' + g.sip_password+ '</password>' + \
            '</accessDeviceCredentials>' + \
            '</command>'

        cmd = g.build_command_xml()
        self.maxDiff = None
        self.assertEqual(target_xml, ET.tostring(cmd).decode('utf-8'))
