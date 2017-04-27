import unittest
import unittest.mock
import xml.etree.ElementTree as ET
from broadsoft.XmlRequest import XmlRequest


class TestBroadsoftXML(unittest.TestCase):
    def test_to_xml(self):
        x = XmlRequest()
        x.command_name = 'GroupAddRequest'
        x.default_domain = 'dd'
        x.encoding = 'piglatin'
        x.protocol = 'gopher'
        x.session_id = 'seshy'
        x.version = '2.5'
        x.xmlns = 'PG13'
        x.xmlns_xsi = "http://youtube.com"

        xml = x.to_xml()
        self.assertEqual(
            '<BroadsoftDocument protocol="' + x.protocol + '" xmlns="' + x.xmlns + '" xmlns:xsi="' + x.xmlns_xsi + '"><sessionId xmlns="">' + x.session_id + '</sessionId><command xmlns="" xsi:type="' + x.command_name + '" /></BroadsoftDocument>',
            ET.tostring(element=xml).decode("utf-8")
        )

    def test_to_xml_requires_command(self):
        x = XmlRequest()
        with self.assertRaises(ValueError):
            x.to_xml()