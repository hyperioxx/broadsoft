import unittest.mock
from broadsoft.Device import Device
from broadsoft.Account import Account
from broadsoft.requestobjects.lib.BroadsoftRequest import BroadsoftRequest
from broadsoft.requestobjects.UserAddRequest import UserAddRequest
from broadsoft.requestobjects.UserModifyRequest import UserModifyRequest
from broadsoft.requestobjects.UserServiceAssignListRequest import UserServiceAssignListRequest
from broadsoft.requestobjects.GroupAccessDeviceAddRequest import GroupAccessDeviceAddRequest
from broadsoft.requestobjects.UserSharedCallAppearanceAddEndpointRequest import UserSharedCallAppearanceAddEndpointRequest


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
                    use_test=True, services=['a'])
        a.devices = [d1, d2]
        ro = a.build_request_object()

        # expect to see 6 commands in the request object...
        self.assertEqual(6, len(ro.commands))

        # ... one to add the user
        cmd = ro.commands[0]
        self.assertIsInstance(cmd, UserAddRequest)

        # ... one to configure services
        cmd = ro.commands[1]
        self.assertIsInstance(cmd, UserServiceAssignListRequest)
        self.assertEqual(['a'], cmd.services)

        # ... one to add d1
        cmd = ro.commands[2]
        self.assertIsInstance(cmd, GroupAccessDeviceAddRequest)
        self.assertEqual(cmd.device_name, 'beaverphone1')

        # ... one to add d2
        cmd = ro.commands[3]
        self.assertIsInstance(cmd, GroupAccessDeviceAddRequest)
        self.assertEqual(cmd.device_name, 'beaverphone2')

        # ... one to associate d1 with the user directly
        cmd = ro.commands[4]
        self.assertIsInstance(cmd, UserModifyRequest)
        self.assertEqual(cmd.device_name, 'beaverphone1')

        # ... one to associate d2 with the user as shared call appearance
        cmd = ro.commands[5]
        self.assertIsInstance(cmd, UserSharedCallAppearanceAddEndpointRequest)
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

    def test_inherits_default_services(self):
        a = Account()
        self.assertEqual(a.default_services, a.services)

        # and can override default services
        a = Account(services=['a'])
        self.assertEqual(['a'], a.services)

    def test_add_services(self):
        # when no services specified, should get default services in UserServiceAssignListRequest object
        a = Account()
        b = BroadsoftRequest()
        a.add_services(req_object=b)
        s = b.commands[0]
        self.assertIsInstance(s, UserServiceAssignListRequest)
        self.assertEqual(a.default_services, s.services)

        # when services overridden, should get inserted
        a = Account(services=['a','b'])
        b = BroadsoftRequest()
        a.add_services(req_object=b)
        s = b.commands[0]
        self.assertIsInstance(s, UserServiceAssignListRequest)
        self.assertEqual(['a','b'], s.services)

    def test_link_primary_device(self):
        a = Account(did=6175551212)
        b = BroadsoftRequest()
        d1 = Device(description='beaver phone 1', name='beaverphone1', type='iphone', use_test=False)
        a.link_primary_device(req_object=b, device=d1)
        self.assertEqual(1, len(b.commands))
        cmd = b.commands[0]
        self.assertIsInstance(cmd, UserModifyRequest)
        self.assertEqual(cmd.did, str(a.did))
        self.assertEqual(cmd.sip_user_id, str(a.did) + '@' + b.default_domain)
        self.assertEqual(cmd.device_name, d1.name)

    def test_link_sca_device(self):
        a = Account(did=6175551212)
        b = BroadsoftRequest()
        d1 = Device(description='beaver phone 1', name='beaverphone1', type='iphone', use_test=False)
        a.link_sca_device(req_object=b, device=d1)
        self.assertEqual(1, len(b.commands))
        cmd = b.commands[0]
        self.assertIsInstance(cmd, UserSharedCallAppearanceAddEndpointRequest)
        self.assertEqual(cmd.did, str(a.did))
        self.assertEqual(cmd.sip_user_id, str(a.did) + '@' + b.default_domain)
        self.assertEqual(cmd.device_name, d1.name)
        self.assertEqual(cmd.line_port, d1.name + '_lp@' + b.default_domain)

    def test_add_devices(self):
        a = Account(did=6175551212)
        b = BroadsoftRequest()
        d1 = Device(description='beaver phone 1', name='beaverphone1', type='iphone', use_test=False)
        d2 = Device(description='beaver phone 2', name='beaverphone2', type='cisco', use_test=False)
        a.devices = [d1, d2]
        a.add_devices(req_object=b)

        # should be four requests
        self.assertEqual(4, len(b.commands))

        # Not going to investigate each one in details, that's handled in test_link_primary_device() and
        # test_link_sca_device(). Just checking for object type and order.
        cmd = b.commands[0]
        self.assertIsInstance(cmd, GroupAccessDeviceAddRequest)
        self.assertEqual(d1.name, cmd.device_name)

        cmd = b.commands[1]
        self.assertIsInstance(cmd, GroupAccessDeviceAddRequest)
        self.assertEqual(d2.name, cmd.device_name)

        cmd = b.commands[2]
        self.assertIsInstance(cmd, UserModifyRequest)
        self.assertEqual(d1.name, cmd.device_name)

        cmd = b.commands[3]
        self.assertIsInstance(cmd, UserSharedCallAppearanceAddEndpointRequest)
        self.assertEqual(d2.name, cmd.device_name)
