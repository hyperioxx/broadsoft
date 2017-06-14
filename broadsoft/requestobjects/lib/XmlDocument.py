import xml.etree.ElementTree as ET
import html

"""
abstract class inherited by objects like SoapEnvelope and BroadsoftRequest

defines methods and properties to be shared by all XML documents, whether Broadsoft request documents, or the 
SOAP envelope that encases them
"""


class XmlDocument:
    def to_string(self, html_encode=False):
        # to_xml() comes from grandchild objects, like AuthenticationRequest
        xml = self.to_xml()
        s = '<?xml version="1.0" encoding="UTF-8"?>' + ET.tostring(xml).decode('utf-8')

        if html_encode:
            s = html.escape(s, quote=True)

        return s