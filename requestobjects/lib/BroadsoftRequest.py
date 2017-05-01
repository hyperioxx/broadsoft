import xml.etree.ElementTree as ET
import requests
import datetime
import socket
import random
import logging
from broadsoft.requestobjects.lib.SoapEnvelope import SoapEnvelope

from broadsoft.requestobjects.lib.XmlDocument import XmlDocument

"""
abstract class inherited by objects like AuthenticationRequest

defines what a request to the Broadsoft OCI server looks like, how to post to it, and how to decode the responses
"""


class BroadsoftRequest(XmlDocument):
    prod_url = '[unknown]'
    test_url = 'https://web1.voiplogic.net/webservice/services/ProvisioningService'
    logging_dir = '/var/log/broadsoft'
    logging_fname = 'api.log'

    def __init__(self, use_test=False, session_id=None, require_logging=True):
        self.api_url = self.derive_api_url(use_test=use_test)
        self.default_domain = 'voiplogic.net'
        self.last_response = None
        self.service_provider = 'ENT136'
        self.session_id = session_id
        self.timezone = 'America/New_York'
        self.derive_session_id()

        self.default_logging(require_logging)

    def default_logging(self, require_logging):
        import os
        from logging.handlers import TimedRotatingFileHandler

        # does the log location exist
        if not os.path.exists(self.logging_dir):
            os.makedirs(name=self.logging_dir, exist_ok=True)

        if not os.path.exists(self.logging_dir) and require_logging:
            raise IOError('no permission to create ' + self.logging_dir)

        logging.basicConfig(filename=self.logging_dir + '/' + self.logging_fname, level=logging.INFO,
                            format='%(asctime)s (%(session_id)s) %(message)s')
        logger = logging.getLogger(name='broadsoftapilog')
        logger.setLevel(level=logging.INFO)
        handler = TimedRotatingFileHandler(filename=self.logging_dir + '/' + self.logging_fname,
                                           when='W0',
                                           interval=1,
                                           backupCount=12)
        logger.addHandler(handler)

    def derive_api_url(self, use_test):
        if use_test:
            return self.test_url

        return self.prod_url

    def derive_session_id(self):
        if self.session_id is None:
            self.session_id = \
                socket.gethostname() + ',' + \
                str(datetime.datetime.utcnow()) + ',' + \
                str(random.randint(1000000000, 9999999999))

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

    def post(self, extract_payload=True):
        # this function is only for descendant objects, like AuthenticationRequest

        # first, convert self into string representation
        # (to_string() comes from broadsoft.requestobjects.XmlDocument)
        payload = self.to_string()

        # wrap that payload in a SOAP envelope, and convert whole enchilada to a string in order to post to broadsoft
        e = SoapEnvelope(body=payload)
        envelope = e.to_string()

        logging.info("url: " + self.api_url, extra={'session_id': self.session_id})
        logging.info("payload: " + envelope, extra={'session_id': self.session_id})

        # post to server
        headers = {'content-type': 'text/xml', 'SOAPAction': ''}
        response = requests.post(url=self.api_url, data=envelope, headers=headers)
        self.last_response = response

        # massage the response and check for errors
        content = response.content
        try:
            content = content.decode('utf-8')
        except AttributeError:
            pass
        logging.info("response: " + content, extra={'session_id': self.session_id})
        BroadsoftRequest.check_error(response=content)

        # dig actual message out of SOAP envelope it came in (and return as XML object)
        if extract_payload:
            return BroadsoftRequest.extract_payload(content)

        # otherwise, return entire message as XML object
        xml = ET.fromstring(text=content)
        return xml

    @staticmethod
    def check_error(response):
        if type(response) is str:
            response = ET.fromstring(text=response)

        error = False
        faults = response.findall('.//{http://schemas.xmlsoap.org/soap/envelope/}Fault')
        if len(faults) > 0:
            fault = faults[0]
            message = fault.findall('./faultstring')[0].text
            detail = fault.findall('./detail/string')[0].text
            logging.error("SOAP error: " + message + ': ' + detail)
            raise RuntimeError("the SOAP server threw an error: " + message + ': ' + detail)

    @staticmethod
    def convert_phone_number(number):
        import re
        number = str(number)
        number = re.sub('\D', '', number)
        number = number[:3] + '-' + number[3:6] + '-' + number[6:]
        return number

    @staticmethod
    def extract_payload(response):
        response = ET.fromstring(text=response)
        payload = response.findall('.//processOCIMessageResponse/{urn:com:broadsoft:webservice}processOCIMessageReturn')[0].text
        return ET.fromstring(text=payload)