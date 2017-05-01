import xml.etree.ElementTree as ET
import re
from broadsoft.requestobjects.XmlDocument import XmlDocument

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
