import unittest
import unittest.mock

class TestBroadsoftXML(unittest.TestCase):
    def test_search_type_adds_search_elements(self):
        self.assertFalse("write this; probably XML_search extends XML, and then specific searches extend that")