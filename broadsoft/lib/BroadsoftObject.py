import xml.etree.ElementTree as ET
import broadsoft.requestobjects.lib.BroadsoftRequest
from broadsoft.requestobjects.lib.BroadsoftRequest import BroadsoftRequest
from broadsoft.requestobjects.lib.BroadsoftRequest import LogoutRequest
import logging
import copy
import re


class BroadsoftObject:
    def __init__(self, xml=None, implicit_overwrite=False, skip_if_exists=False, instance='prod',
                 broadsoftinstance=None, logging_level='info'):
        self.broadsoftinstance = broadsoftinstance
        self.fetched = None
        self.implicit_overwrite = implicit_overwrite
        self.instance = instance
        self.logging_level = logging_level
        self.skip_if_exists = skip_if_exists
        self.xml = xml
        self.prep_attributes()

    def check_if_object_fetched(self):
        if self.xml:
            commands = self.xml.findall('./command')
            for command in commands:
                command_name = command.get('{http://www.w3.org/2001/XMLSchema-instance}type')
                if 'ErrorResponse' in command_name:
                    self.fetched = False
                elif 'GetResponse' in command_name:
                    self.fetched = True
        else:
            self.fetched = False

    def derive_sip_user_id(self, did):
        did = BroadsoftRequest.convert_phone_number(number=did)

        if not did:
            raise ValueError("can't run BroadsoftObject.derive_sip_user_id without a value for did")

        if not self.broadsoftinstance.default_domain:
            raise ValueError("can't run BroadsoftObject.derive_sip_user_id without a value for default_domain")

        return did + '@' + self.broadsoftinstance.default_domain

    def from_xml(self):
        self.prep_attributes()
        self.check_if_object_fetched()

    # Ensures that child objects inherit same BroadsoftInstance as parent (sets parameters like URL, enterprise name,
    # creds group, etc).
    # Obviously, can't run this with set-and-fire static methods, so we have to pass BroadsoftInstance directly for
    # those. Admittedly, it's a little confusing that there are two separate methods for inserting the BroadsoftInstance
    # into child object calls. However, in the case of Device objects added to an Account object, we don't have direct
    # control over the __init__ phase of the object's lifecycle. So injection is best for that, and is easier to test.
    # For the static methods calls, we add at __init__.
    def inject_broadsoftinstance(self, child):
        if self.broadsoftinstance:
            child.broadsoftinstance = self.broadsoftinstance

    def login(self):
        r = BroadsoftRequest(broadsoftinstance=self.broadsoftinstance)
        r.authenticate_and_login()

    def logout(self):
        l = LogoutRequest.logout(broadsoftinstance=self.broadsoftinstance)

    # looks like we can't pass more than 15 commands in a request; here we break
    # up requests with more than that
    def paginate_request(self, request):
        # does the object not have "commands" populated? is a unitary object and should be handed back as single element
        # list
        if len(request.commands) == 0:
            return [request]

        # split out the commands based on the max listed in BroadsoftRequest.max_commands_per_request
        command_pages = []
        command_page = []
        for c in request.commands:
            command_page.append(c)
            if len(command_page) == BroadsoftRequest.max_commands_per_request:
                command_pages.append(command_page)
                command_page = []

        # catch last page if needed
        if len(command_page) > 0:
            command_pages.append(command_page)
            command_page = []

        # now build individual requests that are clones of the original, but with a single page of commands
        requests = []
        for page in command_pages:
            paged_request = copy.deepcopy(request)
            paged_request.commands = page
            requests.append(paged_request)

        if len(requests) > 1:
            logging.info("request has been paginated; atomicity not preserved", extra={'session_id': self.broadsoftinstance.session_id})

        return requests

    def prep_attributes(self):
        if self.broadsoftinstance is None:
            self.broadsoftinstance = self.derive_broadsoft_instance(instance=self.instance)

        if hasattr(self, 'did') and self.did:
            self.did = BroadsoftRequest.convert_phone_number(number=self.did)

        if hasattr(self, 'sip_user_id') and self.did and self.sip_user_id is None:
            self.sip_user_id = self.derive_sip_user_id(did=self.did)

        if self.xml and type(self.xml) is str:
            self.xml = ET.fromstring(self.xml)

        if hasattr(self, 'kname') and hasattr(self, 'email') and self.kname is not None and self.email is None:
            self.email = self.kname + '@mit.edu'

    def provision(self):
        if self.implicit_overwrite:
            self.overwrite()

        request_object = self.build_provision_request()
        request_objects = self.paginate_request(request=request_object)

        for request_object in request_objects:
            request_object.logging_level = self.logging_level
            try:
                request_object.post()

            except RuntimeError as e:
                if self.should_skip_error(error=str(e)):
                    pass

                else:
                    raise(e)

    def should_skip_error(self, error):
        skip = False
        if self.skip_if_exists:
            if re.match(r'the SOAP server threw an error: \[Error 4[25]00\] .+? already exists:.+$', error):
                skip = True

        return skip

    @staticmethod
    def derive_broadsoft_instance(instance='prod'):
        return broadsoft.requestobjects.lib.BroadsoftRequest.instance_factory(instance=instance)
