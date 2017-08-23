import xml.etree.ElementTree as ET


class AccessDevice:
    def __init__(self, device_name='Generic', device_level='Group'):
        self.device_level = device_level
        self.device_name = device_name

    def to_xml(self):
        ad = ET.Element('accessDevice')

        dl = ET.SubElement(ad, 'deviceLevel')
        dl.text = self.device_level

        dn = ET.SubElement(ad, 'deviceName')
        dn.text = self.device_name

        return ad

    def validate(self):
        if not self.device_name:
            raise ValueError("can't run AccessDeviceEndpoint.to_xml() without a value for device_name")

        if not self.device_level:
            raise ValueError("can't run AccessDeviceEndpoint.to_xml() without a value for device_level")
