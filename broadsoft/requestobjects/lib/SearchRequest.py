import xml.etree.ElementTree as ET

from broadsoft.requestobjects.lib.BroadsoftRequest import BroadsoftRequest

"""
abstract class that should actually be instantiated as in GroupGetListInSystemRequest
"""


class SearchRequest(BroadsoftRequest):
    def __init__(self, response_size_limit=100000, **kwargs):
        self.response_size_limit = response_size_limit
        BroadsoftRequest.__init__(self, **kwargs)

    class SearchCriteria:
        valid_modes = [
            'Starts With',
            'Contains',
            'Equal To'
        ]

        def __init__(self, mode='Starts With', value=None, case_insensitive=False):
            self.case_insensitive = case_insensitive
            self.mode = mode
            self.value = value

        def embed(self, parent):
            self.add__validate()

            m = ET.SubElement(parent, 'mode')
            m.text = self.mode

            v = ET.SubElement(parent, 'value')
            v.text = str(self.value)

            c = ET.SubElement(parent, 'isCaseInsensitive')
            if self.case_insensitive:
                c.text = 'true'
            else:
                c.text = 'false'

        def add__validate(self):
            if self.mode not in self.valid_modes:
                raise ValueError("The mode " + str(self.mode) + " is not valid for broadsoft.requestobjects.SearchRequest. Please choose from " + ', '.join(self.valid_modes) + '.')
