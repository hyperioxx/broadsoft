import unittest
import unittest.mock
from broadsoft.lib import BroadsoftInstance
from broadsoft.lib.BroadsoftObject import BroadsoftObject


class TestBroadsoftObject(unittest.TestCase):
    def test_derive_domain_based_on_test_and_prod(self):
        i = BroadsoftInstance.factory(use_test=False)
        b = BroadsoftObject(use_test=False)
        self.assertEqual(i.default_domain, b.default_domain)

        i = BroadsoftInstance.factory(use_test=True)
        b = BroadsoftObject(use_test=True)
        self.assertEqual(i.default_domain, b.default_domain)

    @unittest.mock.patch.object(BroadsoftObject, 'prep_attributes')
    def test_pass_broadsoftinstance(
            self, prep_attributes_patch
    ):
        b = BroadsoftObject(broadsoftinstance='a')
        self.assertEqual('a', b.broadsoftinstance)

    def test_derive_broadsoftinstance(self):
        self.assertIsInstance(
            BroadsoftObject.derive_broadsoft_instance(use_test=False),
            BroadsoftInstance.BroadsoftInstance)

        self.assertIsInstance(
            BroadsoftObject.derive_broadsoft_instance(use_test=True),
            BroadsoftInstance.TestBroadsoftInstance)

    @unittest.mock.patch.object(BroadsoftObject, 'derive_broadsoft_instance')
    def test_init_calls_derive_broadsoftinstance(
            self, derive_broadsoft_instance_patch):
        # implicit use_test
        b = BroadsoftObject()
        self.assertTrue(derive_broadsoft_instance_patch.called)
        call = derive_broadsoft_instance_patch.call_args_list[0]
        args, kwargs = call
        self.assertFalse(kwargs['use_test'])
        derive_broadsoft_instance_patch.called = False

        # use_test True
        b = BroadsoftObject(use_test=True)
        self.assertTrue(derive_broadsoft_instance_patch.called)
        call = derive_broadsoft_instance_patch.call_args_list[1]
        args, kwargs = call
        self.assertTrue(kwargs['use_test'])
        derive_broadsoft_instance_patch.called = False

        # use_test False
        b = BroadsoftObject(use_test=False)
        self.assertTrue(derive_broadsoft_instance_patch.called)
        call = derive_broadsoft_instance_patch.call_args_list[2]
        args, kwargs = call
        self.assertFalse(kwargs['use_test'])
        derive_broadsoft_instance_patch.called = False

    def test_injected_broadsoftinstance_overrides_prior_settings_in_child_object(self):
        self.assertFalse("write this")
