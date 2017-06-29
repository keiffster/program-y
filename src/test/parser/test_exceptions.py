import unittest
import xml.etree.ElementTree as ET

from programy.parser.exceptions import ParserException
from programy.parser.exceptions import DuplicateGrammarException
from programy.parser.exceptions import MatcherException

class ExceptionTests(unittest.TestCase):

    def test_parser_exception_basic(self):
        exception = ParserException("message")
        self.assertEqual("message", exception.message)
        exception.filename = "test.xml"
        self.assertEqual("test.xml", exception.filename)
        self.assertEqual("message in [test.xml]", exception.format_message())

    def test_parser_exception_filename(self):
        exception = ParserException("message", filename="test.xml")
        self.assertEqual("message", exception.message)
        self.assertEqual("test.xml", exception.filename)
        self.assertEqual("message in [test.xml]", exception.format_message())

    def test_parser_exception_xml_as_string(self):
        element = ET.fromstring("<template />")
        exception = ParserException("message", filename="test.xml", xml_exception="xml_exception_error", xml_element=element)
        self.assertEqual("message", exception.message)
        self.assertEqual("test.xml", exception.filename)
        self.assertEqual("xml_exception_error", exception.xml_exception)
        self.assertEqual(element, exception._xml_element)
        self.assertEqual("message in [test.xml] : xml_exception_error", exception.format_message())

    def test_parser_exception_xml(self):
        element = ET.fromstring("<template />")
        xml_exception = ET.ParseError()
        xml_exception.position = []
        xml_exception.position.append(1)
        xml_exception.position.append(2)
        exception = ParserException("message", filename="test.xml", xml_exception=xml_exception, xml_element=element)
        self.assertEqual("message", exception.message)
        self.assertEqual("test.xml", exception.filename)
        self.assertEqual(xml_exception, exception.xml_exception)
        self.assertEqual(element, exception._xml_element)
        self.assertEqual("message in [test.xml] at [line(1), column(2)]", exception.format_message())

    def test_parser_exception_via_sets(self):
        element = ET.fromstring("<template />")
        xml_exception = ET.ParseError()
        xml_exception.position = []
        xml_exception.position.append(1)
        xml_exception.position.append(2)
        exception = ParserException("message", filename="test.xml")
        exception.xml_exception = xml_exception
        self.assertEqual(xml_exception, exception.xml_exception)
        exception.xml_element = element
        self.assertEqual(element, exception.xml_element)
        self.assertEqual("message", exception.message)
        self.assertEqual("test.xml", exception.filename)
        self.assertEqual(xml_exception, exception.xml_exception)
        self.assertEqual(element, exception._xml_element)
        self.assertEqual("message in [test.xml] at [line(1), column(2)]", exception.format_message())

    def test_duplicate_grammar_exception_basic(self):
        exception = DuplicateGrammarException("duplicate")
        self.assertEqual("duplicate", exception.message)
        self.assertEqual("duplicate", exception.format_message())

    def test_duplicate_grammar_exception_filename(self):
        exception = DuplicateGrammarException("message", filename="test.xml")
        self.assertEqual("message", exception.message)
        self.assertEqual("test.xml", exception.filename)
        self.assertEqual("message in [test.xml]", exception.format_message())

    def test_duplicate_grammar_exception_filename_set(self):
        exception = DuplicateGrammarException("duplicate")
        exception.filename = "test.xml"
        self.assertEqual("test.xml", exception.filename)
        self.assertEqual("duplicate in [test.xml]", exception.format_message())

    def test_duplicate_grammar_exception_xml(self):
        element = ET.fromstring("<template />")
        xml_exception = ET.ParseError()
        xml_exception.position = []
        xml_exception.position.append(1)
        xml_exception.position.append(2)
        exception = ParserException("message", filename="test.xml", xml_exception=xml_exception, xml_element=element)
        self.assertEqual("message", exception.message)
        self.assertEqual("test.xml", exception.filename)
        self.assertEqual(xml_exception, exception.xml_exception)
        self.assertEqual(element, exception._xml_element)
        self.assertEqual("message in [test.xml] at [line(1), column(2)]", exception.format_message())

    def test_duplicate_grammar_exception_via_sets(self):
        element = ET.fromstring("<template />")
        xml_exception = ET.ParseError()
        xml_exception.position = []
        xml_exception.position.append(1)
        xml_exception.position.append(2)
        exception = DuplicateGrammarException("message", filename="test.xml")
        exception.xml_exception = xml_exception
        self.assertEqual(xml_exception, exception.xml_exception)
        exception.xml_element = element
        self.assertEqual(element, exception.xml_element)
        self.assertEqual("message", exception.message)
        self.assertEqual("test.xml", exception.filename)
        self.assertEqual(xml_exception, exception.xml_exception)
        self.assertEqual(element, exception._xml_element)
        self.assertEqual("message in [test.xml] at [line(1), column(2)]", exception.format_message())

    def test_matcher_exception(self):
        exception = MatcherException("matcher")
        self.assertEqual("matcher", exception.message)
