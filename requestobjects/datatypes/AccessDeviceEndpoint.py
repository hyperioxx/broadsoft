import xml.etree.ElementTree as ET
from broadsoft.requestobjects.datatypes.AccessDevice import AccessDevice


class AccessDeviceEndpoint:
    def __init__(self, device_name=None, line_port=None, contact=None, device_level='Group'):
        self.contact = contact
        self.device_level = device_level
        self.device_name = device_name
        self.line_port = line_port

    def to_xml(self):
        ade = ET.Element('accessDeviceEndpoint')

        if self.device_name:
            ad = AccessDevice(device_name=self.device_name, device_level=self.device_level)
            ade.append(ad.to_xml())

        if self.line_port:
            lp = ET.SubElement(ade, 'linePort')
            lp.text = self.line_port

        if self.contact:
            c = ET.SubElement(ade, 'contact')
            c.text = self.contact

        return ade