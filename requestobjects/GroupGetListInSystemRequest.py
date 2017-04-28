import xml.etree.ElementTree as ET
from broadsoft.requestobjects.SearchRequest import SearchRequest
from broadsoft.requestobjects.XmlRequest import XmlRequest


class GroupGetListInSystemRequest(SearchRequest):
    command_name = 'GroupGetListInSystemRequest'

    def __init__(self, group_id=None, group_name=None, service_provider=None):
        self.group_id = group_id
        self.group_id_mode = 'Equal To'
        self.group_id_case_insensitive = False
        self.group_name = group_name
        self.group_name_mode = 'Equal To'
        self.group_name_case_insensitive = False
        self.service_provider = service_provider
        self.service_provider_mode = 'Equal To'
        self.service_provider_case_insensitive = False
        SearchRequest.__init__(self)

    def to_xml(self):
        master = XmlRequest.master_to_xml(self)

        cmd = ET.SubElement(master, 'command')
        cmd.set('xsi:type', self.command_name)
        cmd.set('xmlns', '')

        rsl = ET.SubElement(cmd, 'responseSizeLimit')
        rsl.text = str(self.response_lize_limit)

        # add the search criteria that have been specified
        if self.group_id:
            sc = ET.SubElement(cmd, 'searchCriteriaGroupId')
            s = SearchRequest.SearchCriteria(
                mode=self.group_id_mode,
                value=self.group_id,
                case_insensitive=self.group_id_case_insensitive
            )
            s.add(parent=sc)
            
        if self.group_name:
            sc = ET.SubElement(cmd, 'searchCriteriaGroupName')
            s = SearchRequest.SearchCriteria(
                mode=self.group_name_mode,
                value=self.group_name,
                case_insensitive=self.group_name_case_insensitive
            )
            s.add(parent=sc)

        if self.service_provider:
            sc = ET.SubElement(cmd, 'searchCriteriaExactServiceProvider')
            s = SearchRequest.SearchCriteria(
                mode=self.service_provider_mode,
                value=self.service_provider,
                case_insensitive=self.service_provider_case_insensitive
            )
            s.add(parent=sc)

        return master