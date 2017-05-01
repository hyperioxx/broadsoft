import xml.etree.ElementTree as ET
from broadsoft.requestobjects.XmlRequest import XmlRequest


class AuthenticationRequest(XmlRequest):
    command_name = 'AuthenticationRequest'

    def __init__(self):
        self.user_id = 'admMITapi'
        XmlRequest.__init__(self)

    def to_xml(self):
        # master is the entire XML document, cmd is the command element inserted within, which this object will be
        # manipulating
        (master, cmd) = XmlRequest.master_to_xml(self)

        uid = ET.SubElement(cmd, 'userId')
        uid.text = self.user_id

        return master
