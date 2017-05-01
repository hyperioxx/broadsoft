import unittest.mock
import xml.etree.ElementTree as ET

from broadsoft.requestobjects.lib.SearchRequest import SearchRequest


class TestBroadsoftSearchRequest(unittest.TestCase):
    def test_build_search_criteria__validate(self):
        s = SearchRequest.SearchCriteria(mode='Starts With')

        # should run without incident
        s.add__validate()

        s = SearchRequest.SearchCriteria(mode='blaj')
        with self.assertRaises(ValueError):
            s.add__validate()

    def test_init_accepts_args(self):
        s = SearchRequest.SearchCriteria(mode='modemode', value='valval', case_insensitive=False)
        self.assertEqual('modemode', s.mode)
        self.assertEqual('valval', s.value)
        self.assertFalse(s.case_insensitive)

        s = SearchRequest.SearchCriteria(mode='ala', value='high', case_insensitive=True)
        self.assertEqual('ala', s.mode)
        self.assertEqual('high', s.value)
        self.assertTrue(s.case_insensitive)

    def test_build_search_criteria_call(self):
        # Never actually call SearchRequest directly; rather will have a specific instantiation which will build an
        # XmlRequest document. Here we'll just pass some dummy XML to test what SearchRequest builds
        x = ET.Element('searchCriteriaDummy')

        s = SearchRequest.SearchCriteria(value='honesty', case_insensitive=False)
        s.embed(parent=x)
        self.assertEqual(
            '<searchCriteriaDummy>' +
            '<mode>' + s.mode + '</mode>' +
            '<value>' + s.value + '</value>' +
            '<isCaseInsensitive>false</isCaseInsensitive>' +
            '</searchCriteriaDummy>',
            ET.tostring(element=x).decode("utf-8")
        )

        x = ET.Element('searchCriteriaDummy')
        s = SearchRequest.SearchCriteria(value='care', case_insensitive=True)
        s.embed(parent=x)
        self.assertEqual(
            '<searchCriteriaDummy>' +
            '<mode>' + s.mode + '</mode>' +
            '<value>' + s.value + '</value>' +
            '<isCaseInsensitive>true</isCaseInsensitive>' +
            '</searchCriteriaDummy>',
            ET.tostring(element=x).decode("utf-8")
        )

    @unittest.mock.patch.object(SearchRequest.SearchCriteria, 'add__validate')
    def test_build_search_criteria_calls_validate(
            self,
            validate_patch
    ):
        s = SearchRequest.SearchCriteria()
        x = ET.Element('searchCriteriaDummy')
        s.embed(parent=x)
        self.assertTrue(validate_patch.called)

    def test_use_test_gets_passed_to_broadsoftdocument(self):
        g = SearchRequest()
        self.assertEqual(g.prod_url, g.api_url)

        g = SearchRequest(use_test=False)
        self.assertEqual(g.prod_url, g.api_url)

        g = SearchRequest(use_test=True)
        self.assertEqual(g.test_url, g.api_url)

    def test_can_pass_session_id(self):
        g = SearchRequest(session_id='sesh')
        self.assertEqual('sesh', g.session_id)