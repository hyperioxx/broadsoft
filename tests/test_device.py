import unittest.mock
from broadsoft.Device import Device
from broadsoft.requestobjects.GroupAccessDeviceAddRequest import GroupAccessDeviceAddRequest


class TestBroadsoftDevice(unittest.TestCase):
    def test_device_attrs_get_passed_to_request_object(self):
        d = Device(name='beaverphone', description="Tim Beaver's Phone", type='iphone',
                   use_test=True, mac_address='aabbcc112233', protocol='gopher',
                   transport_protocol='ftp')
        ro = d.build_request_object()
        self.assertEqual(d.name, ro.device_name)
        self.assertEqual(d.type, ro.device_type)
        self.assertEqual(d.mac_address, ro.mac_address)
        self.assertEqual(d.protocol, ro.protocol)
        self.assertEqual(d.transport_protocol, ro.transport_protocol)

        # try again, flip-flopping use test
        d = Device(name='beaverphone', description="Tim Beaver's Phone", type='iphone',
                   use_test=False, mac_address='aabbcc112233', protocol='gopher',
                   transport_protocol='ftp')
        ro = d.build_request_object()
        self.assertEqual(d.name, ro.device_name)
        self.assertEqual(d.type, ro.device_type)
        self.assertEqual(d.mac_address, ro.mac_address)
        self.assertEqual(d.protocol, ro.protocol)
        self.assertEqual(d.transport_protocol, ro.transport_protocol)

    def test_device_default_protocols_respected(self):
        d = Device(name='beaverphone', description="Tim Beaver's Phone", type='iphone',
                   mac_address='aabbcc112233', protocol=None, transport_protocol=None)
        ro = d.build_request_object()

        g = GroupAccessDeviceAddRequest()

        self.assertEqual(ro.protocol, g.protocol)
        self.assertEqual(ro.transport_protocol, g.transport_protocol)
