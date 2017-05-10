import xml.etree.ElementTree as ET
import requests
import datetime
import socket
import random
import logging
from broadsoft.requestobjects.lib.SoapEnvelope import SoapEnvelope
from hashlib import sha1, md5

from broadsoft.requestobjects.lib.XmlDocument import XmlDocument

"""
abstract class inherited by objects like AuthenticationRequest

defines what a request to the Broadsoft OCI server looks like, how to post to it, and how to decode the responses
"""


class BroadsoftRequest(XmlDocument):
    prod_api_url = '[unknown]'
    test_api_url = 'https://web1.voiplogic.net/webservice/services/ProvisioningService'
    prod_default_domain = 'broadsoft.mit.edu'
    test_default_domain = 'broadsoft-dev.mit.edu'
    logging_dir = '/var/log/broadsoft'
    logging_fname = 'api.log'
    service_provider = 'ENT136'
    timezone = 'America/New_York'
    check_success = False
    default_group_id = 'mit'

    def __init__(self, use_test=False, session_id=None, require_logging=True, auth_object=None,
                 login_object=None, auto_derive_creds=True, group_id=None, auto_derive_group_id=True):
        self.api_password = None
        self.api_url = None
        self.api_user_id = None
        self.auth_object = auth_object
        self.commands = []
        self.default_domain = None
        self.group_id = group_id
        self.last_response = None
        self.login_object = login_object
        self.session_id = session_id
        self.use_test = use_test

        self.derive_api_url()
        self.derive_default_domain()
        self.derive_session_id()

        if auto_derive_creds:
            self.derive_creds()

        if not self.group_id and auto_derive_group_id:
            self.group_id = self.default_group_id

        # now that we're done setting up shop, start the logging
        self.default_logging(require_logging)

    def authenticate_and_login(self):
        logging.info("running authenticate request", extra={'session_id': self.session_id})
        a = AuthenticationRequest.authenticate(use_test=self.use_test, session_id=self.session_id)
        self.auth_object = a

        logging.info("running login request", extra={'session_id': self.session_id})
        l = LoginRequest.login(use_test=self.use_test, auth_object=a)
        self.login_object = l
        logging.info("continuing with request", extra={'session_id': self.session_id})

    def build_command_shell(self):
        cmd = ET.Element('command')
        cmd.set('xsi:type', self.command_name)
        cmd.set('xmlns', '')
        return cmd

    def check_error(self, string_response):
        response = string_response
        if type(string_response) is str:
            response = ET.fromstring(text=string_response)
        else:
            string_response = ET.tostring(response)
        payload = BroadsoftRequest.extract_payload(response=string_response)

        error_msg = None

        # sometimes errors come in as Error commands inside a SOAP envelope
        if not error_msg:
            error_msg = self.check_error__message(payload=payload)

        # sometimes errors come in as SOAP faults
        if not error_msg:
            error_msg = self.check_error__fault(response=response)

        # request objects that make changes to the system should do an extra check
        if not error_msg and self.check_success:
            error_msg = self.check_error__success(payload=payload)

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
                            format='%(levelname)s:%(asctime)s (%(session_id)s) %(message)s')
        logger = logging.getLogger(name='broadsoftapilog')
        logger.setLevel(level=logging.INFO)
        handler = TimedRotatingFileHandler(filename=self.logging_dir + '/' + self.logging_fname,
                                           when='W0',
                                           interval=1,
                                           backupCount=12)
        logger.addHandler(handler)

    def derive_api_url(self):
        self.api_url = self.prod_api_url
        if self.use_test:
            self.api_url = self.test_api_url

    def derive_commands(self):
        # determine source of commands we'll be injecting into the master XML document

        # begin by presuming what's in self.commands
        # this will be when submitting a compound request of multiple commands
        commands = self.commands

        # otherwise, will be self
        # this will be when directly calling a descendant object, like UserAddRequest
        if self.__class__.__name__ != 'BroadsoftRequest':
            commands = [self]

        return commands

    def derive_creds(self):
        from nistcreds.NistCreds import NistCreds
        creds_member = 'prod'
        if self.use_test:
            creds_member = 'test'
        creds = NistCreds(group='broadsoft', member=creds_member)
        self.api_user_id = creds.username
        self.api_password = creds.password

    def derive_default_domain(self):
        self.default_domain = self.prod_default_domain
        if self.use_test:
            self.default_domain = self.test_default_domain

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

    def post(self, extract_payload=True, auto_login=True):
        # this function is only for descendant objects, like AuthenticationRequest

        logging.info("running " + self.command_name + " request", extra={'session_id': self.session_id})

        # if this isn't an auth/login request, check for login object. none? need to login.
        if self.need_login():
            logging.info("auth/login needed. auto_login is " + str(auto_login), extra={'session_id': self.session_id})
            if auto_login:
                self.authenticate_and_login()
            else:
                logging.error("need an AuthenticationRequest and associated LoginRequest to continue, or set auto_login to True",
                             extra={'session_id': self.session_id})
                raise RuntimeError("need an AuthenticationRequest and associated LoginRequest to continue, or set auto_login to True")

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
        self.check_error(string_response=content)

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
           and (not self.login_object or not self.auth_object):
            return True

        return False

    def to_xml(self):
        doc = ET.Element('BroadsoftDocument')
        doc.set('protocol', 'OCI')
        doc.set('xmlns', 'C')
        doc.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')

        sid = ET.SubElement(doc, 'sessionId')
        sid.set('xmlns', '')
        sid.text = str(self.session_id)

        # inject command XML
        commands = self.derive_commands()
        for cmd_object in commands:
            cmd = cmd_object.build_command_xml()
            doc.append(cmd)

        return doc

    @staticmethod
    def check_error__fault(response):
        error_msg = None

        faults = response.findall('.//{http://schemas.xmlsoap.org/soap/envelope/}Fault')
        if len(faults) > 0:
            fault = faults[0]
            message = fault.findall('./faultstring')[0].text
            detail = fault.findall('./detail/string')[0].text
            error_msg = "the SOAP server threw an error: " + message + ' :: ' + detail

        return error_msg

    @staticmethod
    def check_error__message(payload):
        error_msg = None

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

        return error_msg

    @staticmethod
    def check_error__success(payload):
        error_msg = None

        command = payload.findall('./command')[0]
        command_name = command.get('{http://www.w3.org/2001/XMLSchema-instance}type')
        if command_name != 'c:SuccessResponse':
            error_msg = "we were expecting an explicit success message from the SOAP server, but got " + ET.tostring(
                payload).decode('utf-8')

        return error_msg

    @staticmethod
    def convert_phone_number(number, dashes=False):
        import re
        number = str(number)
        number = re.sub('\D', '', number)
        if dashes:
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


class AuthenticationRequest(BroadsoftRequest):
    command_name = 'AuthenticationRequest'

    def __init__(self, use_test=False, **kwargs):
        self.auth_cookie_jar = None
        self.nonce = None
        BroadsoftRequest.__init__(self, use_test=use_test, **kwargs)

    def build_command_xml(self):
        cmd = self.build_command_shell()

        uid = ET.SubElement(cmd, 'userId')
        uid.text = self.api_user_id

        return cmd

    @staticmethod
    def authenticate(**kwargs):
        a = AuthenticationRequest(**kwargs)
        payload = a.post()
        a.auth_cookie_jar = a.last_response.cookies
        a.nonce = AuthenticationRequest.extract_auth_token(payload=payload)
        return a

    @staticmethod
    def extract_auth_token(payload):
        # when successfully authenticate, auth token is encased inside a <nonce> element in the response payload
        token = payload.findall('./command/nonce')[0]
        return token.text


class LoginRequest(BroadsoftRequest):
    command_name = 'LoginRequest14sp4'

    def __init__(self, use_test=False, **kwargs):
        BroadsoftRequest.__init__(self, use_test=use_test, **kwargs)

    def build_command_xml(self):
        cmd = self.build_command_shell()

        uid = ET.SubElement(cmd, 'userId')
        uid.text = self.api_user_id

        pwd = ET.SubElement(cmd, 'signedPassword')
        pwd.text = self.build_signed_password()

        return cmd

    def build_signed_password(self):
        # the signedPassword is convoluted
        # first, SHA encrypt password
        s = sha1()
        s.update(self.api_password.encode())
        sha_pwd = s.hexdigest()

        # now, combine the SHA passwd with the "nonce" value returned by the AuthenticationRequest and md5 it
        concat_pwd = self.auth_object.nonce + ':' + sha_pwd
        m = md5()
        m.update(concat_pwd.encode())
        signed_pwd = m.hexdigest()

        return signed_pwd

    @staticmethod
    def login(**kwargs):
        l = LoginRequest(**kwargs)
        l.post()
        return l