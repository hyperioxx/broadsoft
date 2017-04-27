import xml.etree.ElementTree as ET


class XmlRequest:
    def __init__(self):
        self.default_domain = 'broadworks'
        self.encoding = "ISO-8859-1"
        self.protocol = 'OCI'
        self.service_provider = None
        self.session_id = None
        self.timezone = 'America/Boston'
        self.xml_version = 1.0
        self.xmlns = 'C'
        self.xmlns_xsi = 'http://www.w3.org/2001/XMLSchema-instance'

    def master_to_xml(self):
        bd = ET.Element('BroadsoftDocument')
        bd.set('protocol', self.protocol)
        bd.set('xmlns', self.xmlns)
        bd.set('xmlns:xsi', self.xmlns_xsi)

        sid = ET.SubElement(bd, 'sessionId')
        sid.set('xmlns', '')
        sid.text = str(self.session_id)

        return bd

    @staticmethod
    def convert_phone_number(number):
        import re
        number = str(number)
        number = re.sub('\D', '', number)
        number = number[:3] + '-' + number[3:6] + '-' + number[6:]
        return number