""" DICOM Standard 2014 -- E.1.1 De-identifier
An Application may claim conformance to an Application Level Confidentiality
Profile and Options as a de-identifier if it protects and retains all
Attributes as specified in the Profile and Options.

This module exports the de-identify action code information to a JSON file. """
from __future__ import print_function
import re
import sys
import json

import requests
from bs4 import BeautifulSoup

ds_url = "http://medical.nema.org/medical/dicom/current/output/html/part15.html"
response = requests.get(ds_url)

soup = BeautifulSoup(response.text)
e11 = soup.find(attrs={ "id": re.compile("sect_E.1.1") })
ul = e11.parent.parent.parent.parent.parent \
        .find("ul", attrs={ "class": "itemizedlist" })

action_codes = {}
for item in ul.find_all("li"):
    code, desc = item.p.text.split("-", 1)
    action_codes[code.strip()] = desc.strip()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'w') as outfile:
            json.dump(action_codes, outfile, indent=2, separators=(',', ': '))
    else:
        import pprint
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(action_codes)