import xml.etree.ElementTree as ET
from broadsoft.requestobjects.datatypes.AccessDevice import AccessDevice


class Endpoint:
    # we only bother building this if certain key elements are present
    quorum = ['device_name', 'line_port']

    def __init__(self, device_name=None, line_port=None, contact=None, device_level='Group'):
        self.contact = contact
        self.device_level = device_level
        self.device_name = device_name
        self.line_port = line_port

    def is_quorum(self):
        # if any of the properties in self.quorum are not None, quorum is met
        for p in self.quorum:
            if getattr(self, p) is not None:
                return True

        return False

    def to_xml(self):
        if not self.is_quorum():
            return None

        ep = ET.Element('endpoint')
        ade = ET.SubElement(ep, 'accessDeviceEndpoint')

        if self.device_name:
            ad = AccessDevice(device_name=self.device_name, device_level=self.device_level)
            ade.append(ad.to_xml())

        if self.line_port:
            lp = ET.SubElement(ade, 'linePort')
            lp.text = self.line_port

        c = ET.SubElement(ade, 'contact')
        c.set('xsi:nil', 'true')

        return ep