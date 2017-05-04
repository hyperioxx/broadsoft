import xml.etree.ElementTree as ET
from broadsoft.requestobjects.lib.BroadsoftRequest import BroadsoftRequest


class GroupAddRequest(BroadsoftRequest):
    command_name = 'GroupAddRequest'
    check_success = True

    def __init__(self, group_id=None, group_name=None, **kwargs):
        self.calling_line_id_name = None
        self.contact_email = None
        self.contact_name = None
        self.contact_number = None
        self.group_id = group_id
        self.group_name = group_name
        self.user_limit = 100000
        BroadsoftRequest.__init__(self, auto_derive_group_id=False, **kwargs)

    def derive_build_contact(self):
        attrs = [self.contact_email, self.contact_name, self.contact_number]
        for attr in attrs:
            if attr is not None:
                return True

        return False

    def derive_calling_line_id_name(self):
        if self.calling_line_id_name is not None:
            return self.calling_line_id_name

        elif self.group_name is not None:
            return str(self.group_name) + ' Line'

        elif self.group_id is not None:
            return str(self.group_id) + ' Line'

    def to_xml(self):
        self.validate()

        # master is the entire XML document, cmd is the command element inserted within, which this object will be
        # manipulating
        (master, cmd) = BroadsoftRequest.master_to_xml(self)

        if self.service_provider:
            sp = ET.SubElement(cmd, 'serviceProviderId')
            sp.text = str(self.service_provider)

        if self.group_id:
            gid = ET.SubElement(cmd, 'groupId')
            gid.text = self.group_id

        dd = ET.SubElement(cmd, 'defaultDomain')
        dd.text = self.default_domain

        if self.user_limit is not None:
            ul = ET.SubElement(cmd, 'userLimit')
            ul.text = str(int(self.user_limit))

        if self.group_name:
            gid = ET.SubElement(cmd, 'groupName')
            gid.text = self.group_name

        clid = ET.SubElement(cmd, 'callingLineIdName')
        clid.text = self.derive_calling_line_id_name()

        tz = ET.SubElement(cmd, 'timeZone')
        tz.text = self.timezone

        if self.derive_build_contact():
            c = ET.SubElement(cmd, 'contact')

            if self.contact_name:
                cname = ET.SubElement(c, 'contactName')
                cname.text = self.contact_name

            if self.contact_number:
                cnumber = ET.SubElement(c, 'contactNumber')
                cnumber.text = BroadsoftRequest.convert_phone_number(number=self.contact_number, dashes=True)

            if self.contact_email:
                ce = ET.SubElement(c, 'contactEmail')
                ce.text = self.contact_email

        return master

    def validate(self):
        if self.group_id is None and self.group_name is None:
            raise ValueError("can't run broadsoft.GroupAddRequest.to_xml() without a value for group_id or group_name")

    @staticmethod
    def add(group_id, group_name, **kwargs):
        g = GroupAddRequest(group_id=group_id, group_name=group_name, **kwargs)
        g.post()
