import unittest.mock
import xml.etree.ElementTree as ET

import broadsoft.requestobjects.lib.BroadsoftRequest
from broadsoft.requestobjects.GroupAccessDeviceGetListRequest import GroupAccessDeviceGetListRequest


class TestBroadsoftGroupAccessDeviceGetListRequest(unittest.TestCase):
    def test_to_xml_with_all_attrs(self):
        b = broadsoft.requestobjects.lib.BroadsoftRequest.BroadsoftInstance()
        g = GroupAccessDeviceGetListRequest(broadsoftinstance=b)
        g.device_name = 'dn'
        g.mac_address = 'ma'
        g.net_address = 'na'
        g.device_type = 'dt'
        g.device_version = 'dv'

        x = g.to_xml()
        self.maxDiff = None
        self.assertEqual(
            """<BroadsoftDocument protocol="OCI" xmlns="C" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><sessionId xmlns="">""" + b.session_id + """</sessionId><command xmlns="" xsi:type="GroupAccessDeviceGetListRequest"><serviceProviderId>ENT136</serviceProviderId><groupId>MIT-GP</groupId><responseSizeLimit>100000</responseSizeLimit><searchCriteriaDeviceName><mode>Equal To</mode><value>dn</value><isCaseInsensitive>true</isCaseInsensitive></searchCriteriaDeviceName><searchCriteriaDeviceMACAddress><mode>Equal To</mode><value>ma</value><isCaseInsensitive>true</isCaseInsensitive></searchCriteriaDeviceMACAddress><searchCriteriaDeviceNetAddress><mode>Equal To</mode><value>na</value><isCaseInsensitive>true</isCaseInsensitive></searchCriteriaDeviceNetAddress><searchCriteriaExactDeviceType><mode>Equal To</mode><value>Generic SIP Phone</value><isCaseInsensitive>true</isCaseInsensitive></searchCriteriaExactDeviceType><searchCriteriaAccessDeviceVersion><mode>Equal To</mode><value>dv</value><isCaseInsensitive>true</isCaseInsensitive></searchCriteriaAccessDeviceVersion></command></BroadsoftDocument>""",
            ET.tostring(x).decode('utf-8')
        )

    def test_to_xml_with_some_attrs(self):
        b = broadsoft.requestobjects.lib.BroadsoftRequest.BroadsoftInstance()
        g = GroupAccessDeviceGetListRequest(broadsoftinstance=b)
        g.mac_address = 'ma'
        g.net_address = 'na'

        x = g.to_xml()
        self.maxDiff = None
        self.assertEqual(
            """<BroadsoftDocument protocol="OCI" xmlns="C" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><sessionId xmlns="">""" + b.session_id + """</sessionId><command xmlns="" xsi:type="GroupAccessDeviceGetListRequest"><serviceProviderId>ENT136</serviceProviderId><groupId>MIT-GP</groupId><responseSizeLimit>100000</responseSizeLimit><searchCriteriaDeviceMACAddress><mode>Equal To</mode><value>ma</value><isCaseInsensitive>true</isCaseInsensitive></searchCriteriaDeviceMACAddress><searchCriteriaDeviceNetAddress><mode>Equal To</mode><value>na</value><isCaseInsensitive>true</isCaseInsensitive></searchCriteriaDeviceNetAddress></command></BroadsoftDocument>""",
            ET.tostring(x).decode('utf-8')
        )

    def test_find_devices_static(self):
        self.assertFalse("write this")

    def test_fetch_devices_static(self):
        self.assertFalse("write this")