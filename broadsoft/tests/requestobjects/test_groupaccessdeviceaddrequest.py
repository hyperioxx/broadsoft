import unittest.mock
import xml.etree.ElementTree as ET

from broadsoft.lib import BroadsoftInstance
from broadsoft.requestobjects.GroupAccessDeviceAddRequest import GroupAccessDeviceAddRequest


class TestBroadsoftGroupAccessDeviceAddRequest(unittest.TestCase):
    def test_validation(self):
        """
        g = GroupAccessDeviceAddRequest(device_name=None, device_type=None, protocol='SIP 2.0',
                 transport_protocol='Unspecified')
        """

        # no device_name
        u = GroupAccessDeviceAddRequest(device_name=None, device_type='dtype', protocol='SIP 2.0',
                                        transport_protocol='Unspecified')
        with self.assertRaises(ValueError):
            u.validate()

        # no device_type
        u = GroupAccessDeviceAddRequest(device_name='dname', device_type=None, protocol='SIP 2.0',
                                        transport_protocol='Unspecified')
        with self.assertRaises(ValueError):
            u.validate()

        # no protocol
        u = GroupAccessDeviceAddRequest(device_name='dname', device_type='dtype', protocol=None,
                                        transport_protocol='Unspecified')
        with self.assertRaises(ValueError):
            u.validate()

        # no transport_protocol
        u = GroupAccessDeviceAddRequest(device_name='dname', device_type='dtype', protocol='SIP 2.0',
                                        transport_protocol=None)
        with self.assertRaises(ValueError):
            u.validate()

        # bad mac addr
        u = GroupAccessDeviceAddRequest(device_name='dname', device_type='dtype',
                                        protocol='SIP 2.0', mac_address='a',
                                        transport_protocol='Unspecified')
        with self.assertRaises(ValueError):
            u.validate()

    def test_group_id_inheritance(self):
        # defaults to default set in BroadsoftRequest
        i = BroadsoftInstance.factory()
        g = GroupAccessDeviceAddRequest(broadsoftinstance=i)
        self.assertEqual(i.default_group_id, g.group_id)

        # can also override
        g = GroupAccessDeviceAddRequest(group_id='gid')
        self.assertEqual('gid', g.group_id)

    def test_convert_mac_address(self):
        g = GroupAccessDeviceAddRequest()
        g.mac_address = 'aa:bb:cc:dd:ee:ff'
        g.convert_mac_address()
        self.assertEqual('aabbccddeeff', g.mac_address)

        g.mac_address = '1111.2222.3333'
        g.convert_mac_address()
        self.assertEqual('111122223333', g.mac_address)

    @unittest.mock.patch.object(GroupAccessDeviceAddRequest, 'convert_mac_address')
    def test_mac_address_gets_converted_on_init(
            self,
            convert_mac_address_patch
    ):
        # not called when no mac addr
        g = GroupAccessDeviceAddRequest()
        self.assertFalse(convert_mac_address_patch.called)

        # called when mac addr present
        g = GroupAccessDeviceAddRequest(mac_address='aa:bb:cc:dd:ee:ff')
        self.assertTrue(convert_mac_address_patch.called)

    @unittest.mock.patch.object(GroupAccessDeviceAddRequest, 'convert_mac_address')
    def test_mac_address_gets_converted_on_build_command_xml(
            self,
            convert_mac_address_patch
    ):
        g = GroupAccessDeviceAddRequest(device_name='dname',
                                        device_type='dtype', description='desc', group_id='testgroup')

        # expect convert not to be called yet
        self.assertFalse(convert_mac_address_patch.called)

        g.mac_address = 'aa:bb:cc:11:22:33'

        # now when we build to xml, expect it to be called
        g.build_command_xml()
        self.assertTrue(convert_mac_address_patch.called)

    def test_to_xml(self):
        # with a mac address
        g = GroupAccessDeviceAddRequest(device_name='dname', mac_address='aabbcc112233',
                                        device_type='dtype', description='desc', group_id='testgroup',
                                        broadsoftinstance=BroadsoftInstance.factory())

        target_xml = \
            '<command xmlns="" xsi:type="GroupAccessDeviceAddRequest14">' + \
            '<serviceProviderId>ENT136</serviceProviderId>' + \
            '<groupId>testgroup</groupId>' + \
            '<deviceName>dname</deviceName>' + \
            '<deviceType>dtype</deviceType>' + \
            '<macAddress>aabbcc112233</macAddress>' + \
            '<description>desc</description>' + \
            '</command>'

        cmd = g.build_command_xml()
        self.maxDiff = None
        self.assertEqual(target_xml, ET.tostring(cmd).decode('utf-8'))

        # without a mac address
        g = GroupAccessDeviceAddRequest(device_name='dname',
                                        device_type='dtype', description='desc', group_id='testgroup',
                                        broadsoftinstance=BroadsoftInstance.factory())

        target_xml = \
            '<command xmlns="" xsi:type="GroupAccessDeviceAddRequest14">' + \
            '<serviceProviderId>ENT136</serviceProviderId>' + \
            '<groupId>testgroup</groupId>' + \
            '<deviceName>dname</deviceName>' + \
            '<deviceType>dtype</deviceType>' + \
            '<description>desc</description>' + \
            '</command>'

        cmd = g.build_command_xml()
        self.maxDiff = None
        self.assertEqual(target_xml, ET.tostring(cmd).decode('utf-8'))
