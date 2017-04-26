import xml.etree.ElementTree as ET


class XmlRequest:
    def __init__(self):
        self.command_data = None
        self.command_name = None
        self.default_domain = 'broadworks'
        self.encoding = "ISO-8859-1"
        self.protocol = 'OCI'
        self.session_id = None
        self.version = 1.0
        self.xmlns = 'C'
        self.xmlns_xsi = 'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"'

    def to_xml(self):
        self.validate()

        bd = ET.Element('BroadsoftDocument')
        bd.set('protocol', self.protocol)
        bd.set('xmlns', self.xmlns)
        bd.set('xmlns:xsi', self.xmlns_xsi)

        sid = ET.SubElement(bd, 'sessionId')
        sid.set('xmlns', '')
        sid.text = str(self.session_id)

        cmd = ET.SubElement(bd, 'command')
        cmd.set('xsi:type', self.command_name)
        cmd.set('xmlns', '')

        return bd

    def validate(self):
        if self.command_name is None:
            raise ValueError("can't run broadsoft.XmlRequest.to_xml() without a value for command_name")

    """
    <?xml version="1.0" encoding="ISO-8859-1"?>
    <BroadsoftDocument protocol="OCI" xmlns="C" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
        <sessionId xmlns="">BB1A413DF12D404128F8956459FBD4D9</sessionId>
        <command xsi:type="GroupAddRequest" xmlns="">
            <serviceProviderId>sp1</serviceProviderId>
            <groupId>group2</groupId>
            <defaultDomain>broadworks</defaultDomain>
            <userLimit>25</userLimit>
            <groupName>Group 2</groupName>
            <callingLineIdName>Group 2 Line ID</callingLineIdName>
            <timeZone>America/New_York</timeZone>
            <contact>
                <contactName>Joe Smith</contactName>
                <contactNumber>301-555-1212</contactNumber>
                <contactEmail>joe.smith@broadworks.net</contactEmail>
            </contact>
        </command>
    </BroadsoftDocument>
    """