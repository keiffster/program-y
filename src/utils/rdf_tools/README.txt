RDF Formatter
=============

A simple utility to reformat an RDF knowledge file. I've found a number of ALice2 RDF files which have entity data
scattered across the file as new predicates are added to the end of files. This utility therefore builds all entities
in memory first and then re-writes the file so that all subject -> predicate -> entity values are in the appropriate
order

Usage:
python3 rdf_formatter.py rdf_file

    rdf_file - Name of an rdf file to reformat
