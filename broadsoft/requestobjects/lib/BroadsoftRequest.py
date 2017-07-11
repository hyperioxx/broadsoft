import xml.etree.ElementTree as ET
import requests
import datetime
import socket
import random
import logging
import re
from broadsoft.requestobjects.lib.SoapEnvelope import SoapEnvelope
from hashlib import sha1, md5
from nettools.MACtools import MAC

from broadsoft.requestobjects.lib.XmlDocument import XmlDocument

"""
abstract class inherited by objects like AuthenticationRequest

defines what a request to the Broadsoft OCI server looks like, how to post to it, and how to decode the responses
"""


class BroadsoftRequest(XmlDocument):
    auth_exceptions = ['AuthenticationRequest', 'LoginRequest14sp4', 'LogoutRequest']
    logging_dir = '/var/log/broadsoft'
    logging_fname = 'api.log'
    default_timezone = 'America/New_York'
    check_success = False

    def __init__(self, require_logging=True, timezone=None, broadsoftinstance=None, group_id=None):
        self.broadsoftinstance = broadsoftinstance
        self.commands = []
        self.group_id = group_id
        self.last_response = None

        if timezone:
            self.timezone = timezone
        else:
            self.timezone = self.default_timezone

        self.prep_attributes()
        self.build_session_id()

        # now that we're done setting up shop, start the logging
        self.default_logging(require_logging)

    def authenticate_and_login(self):
        logging.info("running authenticate request", extra={'session_id': self.broadsoftinstance.session_id})
        a = AuthenticationRequest.authenticate(broadsoftinstance=self.broadsoftinstance)
        self.broadsoftinstance.auth_object = a

        logging.info("running login request", extra={'session_id': self.broadsoftinstance.session_id})
        self.broadsoftinstance.auth_object = a
        l = LoginRequest.login(broadsoftinstance=self.broadsoftinstance)
        self.broadsoftinstance.login_object = l
        logging.info("continuing with request", extra={'session_id': self.broadsoftinstance.session_id})

    def broadsoftinstance_needed(self):
        # value for broadsoftinstance? not needed.
        if self.broadsoftinstance is not None:
            return False

        return True

    def build_command_shell(self):
        cmd = ET.Element('command')
        cmd.set('xsi:type', self.command_name)
        cmd.set('xmlns', '')
        return cmd

    def build_session_id(self):
        if self.broadsoftinstance.session_id is None:
            # if there's an attached auth object, use that session id
            if self.broadsoftinstance.auth_object:
                try:
                    self.broadsoftinstance.session_id = self.broadsoftinstance.auth_object.broadsoftinstance.session_id
                except AttributeError:
                    pass

            # otherwise, build a fresh one
            if self.broadsoftinstance.session_id is None:
                self.broadsoftinstance.session_id = \
                    socket.gethostname() + ',' + \
                    str(datetime.datetime.utcnow()) + ',' + \
                    str(random.randint(1000000000, 9999999999))

    def check_error(self, string_response):
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
            logging.error(error_msg, extra={'session_id': self.broadsoftinstance.session_id})
            raise RuntimeError(error_msg)

    def convert_booleans(self):
        try:
            for a in self.booleans:
                current_val = getattr(self, a)
                if current_val == 'true' or current_val == 'false':
                    continue

                new_val = 'false'
                if current_val:
                    new_val = 'true'
                setattr(self, a, new_val)
        except AttributeError:
            pass

    def convert_mac_address(self):
        m = MAC(mac=self.mac_address)
        m.denude()
        self.mac_address = m.bare_mac

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
        creds = NistCreds(group='broadsoft', member=self.broadsoftinstance.creds_member)
        self.api_user_id = creds.username
        self.api_password = creds.password

    def is_auth_suite(self):
        # commands that are part of the login/logout suite don't ever need login
        is_auth_suite = False

        # command_name may not exist, so run in try/except. No command_name? Clearly not part of the
        # login/logout suite.
        try:
            if self.command_name in self.auth_exceptions:
                is_auth_suite = True
        except AttributeError:
            pass

        return is_auth_suite

    def need_login(self):
        # not part of the login/logout suite, and no login/auth object attached? need to login.
        if not self.is_auth_suite() and (not self.broadsoftinstance.login_object or not self.broadsoftinstance.auth_object):
            return True

        return False

    def need_logout(self):
        # not part of the login/logout suite, and auto_logout? run logout.
        if not self.is_auth_suite() and self.broadsoftinstance.auto_logout:
            return True

        return False

    def post(self, extract_payload=True):
        # this function is only for descendant objects, like AuthenticationRequest

        command_name = "base BroadsoftRequest"
        try:
            command_name = self.command_name
        except AttributeError:
            pass

        logging.info("running " + command_name + " request", extra={'session_id': self.broadsoftinstance.session_id})

        # if this isn't an auth/login request, check for login object. none? need to login.
        if self.need_login():
            logging.info("auth/login needed.", extra={'session_id': self.broadsoftinstance.session_id})
            self.authenticate_and_login()

        # first, convert self into string representation
        # (to_string() comes from broadsoft.requestobjects.XmlDocument)
        payload = self.to_string()

        # wrap that payload in a SOAP envelope, and convert whole enchilada to a string in order to post to broadsoft
        e = SoapEnvelope(body=payload)
        envelope = e.to_string()

        logging.info("url: " + self.broadsoftinstance.api_url, extra={'session_id': self.broadsoftinstance.session_id})

        # if there's an attached auth object, grab cookies
        cookies = None
        if self.broadsoftinstance.auth_object:
            try:
                cookies = self.broadsoftinstance.auth_object.auth_cookie_jar
                logging.info("cookies: " + str(cookies), extra={'session_id': self.broadsoftinstance.session_id})
                pass
            except AttributeError:
                pass

        logging.info("payload: " + envelope, extra={'session_id': self.broadsoftinstance.session_id})

        # post to server
        headers = {'content-type': 'text/xml', 'SOAPAction': ''}
        response = requests.post(url=self.broadsoftinstance.api_url, data=envelope, headers=headers, cookies=cookies)
        self.last_response = response

        # get a non-200 response?
        if int(response.status_code) > 299:
            error_msg = "got " + str(response.status_code) + " running request"
            logging.error(error_msg, extra={'session_id': self.broadsoftinstance.session_id})
            raise RuntimeError(error_msg)

        # massage the response and check for errors
        content = response.content
        try:
            content = content.decode('utf-8')

        except AttributeError:
            pass

        logging.info("response: " + content, extra={'session_id': self.broadsoftinstance.session_id})
        self.check_error(string_response=content)

        # if we're managing login behavior, also do an implicit logout
        if self.need_logout():
            logging.info("automatically running logout request", extra={'session_id': self.broadsoftinstance.session_id})
            l = LogoutRequest.logout(broadsoftinstance=self.broadsoftinstance)

        # if requested, dig actual message out of SOAP envelope it came in (and return as XML object)
        if extract_payload:
            return BroadsoftRequest.extract_payload(content)

        # otherwise, return entire message as XML object
        xml = ET.fromstring(text=content)
        return xml

    # stuff that happens for multiple request objects which we don't want to mess up
    def prep_attributes(self):
        if hasattr(self, 'did') and self.did:
            self.did = BroadsoftRequest.convert_phone_number(number=self.did)

        if hasattr(self, 'mac_address') and self.mac_address:
            self.convert_mac_address()

        if hasattr(self, 'clid_did') and self.clid_did:
            self.clid_did = BroadsoftRequest.convert_phone_number(number=self.clid_did)

        if hasattr(self, 'phone_type') and self.phone_type:
            self.phone_type = BroadsoftRequest.map_phone_type(phone_type=self.phone_type)

        if self.broadsoftinstance_needed():
            self.broadsoftinstance = instance_factory()

        if self.group_id is None:
            self.group_id = self.broadsoftinstance.default_group_id

    def prep_for_xml(self):
        self.prep_attributes()
        self.convert_booleans()

    def to_xml(self):
        self.prep_for_xml()
        doc = ET.Element('BroadsoftDocument')
        doc.set('protocol', 'OCI')
        doc.set('xmlns', 'C')
        doc.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')

        sid = ET.SubElement(doc, 'sessionId')
        sid.set('xmlns', '')
        sid.text = str(self.broadsoftinstance.session_id)

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

        # obvious intl code at the front? strip it
        number = re.sub('^\+\d+\D', '', number)

        # get rid of any non-numeric characters
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
            if payload:
                return ET.fromstring(text=payload)
        return None

    @staticmethod
    def map_phone_type(phone_type):
        # strip any reference to Expansion Modules
        phone_type = re.sub(r' \+ Expansion Module\(\d+\)$', '', phone_type)

        # if it's not "Polycom SoundPoint IP 550", all "Polycom Soundpoint" devices should be de-camel-cased
        if 'Polycom SoundPoint' in phone_type and phone_type != 'Polycom SoundPoint IP 550':
            phone_type = re.sub(r'SoundPoint', 'Soundpoint', phone_type)

        # if it's "Polycom Soundpoint 650" should be "Polycom Soundpoint IP 650"
        m = re.search(r'^(Polycom Sound[pP]oint) (\d+)$', phone_type)
        if m:
            phone_type = m.group(1) + ' IP ' + m.group(2)

        # otherwise, may be a straightforward mapping
        phone_map = {
            'Cisco SPA232D': ' Generic',
            'Hitachi Wireless IP 5000': ' Generic',
            'Linksys SPA2102': 'Linksys SPA-2102',
            'Linksys SPA3102': 'Linksys SPA-3102',
            'Polycom RealPresence Trio 8800': 'Polycom_Trio8800',
            'Polycom Soundpoint IP 320': 'Polycom Soundpoint IP 320 330',
            'Polycom Soundpoint IP 560': 'Polycom-560',
            'Polycom Soundpoint IP 670': 'Polycom-670',
            'Polycom SoundStation IP 4000': 'Polycom-4000',
            'Polycom SoundStation IP 5000': 'Polycom-5000',
            'Polycom SoundStation IP 6000': 'Polycom-6000',
            'Polycom SoundStation IP 7000': 'Polycom-7000',
            'Polycom Soundpoint IP 600/601': 'Polycom Soundpoint IP 601',
            'Polycom VVX 1500': 'Polycom-VVX1500',
            'Polycom VVX 400': 'Polycom-VVX400',
            'Polycom VVX 600': 'Polycom-VVX600'
        }

        if phone_type in phone_map:
            return phone_map[phone_type]

        else:
            return phone_type


class AuthenticationRequest(BroadsoftRequest):
    command_name = 'AuthenticationRequest'

    def __init__(self, api_user_id=None, api_password=None, **kwargs):
        self.auth_cookie_jar = None
        self.nonce = None
        self.api_user_id = api_user_id
        self.api_password = api_password
        BroadsoftRequest.__init__(self, **kwargs)

    def build_command_xml(self):
        if not self.api_user_id or not self.api_password:
            self.derive_creds()

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

    def __init__(self, use_test=False, api_user_id=None, api_password=None, **kwargs):
        self.api_user_id = api_user_id
        self.api_password = api_password
        BroadsoftRequest.__init__(self, **kwargs)
        if self.broadsoftinstance and self.broadsoftinstance.api_username:
            self.api_user_id = self.broadsoftinstance.api_username
        if self.broadsoftinstance and self.broadsoftinstance.api_password:
            self.api_password = self.broadsoftinstance.api_password

    def build_command_xml(self):
        if not self.api_user_id or not self.api_password:
            self.derive_creds()

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
        concat_pwd = self.broadsoftinstance.auth_object.nonce + ':' + sha_pwd
        m = md5()
        m.update(concat_pwd.encode())
        signed_pwd = m.hexdigest()

        return signed_pwd

    @staticmethod
    def login(**kwargs):
        l = LoginRequest(**kwargs)
        l.post()
        return l


class LogoutRequest(BroadsoftRequest):
    command_name = 'LogoutRequest'

    def __init__(self, api_user_id=None, api_password=None, **kwargs):
        self.api_user_id = api_user_id
        self.api_password = api_password
        BroadsoftRequest.__init__(self, **kwargs)

    def build_command_xml(self):
        cmd = self.build_command_shell()

        uid = ET.SubElement(cmd, 'userId')
        uid.text = self.api_user_id

        return cmd

    def post(self, **kwargs):
        BroadsoftRequest.post(self, **kwargs)

        # now that we've logged out, blank out auth related attrs of broadsoftinstance, which clears the way for another
        # auth session should it be needed
        self.broadsoftinstance.auth_object = None
        self.broadsoftinstance.login_object = None
        self.broadsoftinstance.session_id = None

    @staticmethod
    def logout(**kwargs):
        l = LogoutRequest(**kwargs)
        l.post()
        return l


class BroadsoftInstance:
    default_group_id = 'mit'

    def __init__(self, group_id='mit', auth_object=None, login_object=None, session_id=None):
        # these attrs relate to communicating with the Broadsoft API
        self.api_password = None
        self.api_url = '[unknown]'
        self.api_username = None
        self.auth_object = auth_object
        self.auto_logout = True
        self.creds_member = 'prod'
        self.login_object = login_object
        self.session_id = session_id

        # these attrs are inherited by request objects
        self.default_domain = 'broadsoft.mit.edu'
        self.service_provider = 'ENT136'

    def login(self):
        r = BroadsoftRequest(broadsoftinstance=self)
        r.authenticate_and_login()

    def logout(self):
        l = LogoutRequest.logout(broadsoftinstance=self)


class SandboxBroadsoftInstance(BroadsoftInstance):
    def __init__(self, **kwargs):
        BroadsoftInstance.__init__(self, **kwargs)

        # overwrite attrs that are different for test instance
        self.api_url = 'https://mit-lab.oci-us99.bwks.io/webservice/services/ProvisioningService'
        self.api_username = 'resMIT_lab'
        self.api_password = 'PmitAlaSb01'
        self.default_domain = 'broadsoft-dev.mit.edu'
        self.service_provider = 'ENT136'


class TestBroadsoftInstance(BroadsoftInstance):
    def __init__(self, **kwargs):
        BroadsoftInstance.__init__(self, **kwargs)

        # overwrite attrs that are different for test instance
        self.api_url = 'https://web1.voiplogic.net/webservice/services/ProvisioningService'
        self.creds_member = 'test'
        self.default_domain = 'broadsoft-dev.mit.edu'
        self.service_provider = 'ENT136'


def instance_factory(use_test=False) -> object:
    if use_test:
        return TestBroadsoftInstance()

    return BroadsoftInstance()