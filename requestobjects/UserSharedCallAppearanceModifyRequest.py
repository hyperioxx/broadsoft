import xml.etree.ElementTree as ET
from broadsoft.requestobjects.lib.BroadsoftRequest import BroadsoftRequest


class UserSharedCallAppearanceModifyRequest(BroadsoftRequest):
    command_name = 'UserSharedCallAppearanceModifyRequest'
    check_success = True

    def __init__(self, **kwargs):
        """
        <userId>mituser1@broadsoft-dev.mit.edu</userId>
        <alertAllAppearancesForClickToDialCalls>true</alertAllAppearancesForClickToDialCalls>
        <alertAllAppearancesForGroupPagingCalls>false</alertAllAppearancesForGroupPagingCalls>
        <allowSCACallRetrieve>true</allowSCACallRetrieve>
        <multipleCallArrangementIsActive>true</multipleCallArrangementIsActive>
        <allowBridgingBetweenLocations>false</allowBridgingBetweenLocations>
        <bridgeWarningTone>None</bridgeWarningTone>
        <enableCallParkNotification>false</enableCallParkNotification>
        </command>
        """
        BroadsoftRequest.__init__(self, **kwargs)
