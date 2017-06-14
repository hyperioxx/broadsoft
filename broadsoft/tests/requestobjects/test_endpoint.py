import unittest
import unittest.mock
import xml.etree.ElementTree as ET
from broadsoft.requestobjects.datatypes.EndPoint import Endpoint


def return_false(**kwargs):
    return False


class TestEndpoint(unittest.TestCase):
    def test_is_quorum(self):
        e = Endpoint()
        self.assertFalse(e.is_quorum())

        e = Endpoint()
        e.device_name = 'beaverphone'
        self.assertTrue(e.is_quorum())

        e = Endpoint()
        e.line_port = '6175551212_lp@broadsoft-dev.mit.edu'
        self.assertTrue(e.is_quorum())

    @unittest.mock.patch.object(Endpoint, 'is_quorum', side_effect=return_false)
    def test_xml_without_quorum(
            self,
            is_quorum_patch
    ):
        e = Endpoint()
        self.assertIsNone(e.to_xml())

    def test_to_xml(self):
        self.maxDiff = None

        # full call
        e = Endpoint()
        e.device_name = 'beaverphone'
        e.line_port = '6175551212_lp@broadsoft-dev.mit.edu'

        target_xml = \
            '<endpoint>' + \
                '<accessDeviceEndpoint>' + \
                    '<accessDevice>' + \
                        '<deviceLevel>Group</deviceLevel>' + \
                        '<deviceName>beaverphone</deviceName>' + \
                    '</accessDevice>' + \
                    '<linePort>6175551212_lp@broadsoft-dev.mit.edu</linePort>' + \
                '</accessDeviceEndpoint>' + \
            '</endpoint>'

        self.assertEqual(
            target_xml,
            ET.tostring(e.to_xml()).decode('utf-8')
        )

        # no device name
        e = Endpoint()
        e.line_port = '6175551212_lp@broadsoft-dev.mit.edu'

        target_xml = \
            '<endpoint>' + \
            '<accessDeviceEndpoint>' + \
            '<linePort>6175551212_lp@broadsoft-dev.mit.edu</linePort>' + \
            '</accessDeviceEndpoint>' + \
            '</endpoint>'

        self.assertEqual(
            target_xml,
            ET.tostring(e.to_xml()).decode('utf-8')
        )

        # no line port
        e = Endpoint()
        e.device_name = 'beaverphone'

        target_xml = \
            '<endpoint>' + \
            '<accessDeviceEndpoint>' + \
            '<accessDevice>' + \
            '<deviceLevel>Group</deviceLevel>' + \
            '<deviceName>beaverphone</deviceName>' + \
            '</accessDevice>' + \
            '</accessDeviceEndpoint>' + \
            '</endpoint>'

        self.assertEqual(
            target_xml,
            ET.tostring(e.to_xml()).decode('utf-8')
        )