""" DICOM Standard 2014 -- E.1.1 De-identifier
An Application may claim conformance to an Application Level
Confidentiality Profile and Options as a de-identifier if it
protects and retains allAttributes as specified in the Profile
and Options. """
from __future__ import print_function
import re
import requests
from bs4 import BeautifulSoup

response = requests.get("http://medical.nema.org/medical/dicom/current/output/html/part15.html")

soup = BeautifulSoup(response.text)
e11 = soup.find(attrs={ "id": re.compile("table_E.1-1") })
print(e11.parent)