from broadsoft.requestobjects.lib.BroadsoftRequest import BroadsoftRequest
from broadsoft.requestobjects.UserAddRequest import UserAddRequest
from broadsoft.requestobjects.UserModifyRequest import UserModifyRequest
from broadsoft.requestobjects.UserServiceAssignListRequest import UserServiceAssignListRequest
from broadsoft.requestobjects.UserSharedCallAppearanceAddEndpointRequest import UserSharedCallAppearanceAddEndpointRequest
from broadsoft.BroadsoftObject import BroadsoftObject


class Account(BroadsoftObject):
    # these are optional broadsoft services that will get applied by default to every new
    # account
    default_services = [
        'Shared Call Appearance 10'
    ]

    def __init__(self, did=None, extension=None, last_name=None, first_name=None,
                 sip_user_id=None, kname=None, email=None, use_test=False, services=None,
                 **kwargs):
        self.did = did
        self.email = email
        self.first_name = first_name
        self.kname = kname
        self.last_name = last_name
        self.services = self.default_services
        if services:
            if type(services) == str:
                services = [services]
            self.services = services
        self.use_test = use_test

        # these are optional; will be derived by broadsoft.RequestObjects as needed
        self.extension = extension
        self.sip_user_id = sip_user_id

        # fully optional; Devices associated with this Account (should be broadsoft.Device objects)
        self.devices = []

        BroadsoftObject.__init__(self, **kwargs)

    def add_devices(self, req_object):
        if len(self.devices) > 0:
            # first, all devices get added to system
            for d in self.devices:
                d_ro = d.build_request_object()
                d_ro.use_test = self.use_test
                req_object.commands.append(d_ro)

            # first device gets associated directly with user
            self.link_primary_device(req_object=req_object, device=self.devices[0])

            # remaining devices get added as shared call appearances
            for d in self.devices[1:]:
                self.link_sca_device(req_object=req_object, device=d)

    def add_services(self, req_object):
        if self.services and len(self.services) > 0:
            s = UserServiceAssignListRequest(use_test=self.use_test)
            s.did = self.did
            s.sip_user_id = self.sip_user_id
            s.services = self.services
            req_object.commands.append(s)

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

        # if there are services to add for user, add them
        self.add_services(req_object=b)

        # if there are devices to add for user, add them
        self.add_devices(req_object=b)

        return b

    def link_primary_device(self, req_object, device):
        u_mod = UserModifyRequest(did=self.did, sip_user_id=self.sip_user_id,
                                  device_name=device.name, use_test=self.use_test)
        req_object.commands.append(u_mod)

    def link_sca_device(self, req_object, device):
        line_port = device.line_port
        if not line_port:
            line_port = device.name + '_lp@' + req_object.default_domain
        sca = UserSharedCallAppearanceAddEndpointRequest(did=self.did, sip_user_id=self.sip_user_id,
                                                         device_name=device.name, line_port=line_port,
                                                         use_test=self.use_test)
        req_object.commands.append(sca)