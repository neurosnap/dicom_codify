""" DICOM Standard 2014 -- Codify """
from __future__ import print_function
import re
import sys
import json

import requests
from bs4 import BeautifulSoup

def soup(html=None, part=15):
    """ Download DICOM Standard HTML and convert it into Beautiful Soup
    Object

    :param html: Instead of using requests to grab HTML, supply HTML from other source"""
    url = "http://medical.nema.org/medical/dicom/current/output/html/part{0}.html".format(str(part).zfill(2))
    if html is None:
        response = requests.get(url)
        html = response.text

    return BeautifulSoup(html)

def get_action_codes(soup):
    """ Get action codes that instruct what to do with the DICOM data elements
    that need to be modified for basic DICOM anonymization

    :param soup: BeautifulSoup object containing DICOM standard documentation """
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
    anonymization

    :param soup: BeautifulSoup object containing DICOM standard documentation"""
    e11 = soup.find(attrs={ "id": re.compile("table_E.1-1") })
    table = e11.parent.table
    # table headers
    thead = table.find("thead")
    headers = [header.strong.text for header in thead.find_all("th")]
    # table body
    tbody = table.find("tbody")
    trows = tbody.find_all("tr")
    deidentify = []
    for row in trows:
        obj = {}
        for index, cell in enumerate(row.find_all("td")):
            if len(headers) < index or index >= len(headers):
                break
            if cell.p is None:
                obj[headers[index]] = None
            else:
                obj[headers[index]] = cell.p.text
        deidentify.append(obj)

    return deidentify

def get_data_element_dictionary(table):
    """ Get all curently supported DICOM data elements, file meta elements,
    and directory structuring elements

    :param table: BeautifulSoup object containing a DICOM data element HTML table"""
    # type
    de_type = table.parent.parent.find(attrs={ "class": "title" })
    de_type = de_type.strong.text.split(".")[1].strip()
    de_type = de_type.encode("utf8") \
                     .decode("ascii", errors="ignore") \
                     .replace("\n", "")
    # table headers
    thead = table.find("thead")
    headers = [header.strong.text for header in thead.find_all("th") \
                if header.strong is not None]
    headers.append(u"Status")
    # table body
    tbody = table.find("tbody")
    trows = tbody.find_all("tr")
    dictionary = []
    for row in trows:
        obj = {
            "Type": de_type
        }
        for index, cell in enumerate(row.find_all("td")):
            #print(cell.p)
            key = headers[index]
            if cell.p is None:
                obj[key] = None
            else:
                if cell.p.span is None:
                    obj[key] = cell.p.text \
                                .encode("utf8") \
                                .decode("ascii", errors="ignore") \
                                .replace("\n", "")
                else:
                    obj[key] = cell.p.span.text \
                                .encode("utf8") \
                                .decode("ascii", errors="ignore") \
                                .replace("\n", "")
        dictionary.append(obj)

    return dictionary

def create_json(fname, data):
    """ Create JSON file

    :param fname: Name of the file to be saved
    :param data: Array or dictionary to be converted to JSON
    """
    with open(fname, 'w') as outfile:
        json.dump(data, outfile, indent=2, separators=(',', ': '))

    return True
