import xml.etree.ElementTree as ET


class XmlRequest:
    def __init__(self):
        self.command_name = None
        self.encoding = "ISO-8859-1"
        self.protocol = 'OCI'
        self.session_id = None
        self.version = 1.0
        self.xmlns = 'C'
        self.xmlns_xsi = 'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"'

    def to_xml(self):
        self.validate()

        bd = ET.Element('BroadsoftDocument')
        bd.set('protocol', self.protocol)
        bd.set('xmlns', self.xmlns)
        bd.set('xmlns:xsi', self.xmlns_xsi)

        sid = ET.SubElement(bd, 'sessionId')
        sid.set('xmlns', '')
        sid.text = str(self.session_id)

        cmd = ET.SubElement(bd, 'command')
        cmd.set('xsi:type', self.command_name)
        cmd.set('xmlns', '')

        return bd

    def validate(self):
        if self.command_name is None:
            raise ValueError("can't run broadsoft.XmlRequest.to_xml() without a value for command_name")
