import unittest.mock
import xml.etree.ElementTree as ET

from broadsoft.requestobjects.lib.SoapEnvelope import SoapEnvelope


class TestBroadsoftSoapEnvelope(unittest.TestCase):
    def test_to_xml_call(self):
        body = '<foo gar="bage">bar</foo>'
        e = SoapEnvelope(body=body)
        xml = e.to_xml()
        self.assertEqual(
            '<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">' +
        	'<soapenv:Body>' +
        	'<processOCIMessage soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">' +
        	'<arg0 xmlns:soapenc="http://schemas.xmlsoap.org/soap/encoding/" xsi:type="soapenc:string">' +
            '&lt;foo gar="bage"&gt;bar&lt;/foo&gt;' +
            '</arg0>' +
        	'</processOCIMessage>' +
        	'</soapenv:Body>' +
            '</soapenv:Envelope>',
            ET.tostring(xml).decode('utf-8')
        )