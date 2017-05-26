import xml.etree.ElementTree as ET
from broadsoft.requestobjects.lib.BroadsoftRequest import BroadsoftRequest
from broadsoft.requestobjects.datatypes.AccessDevice import AccessDevice


class UserSharedCallAppearanceAddEndpointRequest(BroadsoftRequest):
    command_name = 'UserSharedCallAppearanceAddEndpointRequest14sp2'
    check_success = True
    booleans = [
        'is_active',
        'allow_origination',
        'allow_termination'
    ]

    def __init__(self, did=None, sip_user_id=None, device_name=None, line_port=None, **kwargs):
        self.device_name = device_name
        self.did = did
        self.line_port = line_port
        self.sip_user_id = sip_user_id

        # don't expect to ever overwrite these, so not in init
        self.is_active = True
        self.allow_origination = True
        self.allow_termination = True

        BroadsoftRequest.__init__(self, **kwargs)

    def build_command_xml(self):
        self.prep_for_xml()
        self.validate()

        cmd = self.build_command_shell()

        e = ET.SubElement(cmd, 'userId')
        e.text = self.sip_user_id

        ade = ET.SubElement(cmd, 'accessDeviceEndpoint')
        ad = AccessDevice(device_name=self.device_name)
        ad_xml = ad.to_xml()
        ade.append(ad_xml)

        e = ET.SubElement(ade, 'linePort')
        e.text = self.line_port

        e = ET.SubElement(cmd, 'isActive')
        e.text = self.is_active

        e = ET.SubElement(cmd, 'allowOrigination')
        e.text = self.allow_origination

        e = ET.SubElement(cmd, 'allowTermination')
        e.text = self.allow_termination

        return cmd

    def validate(self):
        if self.sip_user_id is None:
            raise ValueError("can't run broadsoft.UserSharedCallAppearanceModifyRequest.to_xml() without a value for sip_user_id.")

