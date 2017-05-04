import xml.etree.ElementTree as ET
from broadsoft.requestobjects.lib.BroadsoftRequest import BroadsoftRequest


class UserAddRequest(BroadsoftRequest):
    command_name = 'UserAddRequest17sp4'
    check_success = True

    def __init__(self, kname=None, sip_user_id=None, last_name=None, first_name=None, did=None,
                 sip_password=None, email=None, **kwargs):
        # group_id will be inherited from BroadsoftRequest.default_group_id, but can be overridden by passing
        # group_id (will get picked up in **kwargs)
        self.did = did
        self.first_name = first_name
        self.kname = kname
        self.last_name = last_name
        self.sip_password = sip_password
        self.sip_user_id = sip_user_id
        self.email = email
        self.derive_email()
        BroadsoftRequest.__init__(self, **kwargs)
        self.derive_user_id()

    def derive_email(self):
        if not self.email and self.kname:
            self.email = str(self.kname) + '@mit.edu'

    def derive_user_id(self):
        if not self.sip_user_id and self.kname:
            self.sip_user_id = str(self.kname) + '@' + self.default_domain

    def to_xml(self):
        self.validate()
        self.did = BroadsoftRequest.convert_phone_number(number=self.did)

        # master is the entire XML document, cmd is the command element inserted within, which this object will be
        # manipulating
        (master, cmd) = BroadsoftRequest.master_to_xml(self)

        spid = ET.SubElement(cmd, 'serviceProviderId')
        spid.text = self.service_provider

        gid = ET.SubElement(cmd, 'groupId')
        gid.text = self.group_id

        uid = ET.SubElement(cmd, 'userId')
        uid.text = self.sip_user_id

        ln = ET.SubElement(cmd, 'lastName')
        ln.text = self.last_name

        fn = ET.SubElement(cmd, 'firstName')
        fn.text = self.first_name

        clidln = ET.SubElement(cmd, 'callingLineIdLastName')
        clidln.text = self.last_name

        clidfn = ET.SubElement(cmd, 'callingLineIdFirstName')
        clidfn.text = self.first_name

        pn = ET.SubElement(cmd, 'phoneNumber')
        pn.text = self.did

        pw = ET.SubElement(cmd, 'password')
        pw.text = self.sip_password

        e = ET.SubElement(cmd, 'emailAddress')
        e.text = self.email

        return master

    def validate(self):
        import re
        if self.group_id is None:
            raise ValueError("can't run broadsoft.UserAddRequest.to_xml() without a value for group_id")

        if self.sip_user_id is None:
            raise ValueError("can't run broadsoft.UserAddRequest.to_xml() without a value for sip_user_id. you can also add a kname and run derive_user_id()")

        if self.first_name is None:
            raise ValueError("can't run broadsoft.UserAddRequest.to_xml() without a value for first_name")

        if self.last_name is None:
            raise ValueError("can't run broadsoft.UserAddRequest.to_xml() without a value for last_name")

        if self.did is None or not re.match(r'^\d{10}$', str(self.did)):
            raise ValueError("can't run broadsoft.UserAddRequest.to_xml() without a valid value for did")

        if self.sip_password is None:
            raise ValueError("can't run broadsoft.UserAddRequest.to_xml() without a value for sip_password")

    @staticmethod
    def add(first_name, last_name, did, sip_user_id=None, kname=None, sip_password=None, email=None, **kwargs):
        g = UserAddRequest(**kwargs)
        g.post()
