
import os
import unittest

import requests
import vcr
import bs4

import dicom_deidentify as ddi

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

class TestDeidentify(unittest.TestCase):

    def setUp(self):
        self.url = "http://medical.nema.org/medical/dicom/current/output/html/part15.html"

        with vcr.use_cassette(os.path.join(BASE_DIR, 'fixtures', 'vcr_cassettes', 'first_test.yaml')):
            response = requests.get(self.url)
            self.html = response.text

        self.soup = bs4.BeautifulSoup(self.html)
        self.deidentify = ddi.get_deidentify(self.soup)
        self.action_codes = ddi.get_action_codes(self.soup)

    def test_soup_property(self):
        """ dicom_deidentify.soup() ought return BeautifulSoup object """
        soup = ddi.soup(self.html)
        self.assertIsInstance(soup, bs4.BeautifulSoup)
        self.assertEqual(soup, self.soup)

    def test_action_codes(self):
        """ Make sure all action codes are present in dictionary """
        self.assertIn("C", self.action_codes)
        self.assertIn("Z/D", self.action_codes)
        self.assertIn("D", self.action_codes)
        self.assertIn("X/Z/D", self.action_codes)
        self.assertIn("K", self.action_codes)
        self.assertIn("X/Z", self.action_codes)
        self.assertIn("X/D", self.action_codes)
        self.assertIn("U", self.action_codes)
        self.assertIn("X", self.action_codes)
        self.assertIn("Z", self.action_codes)
        self.assertIn("X/Z/U*", self.action_codes)

    def test_deidentify_length(self):
        """ Make sure number of tags are present in deidentify list from
        when originally created """
        self.assertEqual(271, len(self.deidentify))

    def test_deidentify_keys(self):
        """ Make sure all keys are present in deidentify dictionary """
        self.assertIn("Retain Long. Modif. Dates Option", self.deidentify[0])
        self.assertIn("Retain Long. Modif. Dates Option", self.deidentify[0])
        self.assertIn("Retain Long. Full Dates Option", self.deidentify[0])
        self.assertIn("Basic Profile", self.deidentify[0])
        self.assertIn("Retain UIDs Option", self.deidentify[0])
        self.assertIn("Clean Graph. Option", self.deidentify[0])
        self.assertIn("Retain Patient Chars. Option", self.deidentify[0])
        self.assertIn("Attribute Name", self.deidentify[0])
        self.assertIn("Tag", self.deidentify[0])
        self.assertIn("Retain Safe Private Option", self.deidentify[0])
        self.assertIn("In Std. Comp. IOD (from PS3.3)", self.deidentify[0])
        self.assertIn("Clean Desc. Option", self.deidentify[0])
        self.assertIn("Retired (from PS3.6)", self.deidentify[0])
        self.assertIn("Retain Device Ident. Option", self.deidentify[0])
        self.assertIn("Clean Struct. Cont. Option", self.deidentify[0])

if __name__ == '__main__':
    unittest.main(verbosity=2)