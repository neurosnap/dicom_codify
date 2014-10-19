""" DICOM Standard 2014 -- E.1.1 De-identifier
An Application may claim conformance to an Application Level Confidentiality
Profile and Options as a de-identifier if it protects and retains all
Attributes as specified in the Profile and Options. """
from __future__ import print_function
import re
import pprint

import requests
from bs4 import BeautifulSoup

pp = pprint.PrettyPrinter(indent=4)

Z = """replace with a zero length value, or a non-zero length value that may be
        a dummy value and consistent with the VR"""

C = """clean, that is replace with values of similar meaning known not to
        contain identifying information and consistent with the VR"""

XZU = """X unless Z or replacement of contained instance UIDs (U) is required
        to maintain IOD conformance (Type 3 versus Type 2 versus Type 1
        sequences containing UID references)"""

action_codes = {
    "D": "replace with a non-zero length value that may be a dummy value and consistent with the VR",
    "Z": Z,
    "X": "remove",
    "K": "keep (unchanged for non-sequence attributes, cleaned for sequences)",
    "C": C,
    "U": "replace with a non-zero length UID that is internally consistent within a set of Instances",
    "Z/D": "Z unless D is required to maintain IOD conformance (Type 2 versus Type 1)",
    "X/Z": "X unless Z is required to maintain IOD conformance (Type 3 versus Type 2)",
    "X/D": "X unless D is required to maintain IOD conformance (Type 3 versus Type 1)",
    "X/Z/D": "X unless Z or D is required to maintain IOD conformance (Type 3 versus Type 2 versus Type 1)",
    "X/Z/U": XZU,
}

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
pp.pprint(tags)
