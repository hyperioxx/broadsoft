import unittest.mock
import xml.etree.ElementTree as ET
from broadsoft.requestobjects.GroupAccessDeviceAddRequest import GroupAccessDeviceAddRequest
from broadsoft.requestobjects.lib.BroadsoftRequest import BroadsoftRequest


class TestBroadsoftGroupAccessDeviceAddRequest(unittest.TestCase):
    @unittest.mock.patch.object(BroadsoftRequest, 'convert_phone_number')
    @unittest.mock.patch.object(GroupAccessDeviceAddRequest, 'validate')
    def test_did_gets_converted(
            self,
            validate_patch,
            convert_phone_number_patch
    ):
        u = GroupAccessDeviceAddRequest(did='617 555 1212', device_name='test phone',
                                        device_type='Polycom SoundPoint IP 550')
        u.to_xml()
        self.assertTrue(convert_phone_number_patch.called)

    def test_did_format_gets_validated(self):
        u = GroupAccessDeviceAddRequest(did='617555121', device_name='test phone',
                                        device_type='Polycom SoundPoint IP 550')
        with self.assertRaises(ValueError):
            u.validate()

        u = GroupAccessDeviceAddRequest(did='61755512111', device_name='test phone',
                                        device_type='Polycom SoundPoint IP 550')
        with self.assertRaises(ValueError):
            u.validate()

        u = GroupAccessDeviceAddRequest(did='617555121x', device_name='test phone',
                                        device_type='Polycom SoundPoint IP 550')
        with self.assertRaises(ValueError):
            u.validate()

    def test_validation(self):
        """
        g = GroupAccessDeviceAddRequest(did=None, device_name=None, device_type=None, protocol='SIP 2.0',
                 transport_protocol='Unspecified')
        """

        # no device_name
        u = GroupAccessDeviceAddRequest(did=6175551212, device_name=None, device_type='dtype', protocol='SIP 2.0',
                                        transport_protocol='Unspecified')
        with self.assertRaises(ValueError):
            u.validate()

        # no device_type
        u = GroupAccessDeviceAddRequest(did=6175551212, device_name='dname', device_type=None, protocol='SIP 2.0',
                                        transport_protocol='Unspecified')
        with self.assertRaises(ValueError):
            u.validate()

        # no protocol
        u = GroupAccessDeviceAddRequest(did=6175551212, device_name='dname', device_type='dtype', protocol=None,
                                        transport_protocol='Unspecified')
        with self.assertRaises(ValueError):
            u.validate()

        # no transport_protocol
        u = GroupAccessDeviceAddRequest(did=6175551212, device_name='dname', device_type='dtype', protocol='SIP 2.0',
                                        transport_protocol=None)
        with self.assertRaises(ValueError):
            u.validate()

        # bad mac addr
        u = GroupAccessDeviceAddRequest(did=6175551212, device_name='dname', device_type='dtype',
                                        protocol='SIP 2.0', mac_address='a',
                                        transport_protocol=None)
        with self.assertRaises(ValueError):
            u.validate()

    def test_group_id_inheritance(self):
        # defaults to default set in BroadsoftRequest
        g = GroupAccessDeviceAddRequest()
        self.assertEqual(g.default_group_id, g.group_id)

        # can also override
        g = GroupAccessDeviceAddRequest(group_id='gid')
        self.assertEqual('gid', g.group_id)

    def test_to_xml(self):
        g = GroupAccessDeviceAddRequest(did='6175551212', device_name='dname', mac_address='aabbcc112233',
                                        device_type='dtype', description='desc', group_id='testgroup')

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
