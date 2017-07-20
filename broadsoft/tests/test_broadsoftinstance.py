import unittest
import broadsoft.requestobjects.lib.BroadsoftRequest


class TestBroadsoftInstance(unittest.TestCase):
    def test_factory(self):
        b = broadsoft.requestobjects.lib.BroadsoftRequest.instance_factory()
        self.assertIsInstance(b, broadsoft.requestobjects.lib.BroadsoftRequest.BroadsoftInstance)

        b = broadsoft.requestobjects.lib.BroadsoftRequest.instance_factory(instance='prod')
        self.assertIsInstance(b, broadsoft.requestobjects.lib.BroadsoftRequest.BroadsoftInstance)

        b = broadsoft.requestobjects.lib.BroadsoftRequest.instance_factory(instance='dev')
        self.assertIsInstance(b, broadsoft.requestobjects.lib.BroadsoftRequest.DevBroadsoftInstance)

        b = broadsoft.requestobjects.lib.BroadsoftRequest.instance_factory(instance='test')
        self.assertIsInstance(b, broadsoft.requestobjects.lib.BroadsoftRequest.TestBroadsoftInstance)
