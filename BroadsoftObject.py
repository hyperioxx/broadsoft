import xml.etree.ElementTree as ET

class BroadsoftObject:
    def __init__(self, xml=None, **kwargs):
        self.xml = xml
        self.prep_attributes()

    def from_xml(self):
        self.prep_attributes()

    def prep_attributes(self):
        if self.xml and type(self.xml) is str:
            self.xml = ET.fromstring(self.xml)

    def provision(self):
        ro = self.build_request_object()
        results = ro.post()
        return results