
AIML Generator
===============

Generates AIML files from CSV definitions, either

Specifiy a directory where all csv files are location

python3 generator.py --directory ./input --output ./output

Or specify a single csv file with

python3 generator.py --file ./input --output ./output

For either option specify the location where the AIML file(s) will be generated

CSV File Format
================

The file format is simple, for each line specify first the template response, and then a single word in each
csv column for each word of the pattern, e.g

HELLO, HI, THERE

Will create

<category>
    <pattern>HI THERE</pattern>
    <template>HELLO</pattern>
</category>

The Template column can contain any valud AIML template response, including AIML tags such as srai, e.g

<srai>HELLO</srai>, HI, THERE

Will create

<category>
    <pattern>HI THERE</pattern>
    <template><srai>HELLO</srai></pattern>
</category>

The pattern columns have a number of options which affect how much AIML is created

WORD            - A single word
(WORD)          - An optional word
WORD1|WORD2     - A list of words seperated by the bar |

The generator will create each variant of AIML category by applying the basic rules given above.

Optional Words
--------------
The generator will create variants of the sentence which both include and exclude the word, e.g

goodbye, see, you, (mate)

Creates

<category>
    <pattern>SO YOU</pattern>
    <template><srai>goodbye</srai></pattern>
</category>
<category>
    <pattern>SO YOU MATE</pattern>
    <template><srai>goodbye</srai></pattern>
</category>

Word List
---------
Creates each combination of the sentence with each individual word

<srai>I AM TEST</srai>, I, am, a|the, test|tester

Creates

<category>
    <pattern>I am a test</pattern
    <template><srai>I AM TEST</srai></template>
</category>
<category>
    <pattern>I am the test</pattern
    <template><srai>I AM TEST</srai></template>
</category>
<category>
    <pattern>I am a tester</pattern
    <template><srai>I AM TEST</srai></template>
</category>
<category>
    <pattern>I am the tester</pattern
    <template><srai>I AM TEST</srai></template>
</category>

