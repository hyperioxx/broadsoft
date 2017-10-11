import unittest.mock
from broadsoft.Voicemail import Voicemail
from broadsoft.lib.BroadsoftObject import BroadsoftObject
from xml.etree.ElementTree import Element
import xml.etree.ElementTree as ET
from broadsoft.requestobjects.UserVoiceMessagingUserModifyVoiceManagementRequest import UserVoiceMessagingUserModifyVoiceManagementRequest
from broadsoft.requestobjects.UserThirdPartyVoiceMailSupportModifyRequest import UserThirdPartyVoiceMailSupportModifyRequest
from broadsoft.requestobjects.UserVoiceMessagingUserModifyAdvancedVoiceManagementRequest import UserVoiceMessagingUserModifyAdvancedVoiceManagementRequest
from broadsoft.requestobjects.lib.BroadsoftRequest import instance_factory
from broadsoft.requestobjects.UserServiceAssignListRequest import UserServiceAssignListRequest
from broadsoft.requestobjects.UserServiceUnassignListRequest import UserServiceUnassignListRequest

def return_none(**kwargs):
    return None


class TestBroadsoftVoicemail(unittest.TestCase):
    def test_init(self):
        v = Voicemail(behavior='b', busy_to_voicemail='btv', cc_email='cce', did='617-555-1212', email='e',
                      mwi='m', no_answer_to_voicemail='natv', rings='r', straight_to_voicemail='stv', send_cc='scc',
                      sip_user_id='6175551212@mit.edu', type='broadsoftttt', transfer_on_zero='toz',
                      transfer_number='tn', surgemail_domain='sd')
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
        self.assertEqual('sd', v.surgemail_domain)

    def test_return_services(self):
        broadsoft_services = [
            'Voice Messaging User',
            'Voice Messaging User - Video',
            'Voice Portal Calling'
        ]

        unity_services = [
            'Third-Party MWI Control',
            'Third-Party Voice Mail Support'
        ]

        # when type is "broadsoft"
        v = Voicemail(sip_user_id='6175551212@beaver.mit.edu', email='beaver@mit.edu', did=6175551212,
                      surgemail_domain='sd.mit.edu')
        v.type = 'broadsoft'
        services, counterpart_services = v.get_services()

        self.assertEqual(services, broadsoft_services)
        self.assertEqual(counterpart_services, unity_services)

        # when type is "unity"
        v = Voicemail(sip_user_id='6175551212@beaver.mit.edu', email='beaver@mit.edu', did=6175551212,
                      surgemail_domain='sd.mit.edu')
        v.type = 'unity'
        services, counterpart_services = v.get_services()

        self.assertEqual(services, unity_services)
        self.assertEqual(counterpart_services, broadsoft_services)

    def test_type_determines_correct_activation(self):
        # -----------
        # with type BROADSOFT
        v = Voicemail(sip_user_id='6175551212@beaver.mit.edu', email='beaver@mit.edu', did=6175551212,
                      surgemail_domain='sd.mit.edu')
        v.type = 'broadsoft'
        activate = v.build_activate_command()
        deactivate = v.build_deactivate_counterpart_command()

        # activate should be a list, containing a UserServiceAssignListRequest, a
        # UserVoiceMessagingUserModifyVoiceManagementRequest, and a
        # UserVoiceMessagingUserModifyAdvancedVoiceManagementRequest
        self.assertEqual(3, len(activate))
        activate_services, activate_configure, activate_surgemail = activate

        self.assertIsInstance(activate_services, UserServiceAssignListRequest)
        self.assertIsInstance(activate_configure, UserVoiceMessagingUserModifyVoiceManagementRequest)
        self.assertIsInstance(activate_surgemail, UserVoiceMessagingUserModifyAdvancedVoiceManagementRequest)

        # test contents of activate_services object
        self.assertEqual(v.sip_user_id, activate_services.sip_user_id)
        self.assertEqual(activate_services.services, ['Voice Messaging User', 'Voice Messaging User - Video', 'Voice Portal Calling'])
        self.assertIsNone(activate_services.service_pack)

        # deactivate is a list with a UserServiceUnassignListRequest and a UserThirdPartyVoiceMailSupportModifyRequest
        self.assertEqual(2, len(deactivate))
        deactivate_services = deactivate[0]
        deactivate = deactivate[1]
        self.assertIsInstance(deactivate_services, UserServiceUnassignListRequest)
        self.assertIsInstance(deactivate, UserThirdPartyVoiceMailSupportModifyRequest)

        # test contents of deactivate_services
        self.assertEqual(v.sip_user_id, deactivate_services.sip_user_id)
        self.assertEqual(deactivate_services.services,
                         ['Third-Party MWI Control', 'Third-Party Voice Mail Support'])
        self.assertIsNone(deactivate_services.service_pack)

        # -----------
        # with type UNITY
        v = Voicemail(sip_user_id='6175551212@beaver.mit.edu', email='beaver@mit.edu', did=6175551212)
        v.type = 'unity'
        activate = v.build_activate_command()
        deactivate = v.build_deactivate_counterpart_command()

        # activate should be a list, containing a UserServiceAssignListRequest, and a
        # UserThirdPartyVoiceMailSupportModifyRequest
        self.assertEqual(2, len(activate))
        activate_services, activate_third_party = activate

        self.assertIsInstance(activate_services, UserServiceAssignListRequest)
        self.assertIsInstance(activate_third_party, UserThirdPartyVoiceMailSupportModifyRequest)

        # test contents of activate_services object
        self.assertEqual(v.sip_user_id, activate_services.sip_user_id)
        self.assertEqual(activate_services.services,
                         ['Third-Party MWI Control', 'Third-Party Voice Mail Support'])
        self.assertIsNone(activate_services.service_pack)

        # deactivate is a list with a UserServiceUnassignListRequest and a
        # UserVoiceMessagingUserModifyVoiceManagementRequest
        self.assertEqual(2, len(deactivate))
        deactivate_services = deactivate[0]
        deactivate = deactivate[1]
        self.assertIsInstance(deactivate_services, UserServiceUnassignListRequest)
        self.assertIsInstance(deactivate, UserVoiceMessagingUserModifyVoiceManagementRequest)

        # test contents of deactivate_services
        self.assertEqual(v.sip_user_id, deactivate_services.sip_user_id)
        self.assertEqual(deactivate_services.services,
                         ['Voice Messaging User', 'Voice Messaging User - Video', 'Voice Portal Calling'])
        self.assertIsNone(deactivate_services.service_pack)

        # ------------
        # with bad type
        v = Voicemail(sip_user_id='6175551212@beaver.mit.edu', email='beaver@mit.edu', did=6175551212)
        v.type = 'garbanzo'
        with self.assertRaises(NotImplementedError):
            v.build_activate_command()

        with self.assertRaises(NotImplementedError):
            v.build_deactivate_counterpart_command()

    def test_validate(self):
        # missing sip_user_id
        v = Voicemail(email='beaver@mit.edu', did=6175551212)
        v.sip_user_id = None
        with self.assertRaises(ValueError):
            v.validate()

        # missing email
        v = Voicemail(sip_user_id='6175551212@beaver.mit.edu', did=6175551212)
        with self.assertRaises(ValueError):
            v.validate()

        # missing DID
        v = Voicemail(sip_user_id='6175551212@beaver.mit.edu', email='beaver@mit.edu')
        with self.assertRaises(ValueError):
            v.validate()

    def test_activate_barfs_with_bad_type(self):
        v = Voicemail(sip_user_id='6175551212@beaver.mit.edu', email='beaver@mit.edu', type='garbanzo', did=6175551212)
        with self.assertRaises(NotImplementedError):
            v.build_activate_command()

    def test_deactivate_barfs_with_bad_type(self):
        v = Voicemail(sip_user_id='6175551212@beaver.mit.edu', email='beaver@mit.edu', type='garbanzo', did=6175551212)
        with self.assertRaises(NotImplementedError):
            v.build_deactivate_counterpart_command()

    def test_voicemail_inherits_default_surgemail_domain_from_instance(self):
        test_i = instance_factory(instance='test')
        prod_i = instance_factory(instance='prod')

        # default should be prod
        v = Voicemail()
        self.assertEqual(prod_i.surgemail_domain, v.surgemail_domain)

        # explicitly prod
        v = Voicemail(broadsoftinstance=prod_i)
        self.assertEqual(prod_i.surgemail_domain, v.surgemail_domain)

        # explicitly test
        v = Voicemail(broadsoftinstance=test_i)
        self.assertEqual(test_i.surgemail_domain, v.surgemail_domain)

        # can override
        v = Voicemail(broadsoftinstance=test_i, surgemail_domain='override')
        self.assertEqual('override', v.surgemail_domain)

    @unittest.mock.patch.object(BroadsoftObject, '__init__', side_effect=None)
    def test_init_calls_broadsoftobject_init(self, bo_init_patch):
        # this will throw an error since we're mocking BroadsoftObject.__init__, and setting surgemaildomain requires
        # that call
        try:
            v = Voicemail()
        except AttributeError:
            pass

        self.assertTrue(bo_init_patch.called)
