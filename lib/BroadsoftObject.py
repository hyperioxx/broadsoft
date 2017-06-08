import xml.etree.ElementTree as ET

from broadsoft.lib import BroadsoftInstance
from broadsoft.requestobjects.lib.BroadsoftRequest import BroadsoftRequest


class BroadsoftObject:
    def __init__(self, xml=None, use_test=False, broadsoftinstance=None):
        self.xml = xml
        self.broadsoftinstance = broadsoftinstance
        self.default_domain = None
        self.use_test = use_test
        self.prep_attributes()

    def derive_sip_user_id(self, did):
        did = BroadsoftRequest.convert_phone_number(number=did)

        if not did:
            raise ValueError("can't run BroadsoftObject.derive_sip_user_id without a value for did")

        if not self.default_domain:
            raise ValueError("can't run BroadsoftObject.derive_sip_user_id without a value for default_domain")

        return did + '@' + self.default_domain

    def derive_default_domain(self):
        if self.broadsoftinstance:
            self.default_domain = self.broadsoftinstance.default_domain

    def from_xml(self):
        self.prep_attributes()

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
            try:
                child.apply_broadsoftinstance(force=True)
            except AttributeError:
                pass

    def prep_attributes(self):
        if self.broadsoftinstance is None:
            self.broadsoftinstance = self.derive_broadsoft_instance(use_test=self.use_test)

        self.derive_default_domain()

        if hasattr(self, 'did') and self.did:
            self.did = BroadsoftRequest.convert_phone_number(number=self.did)

        if hasattr(self, 'sip_user_id') and self.did and self.sip_user_id is None:
            self.sip_user_id = self.derive_sip_user_id(did=self.did)

        if self.xml and type(self.xml) is str:
            self.xml = ET.fromstring(self.xml)

    def provision(self):
        ro = self.build_provision_request()
        results = ro.post()
        return results

    @staticmethod
    def derive_broadsoft_instance(use_test):
        return BroadsoftInstance.factory(use_test=use_test)
