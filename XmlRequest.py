class XmlRequest:
    def __init__(self):
        self.action = 'add'
        self.command_name = None
        self.default_domain = 'broadworks'
        self.encoding = "ISO-8859-1"
        self.session_id = None
        self.version = 1.0

    """
    <?xml version="1.0" encoding="ISO-8859-1"?>
    <BroadsoftDocument protocol="OCI" xmlns="C" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <sessionIdxmlns="">BB1A413DF12D404128F8956459FBD4D9</sessionId>
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