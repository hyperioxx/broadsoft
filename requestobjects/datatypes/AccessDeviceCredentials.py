import xml.etree.ElementTree as ET
from broadsoft.requestobjects.datatypes.AccessDevice import AccessDevice


class AccessDeviceCredentials:
    def __init__(self, user_name=None, password=None):
        self.user_name = user_name
        self.password = password

    def to_xml(self):
        adc = ET.Element('accessDeviceCredentials')

        e = ET.SubElement(adc, 'userName')
        e.text = self.user_name

        e = ET.SubElement(adc, 'password')
        e.text = self.password

        return adc
