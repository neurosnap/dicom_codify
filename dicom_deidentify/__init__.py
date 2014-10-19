""" DICOM Standard 2014 -- E.1.1 De-identifier
An Application may claim conformance to an Application Level Confidentiality
Profile and Options as a de-identifier if it protects and retains all
Attributes as specified in the Profile and Options.

This module exports the de-identify action code information and the data
element tags to be replaced or removed to a JSON file. """
from __future__ import print_function
import re
import sys
import json

import requests
from bs4 import BeautifulSoup

def soup():
    """ Download DICOM Standard HTML and convert it into Beautiful Soup
    Object """
    ds_url = "http://medical.nema.org/medical/dicom/current/output/html/part15.html"
    response = requests.get(ds_url)

    return BeautifulSoup(response.text)

def get_action_codes(soup):
    """ Get action codes that instruct what to do with the DICOM data elements
    that need to be modified for basic DICOM anonymization """
    e11 = soup.find(attrs={ "id": re.compile("sect_E.1.1") })
    ul = e11.parent.parent.parent.parent.parent \
            .find("ul", attrs={ "class": "itemizedlist" })

    action_codes = {}
    for item in ul.find_all("li"):
        code, desc = item.p.text.split("-", 1)
        action_codes[code.strip()] = desc.strip()

    return action_codes

def get_deidentify(soup):
    """ Get DICOM data element tags to remove or replace for basic
    anonymization """
    e11 = soup.find(attrs={ "id": re.compile("table_E.1-1") })
    table = e11.parent.table
    # table headers
    thead = table.find("thead")
    headers = [header.find("strong").text for header in thead.find_all("th")]
    # table body
    tbody = table.find("tbody")
    trows = tbody.find_all("tr")
    deidentify = []
    for row in trows:
        obj = {}
        for index, cell in enumerate(row.find_all("td")):
            if len(headers) < index:
                break
            if cell.p is None:
                obj[headers[index]] = None
            else:
                obj[headers[index]] = cell.p.text
        deidentify.append(obj)

    return deidentify

def create_json(fname, data):
    """ Create JSON file

    :param fname: Name of the file to be saved
    :param data: Array or dictionary to be converted to JSON
    """
    with open(fname, 'w') as outfile:
        json.dump(data, outfile, indent=2, separators=(',', ': '))

    return True
