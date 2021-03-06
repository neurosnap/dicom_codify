DICOM Standard 2014 -- Codify
=============================

The goal of this project is to systematically attain the necessary information
from the DICOM standard.  This project attempts to scrape the HTML documents
used to describe the DICOM standard and "codify" them into JSON documents for
developers to use.

Data Element Dictionary
-----------------------

This section will download all the Data Elements described in the DICOM
Standard 2014.  `PS 3.6, Table 6-1`_, `PS 3.6, Table 7-1`_, and `PS 3.6, Table 8-1`_
describes the following data elements:

* Registry of DICOM Data Elements
* Registry of DICOM File Meta Elements
* Registry of DICOM Directory Structuring Elements

.. _PS 3.6, Table 6-1: http://medical.nema.org/medical/dicom/current/output/html/part06.html#chapter_6

.. _PS 3.6, Table 7-1: http://medical.nema.org/medical/dicom/current/output/html/part06.html#chapter_7

.. _PS 3.6, Table 8-1: http://medical.nema.org/medical/dicom/current/output/html/part06.html#chapter_8

De-identifier
-------------

The goal of this section is to attain the necessary information from the DICOM
standard to provide basic DICOM anonymization.  Basic anonymization is described
in `PS 3.15, E.1-1`_

.. _PS 3.15, E.1-1: http://medical.nema.org/medical/dicom/current/output/html/part15.html#table_E.1-1

This section will assist in properly anonymizing a DICOM file by creating
json files from the DICOM standard website for the data elements that need to
be replaced or removed to conform to basic DICOM anonymization.

How-To
======

The JSON files are already created, but if you want to create them again,
simply execute each python script:

.. code:: bash

    $ invoke ac --fname=action_codes.json
    $ invoke di --fname=deidentify.json
    $ invoke ded --fname=data_element_dictionary.json

Just want to print the outputs instead of saving them to a file?

.. code:: bash

    $ invoke ac
    $ invoke di
    $ invoke ded

I'm using nose for testing.  It has to download the HTML documents to perform
the tests, which is about 9 MB of data, so please be patient.

.. code:: bash

    $ nosetests

That's it!

Credits
=======

* Eric Bower