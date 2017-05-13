import xml.etree.ElementTree as ET
from broadsoft.requestobjects.lib.BroadsoftRequest import BroadsoftRequest


class UserSharedCallAppearanceModifyRequest(BroadsoftRequest):
    command_name = 'UserSharedCallAppearanceModifyRequest'
    check_success = True

    booleans = [
        'alert_all_appearances_for_click_to_dial_calls',
        'alert_all_appearances_for_group_paging_calls',
        'allow_sca_call_retrieve',
        'multiple_call_arrangement_is_active',
        'allow_bridging_between_locations',
        'enable_call_park_notification'
    ]

    def __init__(self, sip_user_id=None, alert_all_appearances_for_click_to_dial_calls=True,
                 alert_all_appearances_for_group_paging_calls=False, allow_sca_call_retrieve=True,
                 multiple_call_arrangement_is_active=True, allow_bridging_between_locations=False,
                 bridge_warning_tone='None', enable_call_park_notification=False, did=None,
                 **kwargs):
        self.did=did
        self.sip_user_id = sip_user_id
        self.alert_all_appearances_for_click_to_dial_calls = alert_all_appearances_for_click_to_dial_calls
        self.alert_all_appearances_for_group_paging_calls = alert_all_appearances_for_group_paging_calls
        self.allow_sca_call_retrieve = allow_sca_call_retrieve
        self.multiple_call_arrangement_is_active = multiple_call_arrangement_is_active
        self.allow_bridging_between_locations = allow_bridging_between_locations
        self.bridge_warning_tone = bridge_warning_tone
        self.enable_call_park_notification = enable_call_park_notification
        BroadsoftRequest.__init__(self, **kwargs)
        if self.did and self.sip_user_id is None:
            self.sip_user_id = self.derive_sip_user_id()

    def build_command_xml(self):
        if self.did and not self.sip_user_id:
            self.sip_user_id = self.derive_sip_user_id()
        self.validate()

        cmd = self.build_command_shell()

        uid = ET.SubElement(cmd, 'userId')
        uid.text = self.sip_user_id

        s = ET.SubElement(cmd, 'alertAllAppearancesForClickToDialCalls')
        s.text = self.alert_all_appearances_for_click_to_dial_calls

        s = ET.SubElement(cmd, 'alertAllAppearancesForGroupPagingCalls')
        s.text = self.alert_all_appearances_for_group_paging_calls

        s = ET.SubElement(cmd, 'allowSCACallRetrieve')
        s.text = self.allow_sca_call_retrieve

        s = ET.SubElement(cmd, 'multipleCallArrangementIsActive')
        s.text = self.multiple_call_arrangement_is_active

        s = ET.SubElement(cmd, 'allowBridgingBetweenLocations')
        s.text = self.allow_bridging_between_locations

        s = ET.SubElement(cmd, 'bridgeWarningTone')
        s.text = self.bridge_warning_tone

        s = ET.SubElement(cmd, 'enableCallParkNotification')
        s.text = self.enable_call_park_notification

        return cmd

    def validate(self):
        if self.sip_user_id is None:
            raise ValueError("can't run broadsoft.UserSharedCallAppearanceModifyRequest.to_xml() without a value for sip_user_id.")

