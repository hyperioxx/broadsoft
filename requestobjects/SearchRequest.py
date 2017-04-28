import xml.etree.ElementTree as ET
from broadsoft.requestobjects.XmlRequest import XmlRequest

"""
abstract class that should actually be instantiated as in GroupGetListInServiceProviderRequest
"""


class SearchRequest(XmlRequest):
    valid_modes = [
        'Starts With',
        'Contains',
        'Equal To'
    ]

    def __init__(self, mode='Starts With', value=None, case_sensitive=False):
        self.case_sensitive = case_sensitive
        self.mode = mode
        self.value = value
        XmlRequest.__init__(self)

    def build_search_criteria(self, search_criteria_element):
        self.build_search_criteria__validate()

        m = ET.SubElement(search_criteria_element, 'mode')
        m.text = self.mode

        v = ET.SubElement(search_criteria_element, 'value')
        v.text = str(self.value)

        c = ET.SubElement(search_criteria_element, 'isCaseInsensitive')
        if self.case_sensitive:
            c.text = 'true'
        else:
            c.text = 'false'

    def build_search_criteria__validate(self):
        if self.mode not in self.valid_modes:
            raise ValueError("The mode " + str(self.mode) + " is not valid for broadsoft.requestobjects.SearchRequest. Please choose from " + ', '.join(self.valid_modes) + '.')
