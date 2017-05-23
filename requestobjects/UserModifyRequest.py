import xml.etree.ElementTree as ET
from broadsoft.requestobjects.lib.BroadsoftRequest import BroadsoftRequest


class UserModifyRequest(BroadsoftRequest):
    command_name = 'UserModifyRequest16'
    check_success = True

    def __init__(self, sip_user_id=None, last_name=None, first_name=None, clid_first_name=None,
                 clid_last_name=None, name_dialing_name=None, did=None, extension=None, clid_did=None,
                 old_password=None, new_password=None, email_address=None, device_name=None,
                 line_port=None,
                 **kwargs):
        self.clid_did = clid_did
        if self.clid_did:
            self.clid_did = BroadsoftRequest.convert_phone_number(number=self.clid_did)
        self.clid_first_name = clid_first_name
        self.clid_last_name = clid_last_name
        self.device_name = device_name
        self.did = did
        if self.did:
            self.did = BroadsoftRequest.convert_phone_number(number=self.did)
        self.email_address = email_address
        self.extension = extension
        self.first_name = first_name
        self.last_name = last_name
        self.line_port = line_port
        self.name_dialing_name = name_dialing_name
        self.new_password = new_password
        self.old_password = old_password
        self.sip_user_id = sip_user_id
        self.derive_extension()

        BroadsoftRequest.__init__(self, **kwargs)

        # now that BroadsoftRequest has set domain, can run these
        if not self.sip_user_id:
            self.sip_user_id = self.derive_sip_user_id()
        if not self.line_port:
            self.line_port = self.derive_sip_user_id(line_port=True)

    def build_command_xml(self):
        from broadsoft.requestobjects.datatypes.EndPoint import Endpoint
        if self.did:
            self.did = BroadsoftRequest.convert_phone_number(number=self.did)
        if self.clid_did:
            self.clid_did = BroadsoftRequest.convert_phone_number(number=self.clid_did)
        self.derive_extension()
        if not self.sip_user_id:
            self.sip_user_id = self.derive_sip_user_id()
        if not self.line_port:
            self.line_port = self.derive_sip_user_id(line_port=True)

        self.validate()

        cmd = self.build_command_shell()

        uid = ET.SubElement(cmd, 'userId')
        uid.text = self.sip_user_id

        if self.last_name:
            lname = ET.SubElement(cmd, 'lastName')
            lname.text = self.last_name

        if self.first_name:
            fname = ET.SubElement(cmd, 'firstName')
            fname.text = self.first_name

        if self.clid_last_name:
            clid_lname = ET.SubElement(cmd, 'callingLineIdLastName')
            clid_lname.text = self.clid_last_name

        if self.clid_first_name:
            clid_fname = ET.SubElement(cmd, 'callingLineIdFirstName')
            clid_fname.text = self.clid_first_name

        if self.name_dialing_name:
            ndn = ET.SubElement(cmd, 'nameDialingName')
            ndn.text = self.name_dialing_name

        if self.did:
            pn = ET.SubElement(cmd, 'phoneNumber')
            pn.text = str(self.did)

        if self.extension:
            e = ET.SubElement(cmd, 'extension')
            e.text = str(self.extension)

        if self.clid_did:
            clid_did = ET.SubElement(cmd, 'callingLineIdPhoneNumber')
            clid_did.text = str(self.clid_did)

        if self.old_password:
            op = ET.SubElement(cmd, 'oldPassword')
            op.text = self.old_password

        if self.new_password:
            np = ET.SubElement(cmd, 'newPassword')
            np.text = self.new_password

        if self.email_address:
            e = ET.SubElement(cmd, 'emailAddress')
            e.text = self.email_address

        # building the endpoint is a little complicated, so hand that off...
        e = Endpoint(device_name=self.device_name, line_port=self.line_port)
        ex = e.to_xml()
        if ex:
            cmd.append(ex)

        return cmd

    def derive_extension(self, digits=4):
        if not self.extension and self.did:
            self.did = BroadsoftRequest.convert_phone_number(number=self.did)
            self.extension = str(self.did)[-digits:]

    def validate(self):
        import re
        if self.sip_user_id is None:
            raise ValueError("can't run broadsoft.UserModifyRequest.to_xml() without a value for sip_user_id. you can also add a kname and run derive_user_id()")

        if self.did and not re.match(r'^\d{10}$', str(self.did)):
            raise ValueError("the value for did you provided to UserModifyRequest is not valid")

        if self.clid_did and not re.match(r'^\d{10}$', str(self.clid_did)):
            raise ValueError("the value for clid_did you provided to UserModifyRequest is not valid")

        if self.extension and not re.match(r'^\d+$', str(self.extension)):
            raise ValueError("the value for extension you provided to UserModifyRequest is not valid")

    @staticmethod
    def modify(**kwargs):
        #u = UserModifyRequest(first_name=first_name, last_name=last_name, did=did, sip_user_id=sip_user_id, kname=kname, sip_password=sip_password, email=email, **kwargs)
        #u.post()
        pass

