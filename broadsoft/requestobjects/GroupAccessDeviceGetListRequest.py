import xml.etree.ElementTree as ET
from broadsoft.requestobjects.lib.BroadsoftRequest import BroadsoftRequest
from broadsoft.requestobjects.lib.SearchRequest import SearchRequest


class GroupAccessDeviceGetListRequest(SearchRequest):
    command_name = 'GroupAccessDeviceGetListRequest'

    def __init__(self, device_name=None, mac_address=None, net_address=None, device_type=None, device_version=None,
                 **kwargs):
        self.device_name = device_name
        self.device_type = device_type
        self.device_version = device_version
        self.mac_address = mac_address
        self.net_address = net_address

        SearchRequest.__init__(self, **kwargs)

    def build_command_xml(self):
        self.prep_for_xml()
        cmd = self.build_command_shell()

        sid = ET.SubElement(cmd, 'serviceProviderId')
        sid.text = self.broadsoftinstance.service_provider

        gid = ET.SubElement(cmd, 'groupId')
        gid.text = self.group_id

        rsl = ET.SubElement(cmd, 'responseSizeLimit')
        rsl.text = str(self.response_size_limit)

        if self.device_name:
            sc = SearchRequest.SearchCriteria(value=self.device_name, mode='Equal To', case_insensitive=True)
            s = ET.SubElement(cmd, 'searchCriteriaDeviceName')
            sc.embed(parent=s)

        if self.mac_address:
            sc = SearchRequest.SearchCriteria(value=self.mac_address, mode='Equal To', case_insensitive=True)
            s = ET.SubElement(cmd, 'searchCriteriaDeviceMACAddress')
            sc.embed(parent=s)

        if self.net_address:
            sc = SearchRequest.SearchCriteria(value=self.net_address, mode='Equal To', case_insensitive=True)
            s = ET.SubElement(cmd, 'searchCriteriaDeviceNetAddress')
            sc.embed(parent=s)

        if self.device_type:
            sc = SearchRequest.SearchCriteria(value=self.device_type, mode='Equal To', case_insensitive=True)
            s = ET.SubElement(cmd, 'searchCriteriaExactDeviceType')
            sc.embed(parent=s)

        if self.device_version:
            sc = SearchRequest.SearchCriteria(value=self.device_version, mode='Equal To', case_insensitive=True)
            s = ET.SubElement(cmd, 'searchCriteriaAccessDeviceVersion')
            sc.embed(parent=s)

        return cmd

    @staticmethod
    def find_device_by_mac(mac_address, return_raw=False, **kwargs):
        g = GroupAccessDeviceGetListRequest(mac_address=mac_address, **kwargs)
        xml = g.post()

        if return_raw:
            return xml

        # convert results to dict
        if type(xml) is str:
            xml = ET.fromstring(xml)
        table = xml.findall('./command/accessDeviceTable')[0]
        return BroadsoftRequest.convert_results_table(xml=table)

    @staticmethod
    def find_device_by_mac_and_did(mac_address, did, **kwargs):
        from broadsoft.requestobjects.GroupAccessDeviceGetRequest import GroupAccessDeviceGetRequest
        from broadsoft.requestobjects.UserGetRequest import UserGetRequest
        from broadsoft.requestobjects.lib.BroadsoftRequest import BroadsoftRequest

        devices = GroupAccessDeviceGetListRequest.find_device_by_mac(mac_address=mac_address, **kwargs)
        for d in devices:
            # first, fetch the device based on the name.
            fetched_device_xml = GroupAccessDeviceGetRequest.get_device(name=d['Device Name'], **kwargs)

            # this will give us a user. fetch that user.
            sip_user_id = fetched_device_xml.findall('.//userName')[0].text
            user = UserGetRequest.get_user(sip_user_id=sip_user_id, **kwargs)

            # does the user match the passed DID? If so, the MAC/DID pair is assigned.
            results = user.findall('./command/phoneNumber')
            if len(results) > 1:
                raise RuntimeError("UserGetRequest.get_user() returned too many results")
            user_did = user.findall('./command/phoneNumber')[0].text
            user_did = BroadsoftRequest.convert_phone_number(number=user_did)
            did = BroadsoftRequest.convert_phone_number(number=did)

            if did == user_did:
                return fetched_device_xml

        return None

    @staticmethod
    def list_devices(**kwargs):
        g = GroupAccessDeviceGetListRequest(**kwargs)
        xml = g.post()
        return xml
