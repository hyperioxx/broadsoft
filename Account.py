from broadsoft.requestobjects.lib.BroadsoftRequest import BroadsoftRequest
from broadsoft.requestobjects.UserAddRequest import UserAddRequest
from broadsoft.requestobjects.UserModifyRequest import UserModifyRequest
from broadsoft.BroadsoftObject import BroadsoftObject


class Account(BroadsoftObject):
    def __init__(self, did=None, extension=None, last_name=None, first_name=None,
                 sip_user_id=None, kname=None, email=None, use_test=False, **kwargs):
        self.did = did
        self.email = email
        self.first_name = first_name
        self.kname = kname
        self.last_name = last_name
        self.use_test = use_test

        # these are optional; will be derived by broadsoft.RequestObjects as needed
        self.extension = extension
        self.sip_user_id = sip_user_id

        # fully optional; Devices associated with this Account (should be broadsoft.Device objects)
        self.devices = []

        BroadsoftObject.__init__(self, **kwargs)

    def build_request_object(self):
        # going to do this as a compound request so that it's pseudo-atomic...if one fails, the rest should
        # fail, regardless of where in the process that failure occurs
        b = BroadsoftRequest(use_test=self.use_test)

        # object to create the user
        u_add = UserAddRequest(use_test=self.use_test)
        u_add.first_name = self.first_name
        u_add.last_name = self.last_name
        u_add.did = self.did
        u_add.kname = self.kname
        u_add.sip_user_id = self.sip_user_id
        u_add.email = self.email
        b.commands = [u_add]

        # now, for each Device added...
        for d in self.devices:
            # ...want to run a device add request
            d_ro = d.build_request_object()
            d_ro.use_test = self.use_test
            b.commands.append(d_ro)

            # ...and then associate it with this user
            u_mod = UserModifyRequest(use_test=self.use_test)
            u_mod.sip_user_id = self.sip_user_id
            u_mod.did = d.did
            u_mod.device_name = d.name
            b.commands.append(u_mod)

        return b
