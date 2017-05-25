import unittest
import unittest.mock
import xml.etree.ElementTree as ET
from broadsoft.requestobjects.datatypes.AccessDevice import AccessDevice


class TestAccessDeviceEndpoint(unittest.TestCase):
    def validate(self):
        a = AccessDevice(device_level=None)
        with self.assertRaises(ValueError):
            a.validate()

        a = AccessDevice()
        with self.assertRaises(ValueError):
            a.validate()

    def test_to_xml(self):
        self.maxDiff = None

        # full call
        e = AccessDevice()
        e.device_name = 'beaverphone'

        target_xml = \
            '<accessDevice>' + \
                '<deviceLevel>Group</deviceLevel>' + \
                '<deviceName>beaverphone</deviceName>' + \
            '</accessDevice>'

        self.assertEqual(
            target_xml,
            ET.tostring(e.to_xml()).decode('utf-8')
        )
