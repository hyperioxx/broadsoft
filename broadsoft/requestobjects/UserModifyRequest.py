import xml.etree.ElementTree as ET
from broadsoft.requestobjects.lib.BroadsoftRequest import BroadsoftRequest


class UserModifyRequest(BroadsoftRequest):
    command_name = 'UserModifyRequest16'
    check_success = True

    def __init__(self, sip_user_id=None, last_name=None, first_name=None, clid_first_name=None,
                 clid_last_name=None, name_dialing_name=None, did=None, extension=None, clid_did=None,
                 old_password=None, new_password=None, email_address=None, device_name=None,
                 line_port=None, include_endpoint=False,
                 **kwargs):
        self.clid_did = clid_did
        self.clid_first_name = clid_first_name
        self.clid_last_name = clid_last_name
        self.device_name = device_name
        self.did = did
        self.email_address = email_address
        self.extension = extension
        self.first_name = first_name
        self.last_name = last_name
        self.line_port = line_port
        self.name_dialing_name = name_dialing_name
        self.new_password = new_password
        self.old_password = old_password
        self.sip_user_id = sip_user_id
        self.include_endpoint = include_endpoint
        self.derive_extension()

        self.drone_actions = {}

        BroadsoftRequest.__init__(self, **kwargs)

    def build_command_xml(self):
        from broadsoft.requestobjects.datatypes.EndPoint import Endpoint

        self.prep_for_xml()
        self.derive_extension()
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
        if self.include_endpoint:
            e = Endpoint(line_port=self.line_port)
            ex = e.to_xml()
            if ex:
                cmd.append(ex)

        return cmd

    def derive_extension(self, digits=5):
        if not self.extension and self.did:
            self.did = BroadsoftRequest.convert_phone_number(number=self.did)
            self.extension = str(self.did)[-digits:]

    def prep_attributes(self):
        BroadsoftRequest.prep_attributes(self)
        self.set_drones()

    def set_drones(self):
        # define the drone attrs, and the parent they draw from
        drones = {
            'clid_first_name': 'first_name',
            'clid_last_name': 'last_name',
            'clid_did': 'did'
        }

        # want to keep track of when we automatically set drones vs when user does so know when to overwrite implicitly
        for attr, parent in drones.items():
            drone_val = getattr(self, attr)
            parent_val = getattr(self, parent)

            overwrite_drone = False

            # does the drone have a non-None value?
            if drone_val is not None:
                # is the drone val equal to what was set automatically? overwrite.
                if attr in self.drone_actions and self.drone_actions[attr] == drone_val:
                    overwrite_drone = True

            # is the drone None? overwrite.
            else:
                overwrite_drone = True

            if overwrite_drone:
                self.drone_actions[attr] = parent_val
                setattr(self, attr, parent_val)

    def validate(self):
        import re
        if self.sip_user_id is None:
            raise ValueError("can't run broadsoft.UserModifyRequest.to_xml() without a value for sip_user_id.")

        if self.did and not re.match(r'^\d{10}$', str(self.did)):
            raise ValueError("the value for did you provided to UserModifyRequest is not valid")

        if self.clid_did and not re.match(r'^\d{10}$', str(self.clid_did)):
            raise ValueError("the value for clid_did you provided to UserModifyRequest is not valid")

        if self.extension and not re.match(r'^\d+$', str(self.extension)):
            raise ValueError("the value for extension you provided to UserModifyRequest is not valid")

    @staticmethod
    def set_password(new_password, did, sip_user_id, **kwargs):
        u = UserModifyRequest(did=did, sip_user_id=sip_user_id, new_password=new_password, **kwargs)
        u.post()
