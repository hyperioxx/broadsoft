import unittest

from broadsoft.lib import BroadsoftInstance


class TestBroadsoftInstance(unittest.TestCase):
    def test_factory(self):
        b = BroadsoftInstance.factory()
        self.assertIsInstance(b, BroadsoftInstance.BroadsoftInstance)

        b = BroadsoftInstance.factory(use_test=False)
        self.assertIsInstance(b, BroadsoftInstance.BroadsoftInstance)

        b = BroadsoftInstance.factory(use_test=True)
        self.assertIsInstance(b, BroadsoftInstance.TestBroadsoftInstance)
