DICOM Standard 2014 -- De-Identifier Codeified
==============================================

The goal of this project is to attain the necessary information from the DICOM
standard to provide basic DICOM anonymization.  Basic anonymization is described
in .. _PS 3.15, E.1-1: http://medical.nema.org/medical/dicom/current/output/html/part15.html#table_E.1-1

This project will assist in properly anonymizing a DICOM file by creating
json files from the DICOM standard website for the data elements that need to
be replaced or removed to conform to basic DICOM anonymization.

How-To
======

The JSON files are already created, but if you want to create them again,
simply execute each python script:

.. code:: bash

    $ invoke ac action_codes.json
    $ invoke di deidentify.json

That's it!

Credits
=======

* Eric Bower