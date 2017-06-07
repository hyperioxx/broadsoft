import unittest
from broadsoft.BroadsoftObject import BroadsoftObject
from broadsoft.Account import Account

class TestBroadsoftObject(unittest.TestCase):
    def test_derive_domain_based_on_test_and_prod(self):
        b = BroadsoftObject(use_test=False)
        self.assertEqual(b.prod_default_domain, b.default_domain)

        b = BroadsoftObject(use_test=True)
        self.assertEqual(b.test_default_domain, b.default_domain)
