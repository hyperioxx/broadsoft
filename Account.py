from broadsoft.requestobjects.lib.BroadsoftRequest import BroadsoftRequest
from broadsoft.requestobjects.UserAddRequest import UserAddRequest
from broadsoft.requestobjects.GroupAccessDeviceAddRequest import GroupAccessDeviceAddRequest


class Account:
    def __init__(self, did=None, extension=None, last_name=None, first_name=None,
                 sip_user_id=None, kname=None, email=None, use_test=False):
        self.did = did
        self.email = email
        self.first_name = first_name
        self.kname = kname
        self.last_name = last_name
        self.use_test = use_test

        # these are optional; will be derived by broadsoft.RequestObjects as needed
        self.extension = extension
        self.sip_user_id = sip_user_id

        # fully optional
        self.devices = []

    def provision(self):
        # going to do this as a compound request so that it's pseudo-atomic...if one fails, the rest should
        # fail, regardless of where in the process that failure occurs

        # object to create the user
        u_add = UserAddRequest(use_test=self.use_test)
        u_add.first_name = self.first_name
        u_add.last_name = self.last_name
        u_add.did = self.did
        u_add.kname = self.kname
        u_add.sip_user_id = self.sip_user_id

        # object to create device
        # create one device request object per device

        # now add these commands to one master BroadsoftRequest object
        b = BroadsoftRequest(use_test=self.use_test)
        b.commands = [u_add]

        """
        GroupAccessDeviceAddRequest
            device_name
            device_type
            device_description
        
        UserModifyRequest
            sip_user_id *
            did
            device_name *
        """
        pass
