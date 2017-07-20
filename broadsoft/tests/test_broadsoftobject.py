import unittest
import unittest.mock

import broadsoft.requestobjects.lib.BroadsoftRequest
from broadsoft.lib.BroadsoftObject import BroadsoftObject
from broadsoft.Device import Device
from broadsoft.requestobjects.lib.BroadsoftRequest import BroadsoftRequest
from broadsoft.requestobjects.UserAddRequest import UserAddRequest


def return_none(*args, **kwargs):
    return None


class TestBroadsoftObject(unittest.TestCase):
    @unittest.mock.patch.object(BroadsoftObject, 'prep_attributes')
    def test_pass_broadsoftinstance(
            self, prep_attributes_patch
    ):
        b = BroadsoftObject(broadsoftinstance='a')
        self.assertEqual('a', b.broadsoftinstance)

    def test_derive_broadsoftinstance(self):
        self.assertIsInstance(
            BroadsoftObject.derive_broadsoft_instance(instance='prod'),
            broadsoft.requestobjects.lib.BroadsoftRequest.BroadsoftInstance)

        self.assertIsInstance(
            BroadsoftObject.derive_broadsoft_instance(instance='test'),
            broadsoft.requestobjects.lib.BroadsoftRequest.TestBroadsoftInstance)

    @unittest.mock.patch.object(BroadsoftObject, 'derive_broadsoft_instance')
    def test_init_calls_derive_broadsoftinstance(
            self, derive_broadsoft_instance_patch):
        # implicit instance
        b = BroadsoftObject()
        self.assertTrue(derive_broadsoft_instance_patch.called)
        call = derive_broadsoft_instance_patch.call_args_list[0]
        args, kwargs = call
        self.assertEqual(kwargs['instance'], 'prod')
        derive_broadsoft_instance_patch.called = False

        # test instance
        b = BroadsoftObject(instance='test')
        self.assertTrue(derive_broadsoft_instance_patch.called)
        call = derive_broadsoft_instance_patch.call_args_list[1]
        args, kwargs = call
        self.assertEqual(kwargs['instance'], 'test')
        derive_broadsoft_instance_patch.called = False

        # prod instance
        b = BroadsoftObject(instance='prod')
        self.assertTrue(derive_broadsoft_instance_patch.called)
        call = derive_broadsoft_instance_patch.call_args_list[2]
        args, kwargs = call
        self.assertEqual(kwargs['instance'], 'prod')
        derive_broadsoft_instance_patch.called = False

    @unittest.mock.patch.object(BroadsoftRequest, 'authenticate_and_login')
    @unittest.mock.patch.object(BroadsoftRequest, '__init__', side_effect=return_none)
    def test_login_passes_broadsoftinstance(self, init_patch, auth_patch):
        i = broadsoft.requestobjects.lib.BroadsoftRequest.instance_factory(instance='test')
        o = BroadsoftObject(broadsoftinstance=i)
        o.login()

        call = init_patch.call_args_list[0]
        args, kwargs = call
        self.assertIsInstance(kwargs['broadsoftinstance'],
                              broadsoft.requestobjects.lib.BroadsoftRequest.TestBroadsoftInstance)

    @unittest.mock.patch('broadsoft.requestobjects.lib.BroadsoftRequest.LogoutRequest.logout')
    def test_logout_passes_broadsoftinstance(self, logout_patch):
        i = broadsoft.requestobjects.lib.BroadsoftRequest.instance_factory(instance='test')
        o = BroadsoftObject(broadsoftinstance=i)
        o.logout()

        call = logout_patch.call_args_list[0]
        args, kwargs = call
        self.assertIsInstance(kwargs['broadsoftinstance'],
                              broadsoft.requestobjects.lib.BroadsoftRequest.TestBroadsoftInstance)
