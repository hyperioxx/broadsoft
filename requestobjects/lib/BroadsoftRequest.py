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
    prod_api_url = '[unknown]'
    test_api_url = 'https://web1.voiplogic.net/webservice/services/ProvisioningService'
    prod_api_user_id = '[unknown]'
    test_api_user_id = 'admMITapi'
    prod_api_password = '[unknown]'
    test_api_password = 'EnM58#iD3vT'
    default_domain = 'voiplogic.net'
    logging_dir = '/var/log/broadsoft'
    logging_fname = 'api.log'
    service_provider = 'ENT136'
    timezone = 'America/New_York'

    def __init__(self, use_test=False, session_id=None, require_logging=True, auth_object=None, login_object=None):
        self.api_password = None
        self.api_url = self.derive_api_url(use_test=use_test)
        self.api_user_id = None
        self.auth_object = auth_object
        self.last_response = None
        self.login_object = login_object
        self.session_id = session_id
        self.derive_session_id()
        self.derive_creds(use_test=use_test)
        self.default_logging(require_logging)

    def check_error(self, response):
        error_msg = None

        # sometimes errors come in as Error commands inside a SOAP envelope
        payload = BroadsoftRequest.extract_payload(response=response)
        if payload:
            cmd_container = payload.findall('./command')
            if len(cmd_container) > 0:
                cmd = cmd_container[0]
                summary_container = cmd.findall('./summary')
                summary_english_container = cmd.findall('./summaryEnglish')
                detail_container = cmd.findall('./detail')

                summary = None
                summary_english = None
                detail = None
                error = False

                if len(summary_container) > 0:
                    summary = summary_container[0].text
                    error = True
                if len(summary_english_container) > 0:
                    summary_english = summary_english_container[0].text
                    error = True
                if len(detail_container) > 0:
                    detail = detail_container[0].text
                    error = True

                if error:
                    error_msg = "the SOAP server threw an error: "
                    error_msg += str(summary)
                    error_msg += ' :: ' + str(summary_english)
                    error_msg += ' :: ' + str(detail)

        # sometimes errors come in as SOAP faults
        if type(response) is str:
            response = ET.fromstring(text=response)

        faults = response.findall('.//{http://schemas.xmlsoap.org/soap/envelope/}Fault')
        if len(faults) > 0:
            fault = faults[0]
            message = fault.findall('./faultstring')[0].text
            detail = fault.findall('./detail/string')[0].text
            error_msg = "the SOAP server threw an error: " + message + ' :: ' + detail

        # found fault/error? log and raise exception
        if error_msg:
            logging.error(error_msg, extra={'session_id': self.session_id})
            raise RuntimeError(error_msg)

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
            return self.test_api_url

        return self.prod_api_url

    def derive_creds(self, use_test=False):
        if use_test:
            self.api_user_id = self.test_api_user_id
            self.api_password = self.test_api_password

        else:
            self.api_user_id = self.prod_api_user_id
            self.api_password = self.prod_api_password

    def derive_session_id(self):
        if self.session_id is None:
            # if there's an attached auth object, use that session id
            if self.auth_object:
                try:
                    self.session_id = self.auth_object.session_id
                except AttributeError:
                    pass

            # otherwise, build a fresh one
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

        # if this isn't an auth/login request, check for login object. none? need to login.
        if self.need_login():
            raise RuntimeError("need a LoginRequest to continue")

        # first, convert self into string representation
        # (to_string() comes from broadsoft.requestobjects.XmlDocument)
        payload = self.to_string()

        # wrap that payload in a SOAP envelope, and convert whole enchilada to a string in order to post to broadsoft
        e = SoapEnvelope(body=payload)
        envelope = e.to_string()

        logging.info("url: " + self.api_url, extra={'session_id': self.session_id})

        # if there's an attached auth object, grab cookies
        cookies = None
        if self.auth_object:
            try:
                cookies = self.auth_object.auth_cookie_jar
                logging.info("cookies: " + str(cookies), extra={'session_id': self.session_id})
                pass
            except AttributeError:
                pass

        logging.info("payload: " + envelope, extra={'session_id': self.session_id})

        # post to server
        headers = {'content-type': 'text/xml', 'SOAPAction': ''}
        response = requests.post(url=self.api_url, data=envelope, headers=headers, cookies=cookies)
        self.last_response = response

        # massage the response and check for errors
        content = response.content
        try:
            content = content.decode('utf-8')

        except AttributeError:
            pass

        logging.info("response: " + content, extra={'session_id': self.session_id})
        self.check_error(response=content)

        # if requested, dig actual message out of SOAP envelope it came in (and return as XML object)
        if extract_payload:
            return BroadsoftRequest.extract_payload(content)

        # otherwise, return entire message as XML object
        xml = ET.fromstring(text=content)
        return xml

    def need_login(self):
        if \
           self.command_name != 'AuthenticationRequest'\
           and self.command_name != 'LoginRequest14sp4'\
           and not self.login_object:
            return True

        return False

    @staticmethod
    def convert_phone_number(number):
        import re
        number = str(number)
        number = re.sub('\D', '', number)
        number = number[:3] + '-' + number[3:6] + '-' + number[6:]
        return number

    @staticmethod
    def convert_results_table(xml):
        # extract column headings
        headings = []
        for heading in xml.findall('.//colHeading'):
            headings.append(heading.text)

        # associate rows/columns with headings
        data = list()
        for row in xml.findall('.//row'):
            data_row = {}
            col_count = 0
            for col in row.findall('./col'):
                col_name = headings[col_count]
                col_val = col.text
                data_row[col_name] = col_val
                col_count += 1
            data.append(data_row)

        return data

    @staticmethod
    def extract_payload(response):
        response = ET.fromstring(text=response)
        payload_container = response.findall('.//processOCIMessageResponse/{urn:com:broadsoft:webservice}processOCIMessageReturn')
        if len(payload_container) > 0:
            payload = response.findall('.//processOCIMessageResponse/{urn:com:broadsoft:webservice}processOCIMessageReturn')[0].text
            return ET.fromstring(text=payload)
        return None