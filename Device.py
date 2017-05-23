from broadsoft.requestobjects.GroupAccessDeviceAddRequest import GroupAccessDeviceAddRequest
from broadsoft.BroadsoftObject import BroadsoftObject


class Device(BroadsoftObject):
    def __init__(self, name, type, description, did=None, extension=None, use_test=False, mac_address=None, protocol=None,
                 transport_protocol=None, **kwargs):
        self.description = description
        self.name = name
        self.type = type
        self.use_test = use_test

        # optional
        self.did = did
        self.mac_address = mac_address
        self.protocol = protocol
        self.transport_protocol = transport_protocol

        # optional; will be derived by broadsoft.RequestObjects as needed
        self.extension = extension

        BroadsoftObject.__init__(self, **kwargs)

    def build_request_object(self):
        g = GroupAccessDeviceAddRequest(use_test=self.use_test)
        g.description = self.description
        g.device_name = self.name
        g.device_type = self.type
        g.mac_address = self.mac_address
        if self.protocol:
            g.protocol = self.protocol
        if self.transport_protocol:
            g.transport_protocol = self.transport_protocol
        return g