import xml.etree.ElementTree as ET
from broadsoft.requestobjects.datatypes.AccessDevice import AccessDevice


class AccessDeviceCredentials:
    def __init__(self, sip_user_name=None, sip_password=None):
        self.sip_user_name = sip_user_name
        self.sip_password = sip_password

    def to_xml(self):
        adc = ET.Element('accessDeviceCredentials')

        e = ET.SubElement(adc, 'userName')
        e.text = self.sip_user_name

        e = ET.SubElement(adc, 'password')
        e.text = self.sip_password

        return adc
