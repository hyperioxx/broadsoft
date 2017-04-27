import unittest.mock
import xml.etree.ElementTree as ET

from broadsoft.requestobjects.XmlRequest import XmlRequest


class TestBroadsoftXML(unittest.TestCase):
    def test_to_xml_call(self):
        x = XmlRequest()
        x.command_name = 'GroupAddRequest'
        x.default_domain = 'dd'
        x.encoding = 'piglatin'
        x.protocol = 'gopher'
        x.session_id = 'seshy'
        x.version = '2.5'
        x.xmlns = 'PG13'
        x.xmlns_xsi = "http://youtube.com"

        xml = x.master_to_xml()
        self.assertEqual(
            '<BroadsoftDocument protocol="' + x.protocol + '" xmlns="' + x.xmlns + '" xmlns:xsi="' + x.xmlns_xsi + '"><sessionId xmlns="">' + x.session_id + '</sessionId></BroadsoftDocument>',
            ET.tostring(element=xml).decode("utf-8")
        )

    def test_convert_phone_number(self):
        self.assertEqual('617-555-1212', XmlRequest.convert_phone_number(number='6175551212'))
        self.assertEqual('617-555-1212', XmlRequest.convert_phone_number(number='617 555 1212'))
        self.assertEqual('617-555-1212', XmlRequest.convert_phone_number(number='(617) 555-1212'))
        self.assertEqual('617-555-1212', XmlRequest.convert_phone_number(number='(617)-555-1212'))