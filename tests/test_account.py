import unittest.mock
from broadsoft.Device import Device
from broadsoft.Account import Account
from broadsoft.requestobjects.UserAddRequest import UserAddRequest
from broadsoft.requestobjects.UserModifyRequest import UserModifyRequest
from broadsoft.requestobjects.GroupAccessDeviceAddRequest import GroupAccessDeviceAddRequest


class TestBroadsoftAccount(unittest.TestCase):
    def test_account_attrs_get_passed_to_request_object(self):
        a = Account(did=6175551212, extension=51212, last_name='beaver', first_name='tim',
                    sip_user_id='beaver@broadsoft.mit.edu', kname='beaver', email='beaver@mit.edu',
                    use_test=True)
        ro = a.build_request_object()
        uadd = ro.commands[0]
        self.assertEqual(a.did, uadd.did)
        self.assertEqual(a.last_name, uadd.last_name)
        self.assertEqual(a.first_name, uadd.first_name)
        self.assertEqual(a.sip_user_id, uadd.sip_user_id)
        self.assertEqual(a.kname, uadd.kname)
        self.assertEqual(a.email, uadd.email)
        self.assertEqual(a.use_test, uadd.use_test)

        # try again, flip-flopping use test
        a = Account(did=6175551212, extension=51212, last_name='beaver', first_name='tim',
                    sip_user_id='beaver@broadsoft.mit.edu', kname='beaver', email='beaver@mit.edu',
                    use_test=False)
        ro = a.build_request_object()
        uadd = ro.commands[0]
        self.assertEqual(a.did, uadd.did)
        self.assertEqual(a.last_name, uadd.last_name)
        self.assertEqual(a.first_name, uadd.first_name)
        self.assertEqual(a.sip_user_id, uadd.sip_user_id)
        self.assertEqual(a.kname, uadd.kname)
        self.assertEqual(a.email, uadd.email)
        self.assertEqual(a.use_test, uadd.use_test)

    def test_devices_added_get_built_into_request_object(self):
        d1 = Device(description='beaver phone 1', name='beaverphone1', type='iphone')
        d2 = Device(description='beaver phone 2', name='beaverphone2', type='hamburger')
        a = Account(did=6175551212, extension=51212, last_name='beaver', first_name='tim',
                    sip_user_id='beaver@broadsoft.mit.edu', kname='beaver', email='beaver@mit.edu',
                    use_test=True)
        a.devices = [d1, d2]
        ro = a.build_request_object()

        # expect to see 5 commands in the request object...
        self.assertEqual(5, len(ro.commands))

        # ... one to add the user
        cmd = ro.commands[0]
        self.assertIsInstance(cmd, UserAddRequest)

        # ... one to add d1
        cmd = ro.commands[1]
        self.assertIsInstance(cmd, GroupAccessDeviceAddRequest)
        self.assertEqual(cmd.device_name, 'beaverphone1')

        # ... one to associate d1 with the user
        cmd = ro.commands[2]
        self.assertIsInstance(cmd, UserModifyRequest)
        self.assertEqual(cmd.device_name, 'beaverphone1')

        # ... one to add d2
        cmd = ro.commands[3]
        self.assertIsInstance(cmd, GroupAccessDeviceAddRequest)
        self.assertEqual(cmd.device_name, 'beaverphone2')

        # ... one to associate d2 with the user
        cmd = ro.commands[4]
        self.assertIsInstance(cmd, UserModifyRequest)
        self.assertEqual(cmd.device_name, 'beaverphone2')

    def test_child_objects_inherit_use_test(self):
        d1 = Device(description='beaver phone 1', name='beaverphone1', type='iphone', use_test=False)
        a = Account(did=6175551212, extension=51212, last_name='beaver', first_name='tim',
                    sip_user_id='beaver@broadsoft.mit.edu', kname='beaver', email='beaver@mit.edu',
                    use_test=True)
        a.devices = [d1]
        ro = a.build_request_object()
        for cmd in ro.commands:
            self.assertTrue(cmd.use_test)
