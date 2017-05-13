import xml.etree.ElementTree as ET
from broadsoft.requestobjects.lib.BroadsoftRequest import BroadsoftRequest


class UserSharedCallAppearanceAddEndpointRequest(BroadsoftRequest):
    command_name = 'UserSharedCallAppearanceAddEndpointRequest14sp2'
    check_success = True

    def __init__(self, **kwargs):
        BroadsoftRequest.__init__(self, **kwargs)

    def build_command_xml(self):
        self.validate()

        cmd = self.build_command_shell()

        """
        <command xsi:type="UserSharedCallAppearanceAddEndpointRequest14sp2" xmlns="" echo="UserSharedCallAppearanceAddEndpointRequest14sp2 add – add SCA for BTBC Mobile">
        <userId>mituser1@broadsoft.com</userId>
        <accessDeviceEndpoint>
        <accessDevice>
        <deviceLevel>Group</deviceLevel>
        <deviceName>mituser1_btbc_mob</deviceName>
        </accessDevice>
        <linePort>mituser1_btbc_mob_sca@broadsoft.com</linePort>
        </accessDeviceEndpoint>
        <isActive>true</isActive>
        <allowOrigination>true</allowOrigination>
        <allowTermination>true</allowTermination>
        </command>
        """

        return cmd

    def validate(self):
        if self.sip_user_id is None:
            raise ValueError("can't run broadsoft.UserSharedCallAppearanceModifyRequest.to_xml() without a value for sip_user_id.")

