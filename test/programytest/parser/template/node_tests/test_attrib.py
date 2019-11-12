import xml.etree.ElementTree as ET

from programy.parser.template.nodes.attrib import TemplateAttribNode
from programytest.parser.base import ParserTestsBaseClass


class TestTemplateAttribNode(TemplateAttribNode):

    def __init__(self):
        TemplateAttribNode.__init__(self)
        self.pairs = {}

    def set_attrib(self, attrib_name: str, attrib_value):
        self.pairs[attrib_name] = attrib_value


class TemplateAttribNodeTests(ParserTestsBaseClass):

    def test_node(self):
        attrib = TemplateAttribNode()
        self.assertIsNotNone(attrib)
        with self.assertRaises(Exception):
            attrib.set_attrib("Something", "Other")

    def test_parse_node_with_attrib_no_default_value(self):
        attrib = TestTemplateAttribNode()

        graph = self._client_context.brain.aiml_parser.template_parser
        expression = ET.fromstring('<node name="test">Test</node>')
        attrib_name = "name"

        attrib._parse_node_with_attrib(graph, expression, attrib_name)

        self.assertTrue(attrib_name in attrib.pairs)
        self.assertEquals("test", attrib.pairs[attrib_name].word)

    def test_parse_node_with_child_attrib_no_default_value(self):
        attrib = TestTemplateAttribNode()

        graph = self._client_context.brain.aiml_parser.template_parser
        expression = ET.fromstring('<node><name>test</name> Test</node>')
        attrib_name = "name"

        attrib._parse_node_with_attrib(graph, expression, attrib_name)

        self.assertTrue(attrib_name in attrib.pairs)
        self.assertEquals("test", attrib.pairs[attrib_name].children[0].word)

    def test_parse_node_with_no_attrib_no_default_value(self):
        attrib = TestTemplateAttribNode()

        graph = self._client_context.brain.aiml_parser.template_parser
        expression = ET.fromstring('<node>Test</node>')
        attrib_name = "name"

        attrib._parse_node_with_attrib(graph, expression, attrib_name)

        self.assertFalse(attrib_name in attrib.pairs)

    def test_parse_node_with_no_attrib_default_value(self):
        attrib = TestTemplateAttribNode()

        graph = self._client_context.brain.aiml_parser.template_parser
        expression = ET.fromstring('<node>Test</node>')
        attrib_name = "name"

        attrib._parse_node_with_attrib(graph, expression, attrib_name, default_value="test")

        self.assertTrue(attrib_name in attrib.pairs)

    def test_parse_node_with_diff_attrib_no_default_value(self):
        attrib = TestTemplateAttribNode()

        graph = self._client_context.brain.aiml_parser.template_parser
        expression = ET.fromstring('<node nameX="test">Test</node>')
        attrib_name = "name"

        attrib._parse_node_with_attrib(graph, expression, attrib_name)

        self.assertFalse(attrib_name in attrib.pairs)

    def test_parse_node_with_diff_child_attrib_no_default_value(self):
        attrib = TestTemplateAttribNode()

        graph = self._client_context.brain.aiml_parser.template_parser
        expression = ET.fromstring('<node><nameX>test</nameX>Test</node>')
        attrib_name = "name"

        attrib._parse_node_with_attrib(graph, expression, attrib_name)

        self.assertFalse(attrib_name in attrib.pairs)

    def test_parse_node_with_diff_child_attrib_default_value(self):
        attrib = TestTemplateAttribNode()

        graph = self._client_context.brain.aiml_parser.template_parser
        expression = ET.fromstring('<node><nameX>test</nameX>Test</node>')
        attrib_name = "name"

        attrib._parse_node_with_attrib(graph, expression, attrib_name, default_value="test2")

        self.assertTrue(attrib_name in attrib.pairs)
        self.assertEquals("test2", attrib.pairs[attrib_name].word)

    def test_parse_node_with_attribs_no_default_value(self):
        attrib = TestTemplateAttribNode()

        graph = self._client_context.brain.aiml_parser.template_parser
        expression = ET.fromstring('<node name1="test1" name2="test2">Test</node>')

        attrib._parse_node_with_attribs(graph, expression, [["name1", None], ["name2", None]])

        self.assertTrue("name1" in attrib.pairs)
        self.assertEquals("test1", attrib.pairs["name1"].word)
        self.assertTrue("name2" in attrib.pairs)
        self.assertEquals("test2", attrib.pairs["name2"].word)

    def test_parse_node_with_child_attribs_no_default_value(self):
        attrib = TestTemplateAttribNode()

        graph = self._client_context.brain.aiml_parser.template_parser
        expression = ET.fromstring('<node> <name1>test1</name1> <name2>test2</name2> Test</node>')

        attrib._parse_node_with_attribs(graph, expression, [["name1", None], ["name2", None]])

        self.assertTrue("name1" in attrib.pairs)
        self.assertEquals("test1", attrib.pairs["name1"].children[0].word)
        self.assertTrue("name2" in attrib.pairs)
        self.assertEquals("test2", attrib.pairs["name2"].children[0].word)

    def test_parse_node_with_no_attribs_no_default_values(self):
        attrib = TestTemplateAttribNode()

        graph = self._client_context.brain.aiml_parser.template_parser
        expression = ET.fromstring('<node>Test</node>')

        attrib._parse_node_with_attribs(graph, expression, [])

        self.assertFalse("name1" in attrib.pairs)
        self.assertFalse("name2" in attrib.pairs)

    def test_parse_node_with_attribs_default_values(self):
        attrib = TestTemplateAttribNode()

        graph = self._client_context.brain.aiml_parser.template_parser
        expression = ET.fromstring('<node>Test</node>')

        attrib._parse_node_with_attribs(graph, expression, [["name1", "test1"], ["name2", "test2"]])

        self.assertTrue("name1" in attrib.pairs)
        self.assertEquals("test1", attrib.pairs["name1"].word)
        self.assertTrue("name2" in attrib.pairs)
        self.assertEquals("test2", attrib.pairs["name2"].word)

    def test_parse_node_with_child_attribs_with_default_value(self):
        attrib = TestTemplateAttribNode()

        graph = self._client_context.brain.aiml_parser.template_parser
        expression = ET.fromstring('<node> <name1X>test1</name1X> <name2Y>test2</name2Y> Test</node>')

        attrib._parse_node_with_attribs(graph, expression, [["name1", "test1"], ["name2", "test2"]])

        self.assertTrue("name1" in attrib.pairs)
        self.assertEquals("test1", attrib.pairs["name1"].word)
        self.assertTrue("name2" in attrib.pairs)
        self.assertEquals("test2", attrib.pairs["name2"].word)
