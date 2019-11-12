import xml.etree.ElementTree as ET  # pylint: disable=wrong-import-order

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.id import TemplateIdNode
from programy.parser.template.nodes.srai import TemplateSRAINode
from programy.parser.template.nodes.word import TemplateWordNode
from programy.utils.console.console import outputLog
from programytest.parser.base import ParserTestsBaseClass


class TemplateNodeBasicTests(ParserTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

    def test_node_children(self):
        node = TemplateNode()
        node.append(TemplateWordNode("Word1"))
        self.assertEqual(len(node.children), 1)
        node.append(TemplateWordNode("Word2"))
        self.assertEqual(len(node.children), 2)
        self.assertEqual("Word1 Word2", node.resolve_children_to_string(self._client_context))
        self.assertEqual("Word1 Word2", node.resolve(self._client_context))
        self.assertEqual("[NODE]", node.to_string())

    def test_to_xml_simple(self):
        node = TemplateNode()
        node.append(TemplateWordNode("Word1"))
        node.append(TemplateWordNode("Word2"))
        self.assertEqual("Word1 Word2", node.to_xml(self._client_context))

    def test_to_xml_composite(self):
        node = TemplateNode()
        node.append(TemplateWordNode("Word1"))
        node.append(TemplateIdNode())
        srai = TemplateSRAINode()
        srai.append(TemplateWordNode("Srai1"))
        node.append(srai)
        node.append(TemplateWordNode("Word2"))
        self.assertEqual("Word1 <id /> <srai>Srai1</srai> Word2", node.to_xml(self._client_context))

    def test_xml_tree_simple(self):
        node = TemplateNode()
        node.append(TemplateWordNode("Word1"))
        node.append(TemplateWordNode("Word2"))
        xml = node.xml_tree(self._client_context)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template>Word1 Word2</template>", xml_str)

    def test_xml_tree_simple_composite(self):
        node = TemplateNode()
        node.append(TemplateWordNode("Word1"))
        node.append(TemplateIdNode())
        srai = TemplateSRAINode()
        srai.append(TemplateWordNode("Srai1"))
        node.append(srai)
        node.append(TemplateWordNode("Word2"))
        xml = node.xml_tree(self._client_context)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template>Word1 <id /> <srai>Srai1</srai> Word2</template>", xml_str)

    def test_output_child(self):
        node = TemplateNode()
        node.append(TemplateWordNode("Word1"))
        node.append(TemplateIdNode())
        self.assertIsNotNone(node)
        node.append(TemplateWordNode("Word1"))

        node.output_child(node, "\t", "\n", print)
        node.output_child(node, "\t", "\n", outputLog)

    def test_parse_template_node(self):
        node = TemplateNode()
        pattern = ET.fromstring("<template>Test</template>")
        node.parse_template_node(self._client_context.brain.aiml_parser.template_parser, pattern)
        self.assertEquals(1, len(node.children))
        self.assertEquals("Test", node.children[0].word)

    def test_parse_template_node_empty(self):
        node = TemplateNode()
        pattern = ET.fromstring("<template></template>")
        node.parse_template_node(self._client_context.brain.aiml_parser.template_parser, pattern)
        self.assertEquals(0, len(node.children))
