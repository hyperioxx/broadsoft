import unittest
import broadsoft.requestobjects.lib.BroadsoftRequest


class TestBroadsoftInstance(unittest.TestCase):
    def test_factory(self):
        b = broadsoft.requestobjects.lib.BroadsoftRequest.instance_factory()
        self.assertIsInstance(b, broadsoft.requestobjects.lib.BroadsoftRequest.BroadsoftInstance)

        b = broadsoft.requestobjects.lib.BroadsoftRequest.instance_factory(use_test=False)
        self.assertIsInstance(b, broadsoft.requestobjects.lib.BroadsoftRequest.BroadsoftInstance)

        b = broadsoft.requestobjects.lib.BroadsoftRequest.instance_factory(use_test=True)
        self.assertIsInstance(b, broadsoft.requestobjects.lib.BroadsoftRequest.TestBroadsoftInstance)
