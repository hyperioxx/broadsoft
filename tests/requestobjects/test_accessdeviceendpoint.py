import unittest
import unittest.mock
import xml.etree.ElementTree as ET
from broadsoft.requestobjects.datatypes.AccessDeviceEndpoint import AccessDeviceEndpoint


def return_false(**kwargs):
    return False


class TestAccessDeviceEndpoint(unittest.TestCase):
    def test_to_xml(self):
        self.maxDiff = None

        # full call
        ade = AccessDeviceEndpoint()
        ade.device_name = 'beaverphone'
        ade.line_port = '6175551212_lp@broadsoft-dev.mit.edu'

        target_xml = \
            '<accessDeviceEndpoint>' + \
                '<accessDevice>' + \
                    '<deviceLevel>Group</deviceLevel>' + \
                    '<deviceName>beaverphone</deviceName>' + \
                '</accessDevice>' + \
                '<linePort>6175551212_lp@broadsoft-dev.mit.edu</linePort>' + \
                '<contact xsi:nil="true" />' + \
            '</accessDeviceEndpoint>'

        self.assertEqual(
            target_xml,
            ET.tostring(ade.to_xml()).decode('utf-8')
        )

        # no device name
        ade = AccessDeviceEndpoint()
        ade.line_port = '6175551212_lp@broadsoft-dev.mit.edu'

        target_xml = \
            '<accessDeviceEndpoint>' + \
            '<linePort>6175551212_lp@broadsoft-dev.mit.edu</linePort>' + \
            '<contact xsi:nil="true" />' + \
            '</accessDeviceEndpoint>'

        self.assertEqual(
            target_xml,
            ET.tostring(ade.to_xml()).decode('utf-8')
        )

        # no line port
        ade = AccessDeviceEndpoint()
        ade.device_name = 'beaverphone'

        target_xml = \
            '<accessDeviceEndpoint>' + \
            '<accessDevice>' + \
            '<deviceLevel>Group</deviceLevel>' + \
            '<deviceName>beaverphone</deviceName>' + \
            '</accessDevice>' + \
            '<contact xsi:nil="true" />' + \
            '</accessDeviceEndpoint>'

        self.assertEqual(
            target_xml,
            ET.tostring(ade.to_xml()).decode('utf-8')
        )