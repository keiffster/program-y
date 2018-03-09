import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.word import TemplateWordNode
from programy.parser.template.nodes.id import TemplateIdNode
from programy.parser.template.nodes.srai import TemplateSRAINode

from programytest.parser.base import ParserTestsBaseClass

######################################################################################################################
#
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
