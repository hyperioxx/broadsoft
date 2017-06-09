import xml.etree.ElementTree as ET
from broadsoft.requestobjects.lib.BroadsoftRequest import BroadsoftRequest


class UserThirdPartyVoiceMailSupportModifyRequest(BroadsoftRequest):
    command_name = 'UserThirdPartyVoiceMailSupportModifyRequest'
    check_success = True

    booleans = [
        'is_active',
        'busy_redirect_to_voice_mail',
        'no_answer_redirect_to_voice_mail',
        'always_redirect_to_voice_mail',
        'out_of_primary_zone_redirect_to_voice_mail'
    ]

    def __init__(self, sip_user_id=None, is_active=None, busy_redirect_to_voice_mail=None,
                 no_answer_redirect_to_voice_mail=None, server_selection=None, user_server=None, mailbox_id_type=None,
                 no_answer_number_of_rings=None, always_redirect_to_voice_mail=None,
                 out_of_primary_zone_redirect_to_voice_mail=None,
                 **kwargs):
        self.always_redirect_to_voice_mail = always_redirect_to_voice_mail
        self.busy_redirect_to_voice_mail = busy_redirect_to_voice_mail
        self.is_active = is_active
        self.mailbox_id_type = mailbox_id_type
        self.no_answer_number_of_rings = no_answer_number_of_rings
        self.no_answer_redirect_to_voice_mail = no_answer_redirect_to_voice_mail
        self.out_of_primary_zone_redirect_to_voice_mail = out_of_primary_zone_redirect_to_voice_mail
        self.server_selection = server_selection
        self.sip_user_id = sip_user_id
        self.user_server = user_server
        BroadsoftRequest.__init__(self, **kwargs)

    def build_command_xml(self):
        if self.user_server is not None:
            self.user_server = BroadsoftRequest.convert_phone_number(number=self.user_server)
        self.prep_for_xml()
        self.validate()

        cmd = self.build_command_shell()

        uid = ET.SubElement(cmd, 'userId')
        uid.text = self.sip_user_id

        if self.is_active is not None:
            s = ET.SubElement(cmd, 'isActive')
            s.text = self.is_active

        if self.busy_redirect_to_voice_mail is not None:
            s = ET.SubElement(cmd, 'busyRedirectToVoiceMail')
            s.text = self.busy_redirect_to_voice_mail

        if self.no_answer_redirect_to_voice_mail is not None:
            s = ET.SubElement(cmd, 'noAnswerRedirectToVoiceMail')
            s.text = self.no_answer_redirect_to_voice_mail

        if self.server_selection is not None:
            s = ET.SubElement(cmd, 'serverSelection')
            s.text = self.server_selection

        if self.user_server is not None:
            s = ET.SubElement(cmd, 'userServer')
            s.text = str(self.user_server)

        if self.mailbox_id_type is not None:
            s = ET.SubElement(cmd, 'mailboxIdType')
            s.text = self.mailbox_id_type

        if self.no_answer_number_of_rings is not None:
            s = ET.SubElement(cmd, 'noAnswerNumberOfRings')
            s.text = str(self.no_answer_number_of_rings)

        if self.always_redirect_to_voice_mail is not None:
            s = ET.SubElement(cmd, 'alwaysRedirectToVoiceMail')
            s.text = self.always_redirect_to_voice_mail

        if self.out_of_primary_zone_redirect_to_voice_mail is not None:
            s = ET.SubElement(cmd, 'outOfPrimaryZoneRedirectToVoiceMail')
            s.text = self.out_of_primary_zone_redirect_to_voice_mail

        return cmd

    def validate(self):
        if self.sip_user_id is None:
            raise ValueError("can't run broadsoft.UserSharedCallAppearanceModifyRequest.to_xml() without a value for sip_user_id.")

    @staticmethod
    def activate_unity_voicemail(sip_user_id, busy_redirect_to_voice_mail=True,
                                       no_answer_redirect_to_voice_mail=True, server_selection='User Specific Mail Server',
                                       user_server=6172530000, mailbox_id_type='User Or Group Phone Number',
                                 no_answer_number_of_rings=3, always_redirect_to_voice_mail=False,
                                 out_of_primary_zone_redirect_to_voice_mail=False,
                                 **kwargs):
        u = UserThirdPartyVoiceMailSupportModifyRequest(sip_user_id=sip_user_id, is_active=True,
                                                        busy_redirect_to_voice_mail=busy_redirect_to_voice_mail,
                                                        no_answer_redirect_to_voice_mail=no_answer_redirect_to_voice_mail,
                                                        server_selection=server_selection, user_server=user_server,
                                                        mailbox_id_type=mailbox_id_type,
                                                        no_answer_number_of_rings=no_answer_number_of_rings,
                                                        always_redirect_to_voice_mail=always_redirect_to_voice_mail,
                                                        out_of_primary_zone_redirect_to_voice_mail=out_of_primary_zone_redirect_to_voice_mail,
                                                        **kwargs)
        u.post()

    @staticmethod
    def deactivate_unity_voicemail(sip_user_id, **kwargs):
        u = UserThirdPartyVoiceMailSupportModifyRequest(sip_user_id=sip_user_id, is_active=False, **kwargs)
        u.post()
