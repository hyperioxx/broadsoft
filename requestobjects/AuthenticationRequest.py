import xml.etree.ElementTree as ET
from broadsoft.requestobjects.BroadsoftRequest import BroadsoftRequest


class AuthenticationRequest(BroadsoftRequest):
    command_name = 'AuthenticationRequest'

    def __init__(self):
        self.user_id = 'admMITapi'
        BroadsoftRequest.__init__(self)

    def to_xml(self):
        # master is the entire XML document, cmd is the command element inserted within, which this object will be
        # manipulating
        (master, cmd) = BroadsoftRequest.master_to_xml(self)

        uid = ET.SubElement(cmd, 'userId')
        uid.text = self.user_id

        return master
