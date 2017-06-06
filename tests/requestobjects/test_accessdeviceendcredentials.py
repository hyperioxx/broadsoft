import unittest
import unittest.mock
import xml.etree.ElementTree as ET
from broadsoft.requestobjects.datatypes.AccessDeviceCredentials import AccessDeviceCredentials


class TestAccessDeviceCredentials(unittest.TestCase):
    def test_to_xml(self):
        self.maxDiff = None

        adc = AccessDeviceCredentials()
        adc.user_name = '6175551212@mit.edu'
        adc.password = 'pw'

        target_xml = \
            '<accessDeviceCredentials>' + \
                '<userName>' + adc.user_name + '</userName>' + \
                '<password>' + adc.password + '</password>' + \
            '</accessDeviceCredentials>'

        self.assertEqual(
            target_xml,
            ET.tostring(adc.to_xml()).decode('utf-8')
        )
