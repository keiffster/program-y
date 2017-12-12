RDF Lister
==========
Creates a single CSV file from all the rdf files found in the directory ( and sub directories ) specified
All entries are sorted by Subject, then predicate, then entity value.

This tool is useful to debugging RDF to make sure all RDF entities are in the same file and located next to each
other

Usage:
    python3 rdf_lister rdf_dir csv_file