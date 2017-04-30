import xml.etree.ElementTree as ET

"""
abstract class that should actually be instantiated as in GroupAddRequest
"""


class XmlRequest:
    def __init__(self):
        self.default_domain = 'voiplogic.net'
        self.encoding = "ISO-8859-1"
        self.protocol = 'OCI'
        self.service_provider = 'ENT136'
        self.session_id = None
        self.timezone = 'America/New_York'
        self.xml_version = 1.0
        self.xmlns = 'C'
        self.xmlns_xsi = 'http://www.w3.org/2001/XMLSchema-instance'

    def master_to_xml(self):
        master = ET.Element('BroadsoftDocument')
        master.set('protocol', self.protocol)
        master.set('xmlns', self.xmlns)
        master.set('xmlns:xsi', self.xmlns_xsi)

        sid = ET.SubElement(master, 'sessionId')
        sid.set('xmlns', '')
        sid.text = str(self.session_id)

        # if self.command_name is set (should be a class var in the descendant object), build a <command> subelement
        cmd = None
        try:
            command_name = self.command_name
            cmd = ET.SubElement(master, 'command')
            cmd.set('xsi:type', command_name)
            cmd.set('xmlns', '')
        except AttributeError:
            pass

        # returns both master XML and (for convenience) inserted command, which is where more stuff gets inserted by
        # descendant object
        return master, cmd

    @staticmethod
    def convert_phone_number(number):
        import re
        number = str(number)
        number = re.sub('\D', '', number)
        number = number[:3] + '-' + number[3:6] + '-' + number[6:]
        return number