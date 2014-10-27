""" Some quick-n-dirty unit tests for HTML consistency, stable
keys, and list lengths from when I originally created this utilty """
import os
import re
import unittest

import bs4

import dicom_codify as dci

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

class TestDeidentify(unittest.TestCase):

    def setUp(self):
        self.soup = dci.soup(part=15)
        self.deidentify = dci.get_deidentify(self.soup)
        self.action_codes = dci.get_action_codes(self.soup)

        ded_soup = dci.soup(part=6)
        e61 = ded_soup.find(attrs={ "id": re.compile("table_6-1") })
        e71 = ded_soup.find(attrs={ "id": re.compile("table_7-1") })
        e81 = ded_soup.find(attrs={ "id": re.compile("table_8-1") })
        self.ded = dci.get_data_element_dictionary(e61.parent.table) \
                   + dci.get_data_element_dictionary(e71.parent.table) \
                   + dci.get_data_element_dictionary(e81.parent.table)

    def test_soup_property(self):
        """ dicom_deidentify.soup() ought return BeautifulSoup object """
        soup = dci.soup(self.html)
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

    def test_data_element_dictionary_length(self):
        """ Make sure list length for dictionary is same from when
        originall created  """
        self.assertEqual(3839, len(self.ded))

    def test_data_element_dictionary_keys(self):
        """ Make sure all keys are present from when originally created """
        self.assertIn("Keyword", self.ded[0])
        self.assertIn("Name", self.ded[0])
        self.assertIn("Status", self.ded[0])
        self.assertIn("Tag", self.ded[0])
        self.assertIn("VM", self.ded[0])
        self.assertIn("VR", self.ded[0])


if __name__ == '__main__':
    unittest.main(verbosity=2)