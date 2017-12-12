CSV Tools
==========
A set of tools for converting to and from AIML from CSV

AIML to CSV
------------
Takes a single AIML file and converts to CSV file format
Useful for exporting to CSV, making bulk changes and then converting back to AIML

Usage:
python3 aiml_to_csv.py input_aiml output_csv

File Format:
Any AIML 1.x or 2.x compliant xml file

CSV to AIML
------------
Takes a CSV file conforming to the format described below and converts to AIML

Usage:
python3 csv_to_aiml.py input_csv output_aiml

File Format:
The format is made up for 4 columns
    - Pattern
    - Topic
    - That
    - Template

E.g.
    "HELLO","*","*","Hello there"
    "HELLO *","*","*","<srai>HELLO</srai>"
    "BYE","FAREWELL","*","See ya"
    "MAYBE","*","THINKING","OK THEN"
    "LA LA LA","SINGING","SING A SONG","Ouch that hurts"