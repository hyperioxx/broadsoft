import unittest.mock
import xml.etree.ElementTree as ET
from broadsoft.requestobjects.UserSharedCallAppearanceAddEndpointRequest import UserSharedCallAppearanceAddEndpointRequest
from broadsoft.requestobjects.lib.BroadsoftRequest import BroadsoftRequest


class TestBroadsoftUserSharedCallAddEndpointRequest(unittest.TestCase):
    def test_sip_user_id_derived_in_init(self):
        u = UserSharedCallAppearanceAddEndpointRequest(did=6175551212)
        self.assertEqual('6175551212@' + u.default_domain, u.sip_user_id)

        u = UserSharedCallAppearanceAddEndpointRequest(did=6175551212, sip_user_id='beaver@mit.edu')
        self.assertEqual('beaver@mit.edu', u.sip_user_id)

    def test_sip_line_port_derived_in_init(self):
        u = UserSharedCallAppearanceAddEndpointRequest(did=6175551212)
        self.assertEqual('6175551212_lp@' + u.default_domain, u.line_port)

        u = UserSharedCallAppearanceAddEndpointRequest(did=6175551212, line_port='beaver@mit.edu')
        self.assertEqual('beaver@mit.edu', u.line_port)

    def test_sip_user_id_derived_in_to_xml(self):
        u = UserSharedCallAppearanceAddEndpointRequest()
        u.did = 6175551212
        u.build_command_xml()
        self.assertEqual('6175551212@' + u.default_domain, u.sip_user_id)

        u = UserSharedCallAppearanceAddEndpointRequest()
        u.did = 6175551212
        u.sip_user_id = 'beaver@mit.edu'
        u.build_command_xml()
        self.assertEqual('beaver@mit.edu', u.sip_user_id)

    def test_sip_line_port_derived_in_to_xml(self):
        u = UserSharedCallAppearanceAddEndpointRequest()
        u.did = 6175551212
        u.build_command_xml()
        self.assertEqual('6175551212_lp@' + u.default_domain, u.line_port)

        u = UserSharedCallAppearanceAddEndpointRequest()
        u.did = 6175551212
        u.line_port = 'beaver@mit.edu'
        u.build_command_xml()
        self.assertEqual('beaver@mit.edu', u.line_port)

    def test_validate(self):
        u = UserSharedCallAppearanceAddEndpointRequest()
        with self.assertRaises(ValueError):
            u.validate()

    def test_build_command_xml(self):
        u = UserSharedCallAppearanceAddEndpointRequest(did=6175551212, device_name='beaverphone',
                                                       line_port='6175551212_beaverphone@broadsoft.mit.edu')

        self.maxDiff = None
        xml = u.to_xml()
        cmd = xml.findall('command')[0]
        self.assertEqual(
            '<command xmlns="" xsi:type="UserSharedCallAppearanceAddEndpointRequest14sp2">' +
            '<userId>6175551212@' + u.default_domain + '</userId>' +
            '<accessDeviceEndpoint>' +
                '<accessDevice>' +
                    '<deviceLevel>Group</deviceLevel>' +
                    '<deviceName>beaverphone</deviceName>' +
                '</accessDevice>' +
                '<linePort>6175551212_beaverphone@broadsoft.mit.edu</linePort>' +
            '</accessDeviceEndpoint>' +
            '<isActive>true</isActive>' +
            '<allowOrigination>true</allowOrigination>' +
            '<allowTermination>true</allowTermination>' +
            '</command>',
            ET.tostring(cmd).decode('utf-8')
        )
