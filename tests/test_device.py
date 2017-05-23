import unittest.mock
from broadsoft.Device import Device


class TestBroadsoftDevice(unittest.TestCase):
    def test_device_attrs_get_passed_to_request_object(self):
        d = Device(did=6175551212, name='beaverphone', description="Tim Beaver's Phone", type='iphone',
                   extension=51212, use_test=True, mac_address='aabbcc112233', protocol='gopher',
                   transport_protocol='ftp')
        ro = d.build_request_object()
        self.assertEqual(d.name, ro.device_name)
        self.assertEqual(d.type, ro.device_type)
        self.assertEqual(d.mac_address, ro.mac_address)
        self.assertEqual(d.protocol, ro.protocol)
        self.assertEqual(d.transport_protocol, ro.transport_protocol)

        # try again, flip-flopping use test
        d = Device(did=6175551212, name='beaverphone', description="Tim Beaver's Phone", type='iphone',
                   extension=51212, use_test=False, mac_address='aabbcc112233', protocol='gopher',
                   transport_protocol='ftp')
        ro = d.build_request_object()
        self.assertEqual(d.name, ro.device_name)
        self.assertEqual(d.type, ro.device_type)
        self.assertEqual(d.mac_address, ro.mac_address)
        self.assertEqual(d.protocol, ro.protocol)
        self.assertEqual(d.transport_protocol, ro.transport_protocol)
