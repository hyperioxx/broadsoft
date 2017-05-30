import xml.etree.ElementTree as ET

from broadsoft.requestobjects.lib.BroadsoftRequest import BroadsoftRequest
from broadsoft.requestobjects.lib.SearchRequest import SearchRequest


class GroupGetListInServiceProviderRequest(SearchRequest):
    command_name = 'GroupGetListInServiceProviderRequest'

    def __init__(self, **kwargs):
        SearchRequest.__init__(self, **kwargs)

    def build_command_xml(self):
        self.prep_for_xml()
        cmd = self.build_command_shell()

        sid = ET.SubElement(cmd, 'serviceProviderId')
        sid.text = self.service_provider

        rsl = ET.SubElement(cmd, 'responseSizeLimit')
        rsl.text = str(self.response_size_limit)

        return cmd

    @staticmethod
    def list_groups(**kwargs):
        g = GroupGetListInServiceProviderRequest(**kwargs)
        xml = g.post()
        return xml
