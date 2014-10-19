""" DICOM Deidentifier Task Runner
A convenient way to execute tasks for a python package
"""
from invoke import run, task

from dicom_deidentify import soup, create_json

@task(help={"fname": "File name to save JSON output"})
def ac(fname=None):
    from dicom_deidentify import get_action_codes
    output = get_action_codes(soup())

    if fname is not None:
        print("Creating action codes ...")
        create_json(fname, output)
        print("{0} saved successfully!".format(fname))
    else:
        pretty(output)

@task(help={"fname": "File name to save JSON output"})
def di(fname=None):
    from dicom_deidentify import get_deidentify
    output = get_deidentify(soup())

    if fname is not None:
        print("Creating DICOM data element tag information ...")
        create_json(fname, output)
        print("{0} saved successfully!".format(fname))
    else:
        pretty(output)

def pretty(output):
    import pprint
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(output)