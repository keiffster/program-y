from programy.utils.parsing.linenumxml import LineNumberingParser
import xml.etree.ElementTree as ET

import os
import unittest

#############################################################################
#

class LineNumberingParserTests(unittest.TestCase):

    def test_broken_xml(self):
        with self.assertRaises(ET.ParseError) as raised:
            ET.parse(os.path.dirname(__file__)+ os.sep + "broken.xml", parser=LineNumberingParser())
        self.assertEqual(22, raised.exception.position[0])
        self.assertEqual(10, raised.exception.position[1])

    def test_working_xml(self):
        tree = ET.parse(os.path.dirname(__file__)+ os.sep + "working.xml", parser=LineNumberingParser())
        aiml = tree.getroot()
        self.assertEqual(28, aiml._end_line_number)
        self.assertEqual(0, aiml._end_column_number)

        patterns = aiml.findall('category')
        self.assertEqual(1, len(patterns))
        self.assertEqual(26, patterns[0]._end_line_number)
        self.assertEqual(4, patterns[0]._end_column_number)
