import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.first import TemplateFirstNode
from programy.parser.template.nodes.word import TemplateWordNode

from programytest.parser.base import ParserTestsBaseClass


class MockTemplateFirstNode(TemplateFirstNode):
    def __init__(self):
        TemplateFirstNode.__init__(self)

    def resolve_to_string(self, context):
        raise Exception("This is an error")


class TemplateFirstNodeTests(ParserTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateFirstNode()
        self.assertIsNotNone(node)

        root.append(node)
        word1 = TemplateWordNode("Word1")
        node.append(word1)
        word2 = TemplateWordNode("Word2")
        node.append(word2)
        word3 = TemplateWordNode("Word3")
        node.append(word3)

        self.assertEqual(root.resolve(self._client_context), "Word1")

    def test_to_xml(self):
        root = TemplateNode()
        node = TemplateFirstNode()
        root.append(node)
        word1 = TemplateWordNode("Word1")
        node.append(word1)
        word2 = TemplateWordNode("Word2")
        node.append(word2)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><first>Word1 Word2</first></template>", xml_str)

    def test_node_no_words(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateFirstNode()
        self.assertIsNotNone(node)

        root.append(node)

        self.assertEqual(root.resolve(self._client_context), "NIL")

    def test_to_xml_no_words(self):
        root = TemplateNode()
        node = TemplateFirstNode()
        root.append(node)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><first /></template>", xml_str)

    def test_node_exception_handling(self):
        root = TemplateNode()
        node = MockTemplateFirstNode()
        root.append(node)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)