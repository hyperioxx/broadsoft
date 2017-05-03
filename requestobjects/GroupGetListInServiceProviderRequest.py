import xml.etree.ElementTree as ET

from broadsoft.requestobjects.lib.BroadsoftRequest import BroadsoftRequest
from broadsoft.requestobjects.lib.SearchRequest import SearchRequest


class GroupGetListInServiceProviderRequest(SearchRequest):
    command_name = 'GroupGetListInServiceProviderRequest'

    def __init__(self, **kwargs):
        SearchRequest.__init__(self, **kwargs)

    def to_xml(self):
        # master is the entire XML document, cmd is the command element inserted within, which this object will be
        # manipulating
        (master, cmd) = BroadsoftRequest.master_to_xml(self)

        sid = ET.SubElement(cmd, 'serviceProviderId')
        sid.text = self.service_provider

        rsl = ET.SubElement(cmd, 'responseSizeLimit')
        rsl.text = str(self.response_size_limit)

        return master

    @staticmethod
    def list_groups(**kwargs):
        g = GroupGetListInServiceProviderRequest(**kwargs)
        xml = g.post()

        # convert GroupTable to dict
        if type(xml) is str:
            xml = ET.fromstring(xml)
        group_table = xml.findall('./command/groupTable')[0]
        return BroadsoftRequest.convert_results_table(xml=group_table)
