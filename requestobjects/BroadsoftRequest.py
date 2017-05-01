import xml.etree.ElementTree as ET
import requests
from broadsoft.requestobjects.XmlDocument import XmlDocument
from broadsoft.requestobjects.SoapEnvelope import SoapEnvelope

"""
abstract class inherited by objects like AuthenticationRequest
"""


class BroadsoftRequest(XmlDocument):
    def __init__(self):
        self.api_url = 'https://web1.voiplogic.net/webservice/services/ProvisioningService'
        self.default_domain = 'voiplogic.net'
        self.service_provider = 'ENT136'
        self.session_id = None
        self.timezone = 'America/New_York'

    def master_to_xml(self):
        master = ET.Element('BroadsoftDocument')
        master.set('protocol', 'OCI')
        master.set('xmlns', 'C')
        master.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')

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

    def post(self):
        # this function is only for descendant objects, like AuthenticationRequest

        # first, convert self into string representation
        # (to_string() comes from broadsoft.requestobjects.XmlDocument)
        payload = self.to_string()

        # wrap that payload in a SOAP envelope, and convert whole enchilada to a string in order to post to broadsoft
        e = SoapEnvelope(body=payload)
        envelope = e.to_string()

        # post to server
        headers = {'content-type': 'text/xml', 'SOAPAction': ''}
        response = requests.post(self.api_url, data=envelope, headers=headers)

        return response

    @staticmethod
    def convert_phone_number(number):
        import re
        number = str(number)
        number = re.sub('\D', '', number)
        number = number[:3] + '-' + number[3:6] + '-' + number[6:]
        return number