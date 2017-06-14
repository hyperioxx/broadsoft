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

    def test_build_command_xml(self):
        u = UserSharedCallAppearanceModifyRequest(sip_user_id='6175551212@broadsoft-dev.mit.edu',
                                                  alert_all_appearances_for_click_to_dial_calls=False,
                                                  alert_all_appearances_for_group_paging_calls=True,
                                                  allow_sca_call_retrieve=False,
                                                  multiple_call_arrangement_is_active=False,
                                                  allow_bridging_between_locations=True,
                                                  bridge_warning_tone='Awooga',
                                                  enable_call_park_notification=True)
        target_xml = \
            '<command xmlns="" xsi:type="UserSharedCallAppearanceModifyRequest">' + \
            '<userId>6175551212@broadsoft-dev.mit.edu</userId>' + \
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
