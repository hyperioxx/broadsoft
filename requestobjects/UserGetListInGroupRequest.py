import xml.etree.ElementTree as ET

from broadsoft.requestobjects.lib.BroadsoftRequest import BroadsoftRequest
from broadsoft.requestobjects.lib.SearchRequest import SearchRequest


class UserGetListInGroupRequest(SearchRequest):
    command_name = 'UserGetListInGroupRequest'

    def __init__(self, group_id=None, **kwargs):
        self.group_id = group_id
        SearchRequest.__init__(self, **kwargs)

    def build_command_xml(self):
        self.prep_for_xml()
        cmd = self.build_command_shell()

        sid = ET.SubElement(cmd, 'serviceProviderId')
        sid.text = self.broadsoftinstance.service_provider

        gid = ET.SubElement(cmd, 'GroupId')
        gid.text = self.group_id

        rsl = ET.SubElement(cmd, 'responseSizeLimit')
        rsl.text = str(self.response_size_limit)

        return cmd

    @staticmethod
    def list_users(**kwargs):
        g = UserGetListInGroupRequest(**kwargs)
        xml = g.post()
        return BroadsoftRequest.convert_results_table(xml = xml)
