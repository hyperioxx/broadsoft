import unittest.mock
import xml.etree.ElementTree as ET
from broadsoft.requestobjects.UserSharedCallAppearanceModifyRequest import UserSharedCallAppearanceModifyRequest
from broadsoft.requestobjects.lib.BroadsoftRequest import BroadsoftRequest


class TestBroadsoftUserSharedCallAppearanceModifyRequest(unittest.TestCase):
    def test_validate(self):
        u = UserSharedCallAppearanceModifyRequest()
        with self.assertRaises(ValueError):
            u.validate()

    @unittest.mock.patch.object(UserSharedCallAppearanceModifyRequest, 'validate')
    def test_build_command_xml_calls_validate(
            self,
            validate_patch
    ):
        u = UserSharedCallAppearanceModifyRequest(sip_user_id='6175551212@broadsoft-dev.mit.edu')
        u.build_command_xml()
        self.assertTrue(validate_patch.called)

    def test_sip_userid_derived_from_did(self):
        u = UserSharedCallAppearanceModifyRequest(did='617-555-1212')
        self.assertEqual('6175551212@' + u.default_domain, u.sip_user_id)

        u = UserSharedCallAppearanceModifyRequest(sip_user_id='beaver@mit.edu', did='617-555-1212')
        self.assertEqual('beaver@mit.edu', u.sip_user_id)

    @unittest.mock.patch.object(BroadsoftRequest, 'derive_sip_user_id')
    def test_build_command_xml_derives_userid(
            self,
            derive_sip_user_id_patch
    ):
        u = UserSharedCallAppearanceModifyRequest()
        self.assertFalse(derive_sip_user_id_patch.called)
        u.did = '617-555-1212'
        u.build_command_xml()
        self.assertTrue(derive_sip_user_id_patch.called)

        derive_sip_user_id_patch.called = False
        u = UserSharedCallAppearanceModifyRequest()
        self.assertFalse(derive_sip_user_id_patch.called)
        u.did = '617-555-1212'
        u.sip_user_id = 'beaver@mit.edu'
        u.build_command_xml()
        self.assertFalse(derive_sip_user_id_patch.called)

    def test_build_command_xml(self):
        u = UserSharedCallAppearanceModifyRequest(did=6175551212,
                                                  alert_all_appearances_for_click_to_dial_calls=False,
                                                  alert_all_appearances_for_group_paging_calls=True,
                                                  allow_sca_call_retrieve=False,
                                                  multiple_call_arrangement_is_active=False,
                                                  allow_bridging_between_locations=True,
                                                  bridge_warning_tone='Awooga',
                                                  enable_call_park_notification=True)
        target_xml = \
            '<command xmlns="" xsi:type="UserSharedCallAppearanceModifyRequest">' + \
            '<userId>6175551212@' + u.default_domain + '</userId>' + \
            '<alertAllAppearancesForClickToDialCalls>false</alertAllAppearancesForClickToDialCalls>' + \
            '<alertAllAppearancesForGroupPagingCalls>true</alertAllAppearancesForGroupPagingCalls>' + \
            '<allowSCACallRetrieve>false</allowSCACallRetrieve>' + \
            '<multipleCallArrangementIsActive>false</multipleCallArrangementIsActive>' + \
            '<allowBridgingBetweenLocations>true</allowBridgingBetweenLocations>' + \
            '<bridgeWarningTone>Awooga</bridgeWarningTone>' + \
            '<enableCallParkNotification>true</enableCallParkNotification>' + \
            '</command>'

        xml = u.to_xml()
        cmd = xml.findall('./command')[0]
        self.assertEqual(
            target_xml,
            ET.tostring(cmd).decode('utf-8')
        )
