import unittest
import xml.etree.ElementTree as ET

from programy.parser.exceptions import ParserException
from programy.parser.exceptions import DuplicateGrammarException
from programy.parser.exceptions import MatcherException

class ExceptionTests(unittest.TestCase):

    def test_parser_exception(self):
        exception = ParserException("message")
        self.assertEqual("message", exception.message)
        exception.filename = "test.xml"
        self.assertEqual("test.xml", exception.filename)

        exception = ParserException("message", filename="test.xml")
        self.assertEqual("message", exception.message)
        self.assertEqual("test.xml", exception.filename)

        element = ET.fromstring("<template />")
        xml_exception = ET.ParseError()
        exception = ParserException("message", filename="test.xml", xml_exception=xml_exception, xml_element=element)
        self.assertEqual("message", exception.message)
        self.assertEqual("test.xml", exception.filename)
        self.assertEqual(xml_exception, exception.xml_exception)
        self.assertEqual(element, exception._xml_element)

    def test_duplicate_grammar_exception(self):
        exception = DuplicateGrammarException("duplicate")
        self.assertEqual("duplicate", exception.message)

        exception.filename = "test.xml"
        self.assertEqual("test.xml", exception.filename)

        exception = ParserException("message", filename="test.xml")
        self.assertEqual("message", exception.message)
        self.assertEqual("test.xml", exception.filename)

        element = ET.fromstring("<template />")
        xml_exception = ET.ParseError()
        exception = ParserException("message", filename="test.xml", xml_exception=xml_exception, xml_element=element)
        self.assertEqual("message", exception.message)
        self.assertEqual("test.xml", exception.filename)
        self.assertEqual(xml_exception, exception.xml_exception)
        self.assertEqual(element, exception._xml_element)

    def test_matcher_exception(self):
        exception = MatcherException("matcher")
        self.assertEqual("matcher", exception.message)
