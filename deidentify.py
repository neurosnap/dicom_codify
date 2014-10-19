""" DICOM Standard 2014 -- E.1.1 De-identifier
An Application may claim conformance to an Application Level Confidentiality
Profile and Options as a de-identifier if it protects and retains all
Attributes as specified in the Profile and Options.

This module exports the DICOM data element tag information to a JSON file. """
from __future__ import print_function
import re
import sys
import json

import requests
from bs4 import BeautifulSoup

ds_url = "http://medical.nema.org/medical/dicom/current/output/html/part15.html"
response = requests.get(ds_url)

soup = BeautifulSoup(response.text)
e11 = soup.find(attrs={ "id": re.compile("table_E.1-1") })
table = e11.parent.table
# table headers
thead = table.find("thead")
headers = [header.find("strong").text for header in thead.find_all("th")]
# table body
tbody = table.find("tbody")
trows = tbody.find_all("tr")
tags = []
for row in trows:
    obj = {}
    for index, cell in enumerate(row.find_all("td")):
        if len(headers) < index:
            break
        if cell.p is None:
            obj[headers[index]] = None
        else:
            obj[headers[index]] = cell.p.text
    tags.append(obj)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'w') as outfile:
            json.dump(tags, outfile, indent=2, separators=(',', ': '))
    else:
        import pprint
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(action_codes)