import unittest.mock
from broadsoft.Voicemail import Voicemail
from broadsoft.lib.BroadsoftObject import BroadsoftObject
from xml.etree.ElementTree import Element
import xml.etree.ElementTree as ET
from broadsoft.requestobjects.UserVoiceMessagingUserModifyVoiceManagementRequest import UserVoiceMessagingUserModifyVoiceManagementRequest
from broadsoft.requestobjects.UserThirdPartyVoiceMailSupportModifyRequest import UserThirdPartyVoiceMailSupportModifyRequest
from broadsoft.requestobjects.UserVoiceMessagingUserModifyAdvancedVoiceManagementRequest import UserVoiceMessagingUserModifyAdvancedVoiceManagementRequest

def return_none(**kwargs):
    return None


class TestBroadsoftVoicemail(unittest.TestCase):
    def test_init(self):
        v = Voicemail(behavior='b', busy_to_voicemail='btv', cc_email='cce', did='617-555-1212', email='e',
                      mwi='m', no_answer_to_voicemail='natv', rings='r', straight_to_voicemail='stv', send_cc='scc',
                      sip_user_id='6175551212@mit.edu', type='broadsoftttt', transfer_on_zero='toz',
                      transfer_number='tn')
        self.assertEqual('b', v.behavior)
        self.assertEqual('btv', v.busy_to_voicemail)
        self.assertEqual('cce', v.cc_email)
        self.assertEqual('6175551212', v.did)
        self.assertEqual('e', v.email)
        self.assertEqual('m', v.mwi)
        self.assertEqual('natv', v.no_answer_to_voicemail)
        self.assertEqual('r', v.rings)
        self.assertEqual('stv', v.straight_to_voicemail)
        self.assertEqual('scc', v.send_cc)
        self.assertEqual('6175551212@mit.edu', v.sip_user_id)
        self.assertEqual('broadsoftttt', v.type)
        self.assertEqual('toz', v.transfer_on_zero)
        self.assertEqual('tn', v.transfer_number)

    def test_type_determines_correct_activation(self):
        v = Voicemail(sip_user_id='6175551212@beaver.mit.edu', email='beaver@mit.edu')
        v.type = 'broadsoft'
        activate = v.build_activate_command()
        deactivate = v.build_deactivate_counterpart_command()

        # activate should be a list, containing a UserVoiceMessagingUserModifyVoiceManagementRequest and a
        # UserVoiceMessagingUserModifyAdvancedVoiceManagementRequest
        activate_configure, activate_surgemail = activate

        self.assertIsInstance(activate_configure, UserVoiceMessagingUserModifyVoiceManagementRequest)
        self.assertIsInstance(activate_surgemail, UserVoiceMessagingUserModifyAdvancedVoiceManagementRequest)

        # deactivate is a list with just a UserThirdPartyVoiceMailSupportModifyRequest
        deactivate = deactivate[0]
        self.assertIsInstance(deactivate, UserThirdPartyVoiceMailSupportModifyRequest)

        v = Voicemail(sip_user_id='6175551212@beaver.mit.edu', email='beaver@mit.edu')
        v.type = 'unity'
        activate = v.build_activate_command()
        deactivate = v.build_deactivate_counterpart_command()

        # activate and deactivate here are both single item lists
        activate = activate[0]
        deactivate = deactivate[0]

        self.assertIsInstance(activate, UserThirdPartyVoiceMailSupportModifyRequest)
        self.assertIsInstance(deactivate, UserVoiceMessagingUserModifyVoiceManagementRequest)

        v = Voicemail(sip_user_id='6175551212@beaver.mit.edu', email='beaver@mit.edu')
        v.type = 'garbanzo'
        with self.assertRaises(NotImplementedError):
            v.build_activate_command()

        with self.assertRaises(NotImplementedError):
            v.build_deactivate_counterpart_command()

    def test_validate(self):
        v = Voicemail(email='beaver@mit.edu')
        with self.assertRaises(ValueError):
            v.validate()

        v = Voicemail(sip_user_id='6175551212@beaver.mit.edu')
        with self.assertRaises(ValueError):
            v.validate()

    def test_activate_barfs_with_bad_type(self):
        v = Voicemail(sip_user_id='6175551212@beaver.mit.edu', email='beaver@mit.edu', type='garbanzo')
        with self.assertRaises(NotImplementedError):
            v.build_activate_command()

    def test_deactivate_barfs_with_bad_type(self):
        v = Voicemail(sip_user_id='6175551212@beaver.mit.edu', email='beaver@mit.edu', type='garbanzo')
        with self.assertRaises(NotImplementedError):
            v.build_deactivate_counterpart_command()
