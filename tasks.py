""" DICOM Deidentifier Task Runner
A convenient way to execute tasks for a python package
"""
from invoke import run, task

from dicom_deidentify import soup, create_json

@task(help={"fname": "File name to save JSON output"})
def ac(fname):
    from dicom_deidentify import get_action_codes
    create_json(fname, get_action_codes(soup()))

@task(help={"fname": "File name to save JSON output"})
def di(fname):
    from dicom_deidentify import get_deidentify
    create_json(fname, get_deidentify(soup()))