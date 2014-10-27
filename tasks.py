""" DICOM Codify Task Runner
A convenient way to execute tasks for a python package
"""
import re
from invoke import run, task

from dicom_codify import soup, create_json

@task(help={"fname": "File name to save JSON output"})
def ac(fname=None):
    """ Action Codes """
    from dicom_codify import get_action_codes
    output = get_action_codes(soup())

    if fname is not None:
        print("Creating action codes ...")
        create_json(fname, output)
        print("{0} saved successfully!".format(fname))
    else:
        pretty(output)

@task(help={"fname": "File name to save JSON output"})
def di(fname=None):
    """ De-identifers """
    from dicom_codify import get_deidentify
    output = get_deidentify(soup())

    if fname is not None:
        print("Creating DICOM data element tag information ...")
        create_json(fname, output)
        print("{0} saved successfully!".format(fname))
    else:
        pretty(output)

@task(help={"fname": "File name to save JSON output"})
def ded(fname=None):
    """ Data Element Dictionary """
    from dicom_codify import get_data_element_dictionary
    asoup = soup(part=6)
    # table 6.1:
    # http://medical.nema.org/medical/dicom/current/output/html/part06.html#chapter_6
    e61 = asoup.find(attrs={ "id": re.compile("table_6-1") })
    # table 7.1:
    # http://medical.nema.org/medical/dicom/current/output/html/part06.html#chapter_7
    e71 = asoup.find(attrs={ "id": re.compile("table_7-1") })
    # table 8.1:
    # http://medical.nema.org/medical/dicom/current/output/html/part06.html#chapter_8
    e81 = asoup.find(attrs={ "id": re.compile("table_8-1") })

    output = get_data_element_dictionary(e61.parent.table) \
             + get_data_element_dictionary(e71.parent.table) \
             + get_data_element_dictionary(e71.parent.table)

    if fname is not None:
        print("Creating DICOM data element dictionary information ...")
        create_json(fname, output)
        print("{0} saved successfully!".format(fname))
    else:
        pretty(output)

def pretty(output):
    import pprint
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(output)