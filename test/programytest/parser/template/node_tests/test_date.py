import xml.etree.ElementTree as ET

from programy.parser.exceptions import ParserException
from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.date import TemplateDateNode
from programy.parser.template.nodes.word import TemplateWordNode
from programytest.custom import CustomAssertions
from programytest.parser.base import ParserTestsBaseClass


class MockTemplateDateNode(TemplateDateNode):

    def __init__(self, date_format=None):
        TemplateDateNode.__init__(self)

    def resolve_to_string(self, context):
        raise Exception("This is a failure")


class MockTemplateDateNodeLocale(TemplateDateNode):

    def __init__(self, date_format=None):
        TemplateDateNode.__init__(self, locale="en_US")

    def _set_locate(self, client_context):
        raise Exception("This is a failure")


class TemplateDateNodeTests(ParserTestsBaseClass, CustomAssertions):

    DEFAULT_DATETIME_REGEX = "^.{3}\s*.{3}\s*\d{1,}\s\d{2}:\d{2}:\d{2}\s\d{4}"

    def test_get_set(self):
        node = TemplateDateNode()
        self.assertIsNotNone(node.date_format)
        self.assertIsInstance(node.date_format, TemplateNode)
        self.assertEquals("%c", node.date_format.word)
        self.assertIsNone(node.locale)

        node.date_format = "%c"
        node.locale = "en_US"

        self.assertIsInstance(node.date_format, TemplateNode)
        self.assertEquals("%c", node.date_format.word)
        self.assertIsInstance(node.locale, TemplateNode)
        self.assertEquals("en_US", node.locale.word)

        node.date_format = TemplateWordNode("%B")
        node.locale = TemplateWordNode("de_DE")

        self.assertIsInstance(node.date_format, TemplateNode)
        self.assertEquals("%B", node.date_format.word)
        self.assertIsInstance(node.locale, TemplateNode)
        self.assertEquals("de_DE", node.locale.word)

    def test_node_defaultformat(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateDateNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)
        self.assertRegex(root.resolve(self._client_context), TemplateDateNodeTests.DEFAULT_DATETIME_REGEX)

    def test_node_with_locale(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateDateNode(locale="en_US")
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)
        self.assertRegex(root.resolve(self._client_context), TemplateDateNodeTests.DEFAULT_DATETIME_REGEX)

    def test_node_customformat_constructor(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateDateNode(date_format="%c")
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)
        self.assertRegex(root.resolve(self._client_context), TemplateDateNodeTests.DEFAULT_DATETIME_REGEX)

    def test_node_customformat_parameter(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateDateNode()
        self.assertIsNotNone(node)
        node.date_format = "%c"
        root.append(node)

        self.assertEqual(len(root.children), 1)
        self.assertEqual("%c", node.date_format.word)
        self.assertRegex(root.resolve(self._client_context), TemplateDateNodeTests.DEFAULT_DATETIME_REGEX)

    def test_set_attrib_locate_as_string(self):
        node = TemplateDateNode()
        self.assertIsNotNone(node)
        node.set_attrib("locale", "en_US")
        self.assertEquals("en_US", node.locale.word)

    def test_set_attrib_locate_as_node(self):
        node = TemplateDateNode()
        self.assertIsNotNone(node)
        node.set_attrib("locale", TemplateWordNode("en_US"))
        self.assertEquals("en_US", node.locale.word)

    def test_set_attrib_unknown(self):
        node = TemplateDateNode()
        self.assertIsNotNone(node)
        with self.assertRaises(ParserException):
            node.set_attrib("unknown", TemplateWordNode("en_US"))

    def test_node_customformat_set_attrib(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateDateNode()
        self.assertIsNotNone(node)
        node.set_attrib("format", "%c")

        root.append(node)
        self.assertEqual(len(root.children), 1)
        self.assertRegex(root.resolve(self._client_context), TemplateDateNodeTests.DEFAULT_DATETIME_REGEX)

    def test_node_customformat_set_attrib_invalid(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateDateNode()
        self.assertIsNotNone(node)
        with self.assertRaises(ParserException):
            node.set_attrib("unknown", "%c")

    def test_to_xml_defaults(self):
        root = TemplateNode()
        node = TemplateDateNode()
        root.append(node)
        node.append(TemplateWordNode("Mon Sep 30 07:06:05 2013"))
        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><date format="%c">Mon Sep 30 07:06:05 2013</date></template>', xml_str)

    def test_to_xml_with_format(self):
        node = TemplateDateNode(date_format="%c")
        xml = node.to_xml(self._client_context)
        self.assertIsNotNone(xml)
        self.assertEquals('<date format="%c" ></date>', xml)

    def test_to_xml_with_locale(self):
        node = TemplateDateNode(locale="en_US")
        xml = node.to_xml(self._client_context)
        self.assertIsNotNone(xml)
        self.assertEquals('<date format="%c" locale="en_US"></date>', xml)

    def test_to_xml_with_format_and_locale(self):
        node = TemplateDateNode(date_format="%c", locale="en_US")
        xml = node.to_xml(self._client_context)
        self.assertIsNotNone(xml)
        self.assertEquals('<date format="%c" locale="en_US"></date>', xml)

    def test_node_exception_handling(self):
        node = MockTemplateDateNode()
        self.assertIsNotNone(node)

        with self.assertRaises(Exception):
            node.resolve_to_string(self._client_context)

    def test_node_locale_exception(self):
        node = MockTemplateDateNodeLocale()
        self.assertIsNotNone(node)

        self.assertEqual("", node.resolve_to_string(self._client_context))
