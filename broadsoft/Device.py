from broadsoft.lib.BroadsoftObject import BroadsoftObject
from broadsoft.requestobjects.GroupAccessDeviceAddRequest import GroupAccessDeviceAddRequest
from broadsoft.requestobjects.GroupAccessDeviceGetRequest import GroupAccessDeviceGetRequest
from broadsoft.requestobjects.GroupAccessDeviceModifyRequest import GroupAccessDeviceModifyRequest
from broadsoft.requestobjects.lib.BroadsoftRequest import BroadsoftRequest
from broadsoft.requestobjects.GroupAccessDeviceDeleteRequest import GroupAccessDeviceDeleteRequest
from broadsoft.requestobjects.GroupAccessDeviceGetListRequest import GroupAccessDeviceGetListRequest
import xml.etree.ElementTree as ET
import logging

class Device(BroadsoftObject):
    def __init__(self, name=None, type=None, description=None, mac_address=None, protocol=None,
                 transport_protocol=None, line_port=None, is_primary=None, did=None, index=1, **kwargs):
        self.description = description
        self.did = did
        self.index = index              # defaults to 1; the number of appearances for a given DID on a given device,
                                        # which can be more than 1
        self.is_primary = is_primary
        self.name = name
        self.type = type

        # optional
        self.line_port = line_port
        self.mac_address = mac_address
        self.protocol = protocol
        self.transport_protocol = transport_protocol

        BroadsoftObject.__init__(self, **kwargs)
        self.derive_line_port()

    def __repr__(self):
        return "<Broadsoft Device name:%s, type:%s, line_port:%s>" % (self.name, self.type, self.line_port)

    # expects <AccessDeviceEndpoint> coming from User xml
    def bootstrap_access_device_endpoint(self, ade):
        self.name = ade.findall('./accessDevice/deviceName')[0].text
        self.line_port = ade.findall('./linePort')[0].text
        self.is_primary = True

    # running a GroupAccessDeviceGetListRequest.find_device_by_mac_and_did() returns
    def bootstrap_find_result(self, result):
        self.mac_address = result['MAC Address']
        self.type = result['Device Type']
        self.name = result['Device Name']

    # expects to get a result row, from running a UserSharedCallAppearanceGetRequest, which was run through
    # BroadsoftRequest.convert_results_table
    def bootstrap_shared_call_appearance(self, sca):
        self.mac_address = sca['Mac Address']
        self.type = sca['Device Type']
        self.line_port = sca['Line/Port']
        self.name = sca['Device Name']
        self.is_primary = False

    def build_provision_request(self):
        g = GroupAccessDeviceAddRequest()
        self.inject_broadsoftinstance(child=g)
        g.description = self.description
        g.device_name = self.name
        g.device_type = self.type
        g.mac_address = self.mac_address
        if self.protocol:
            g.protocol = self.protocol
        if self.transport_protocol:
            g.transport_protocol = self.transport_protocol
        g.prep_attributes()
        return g

    def delete(self, bundle=False):
        if self.name is None:
            raise ValueError("can't run Device.delete() without a value for name")

        # "bundle" is for when we're packing the delete request into a set of requests to take advantage of atomicity
        if bundle:
            g = GroupAccessDeviceDeleteRequest(device_name=self.name, broadsoftinstance=self.broadsoftinstance)
            return g

        else:
            return GroupAccessDeviceDeleteRequest.delete_device(device_name=self.name,
                                                                broadsoftinstance=self.broadsoftinstance)

    def derive_line_port(self):
        if self.did and self.index and self.mac_address and self.broadsoftinstance.default_domain:
            from nettools.MACtools import MAC

            did = BroadsoftRequest.convert_phone_number(number=self.did)
            m = MAC(mac=self.mac_address)
            mac = m.bare_mac

            self.line_port = str(did) + '_' + str(mac) + '_' + str(self.index) + '@' + self.broadsoftinstance.default_domain

    def fetch(self, target_name=None):
        if not target_name:
            target_name = self.name
        self.xml = GroupAccessDeviceGetRequest.get_device(name=target_name, broadsoftinstance=self.broadsoftinstance)
        self.from_xml()

    def from_xml(self):
        BroadsoftObject.from_xml(self)

        self.type = self.xml.findall('./command/deviceType')[0].text
        descs = self.xml.findall('./command/description')
        if len(descs) > 0:
            self.description = descs[0].text

    def overwrite(self):
        desc = "(name: " + str(self.name) + ", mac: " + str(self.mac_address) + ", did: " + str(self.mac_address) + ")"
        logging.info("overwriting pre-existing devices " + desc, extra={'session_id': self.broadsoftinstance.session_id})

        if self.name is None:
            result = GroupAccessDeviceGetListRequest.find_device_by_mac_and_did(mac_address=self.mac_address, did=self.did,
                                                                           broadsoftinstance=self.broadsoftinstance)
            if result is not None:
                self.bootstrap_find_result(result=result)
                logging.info("overwriting pre-existing devices, lookup returned name " + str(self.name),
                             extra={'session_id': self.broadsoftinstance.session_id})

        if self.name is not None:
            logging.info("overwriting pre-existing devices, running delete on " + str(self.name),
                         extra={'session_id': self.broadsoftinstance.session_id})
            self.delete()
        else:
            logging.info("overwriting pre-existing devices, no matches found for " + desc,
                         extra={'session_id': self.broadsoftinstance.session_id})

    def set_password(self, did=None, sip_user_name=None, sip_password=None):
        if not did and not sip_user_name:
            raise ValueError("can't call Device.set_password without a value for did or sip_user_name")

        if not sip_password:
            raise ValueError("can't call Device.set_password without a value for password")

        if not self.name:
            raise ValueError("can't call Device.set_password without a value for device name")

        if not sip_user_name and did:
            sip_user_name = self.derive_sip_user_id(did=did)

        g = GroupAccessDeviceModifyRequest(device_name=self.name, sip_user_name=sip_user_name,
                                           sip_password=sip_password)
        self.inject_broadsoftinstance(child=g)
        g.post()