import xml.etree.ElementTree as ET

from broadsoft.requestobjects.lib.XmlDocument import XmlDocument

"""
Defines the SOAP envelope that encases Broadsoft request documents.

To create a SOAP envelope for an XML document, build your document, convert it to string, and pass to this object. will
return an ElementTree XML object (NOT a string).

example:

doc = '<?xml version="1.0" encoding="UTF-8"?><xml><child1>hi</child1></xml>'
string_doc = html.escape(doc, quote=True)
s = SoapEnvelope(body=string_doc)
envelope = s.to_xml()
"""


class SoapEnvelope(XmlDocument):
    def __init__(self, body=None):
        self.body = body

    def to_xml(self):
        env = ET.Element('soapenv:Envelope')
        env.set('xmlns:soapenv', "http://schemas.xmlsoap.org/soap/envelope/")
        env.set('xmlns:xsd', "http://www.w3.org/2001/XMLSchema")
        env.set('xmlns:xsi', "http://www.w3.org/2001/XMLSchema-instance")

        body = ET.SubElement(env, 'soapenv:Body')

        p = ET.SubElement(body, 'processOCIMessage')
        p.set('soapenv:encodingStyle', "http://schemas.xmlsoap.org/soap/encoding/")

        arg = ET.SubElement(p, 'arg0')
        arg.set('xsi:type', "soapenc:string")
        arg.set('xmlns:soapenc', "http://schemas.xmlsoap.org/soap/encoding/")
        arg.text = self.body

        return env
