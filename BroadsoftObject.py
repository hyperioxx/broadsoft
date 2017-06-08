import xml.etree.ElementTree as ET
from broadsoft.requestobjects.lib.BroadsoftRequest import BroadsoftRequest
from broadsoft import BroadsoftInstance


class BroadsoftObject:
    prod_default_domain = 'broadsoft.mit.edu'
    test_default_domain = 'broadsoft-dev.mit.edu'

    def __init__(self, xml=None, use_test=False, broadsoft_instance=None):
        self.xml = xml
        self.broadsoft_instance = broadsoft_instance
        self.default_domain = None
        self.use_test = use_test
        self.prep_attributes()

    def derive_sip_user_id(self, did):
        did = BroadsoftRequest.convert_phone_number(number=did)
        return did + '@' + self.default_domain

    def derive_default_domain(self):
        self.default_domain = self.prod_default_domain
        if self.use_test:
            self.default_domain = self.test_default_domain

    def from_xml(self):
        self.prep_attributes()

    def prep_attributes(self):
        self.derive_default_domain()

        if hasattr(self, 'did') and self.did:
            self.did = BroadsoftRequest.convert_phone_number(number=self.did)

        if hasattr(self, 'sip_user_id') and self.did and self.sip_user_id is None:
            self.sip_user_id = self.derive_sip_user_id(did=self.did)

        if self.xml and type(self.xml) is str:
            self.xml = ET.fromstring(self.xml)

        if self.broadsoft_instance is None:
            self.broadsoft_instance = self.derive_broadsoft_instance(use_test=self.use_test)

    def provision(self):
        ro = self.build_provision_request()
        results = ro.post()
        return results

    @staticmethod
    def derive_broadsoft_instance(use_test):
        return BroadsoftInstance.factory(use_test=use_test)
