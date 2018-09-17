import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.bot import TemplateBotNode
from programy.parser.template.nodes.word import TemplateWordNode

from programytest.parser.base import ParserTestsBaseClass

class MockTemplateBotNode(TemplateBotNode):

    def __init__(self):
        TemplateBotNode.__init__(self)

    def resolve_to_string(self, context):
        raise Exception("This is a failure")

class TemplateBotNodeTests(ParserTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateBotNode()
        self.assertIsNotNone(node)
        node.name = TemplateWordNode("location")
        root.append(node)
        self.assertEqual(len(root.children), 1)

        self._client_context.brain.properties.add_property("location", "Scotland")

        result = node.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("Scotland", result)

    def test_node_no_value(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateBotNode()
        self.assertIsNotNone(node)
        node.name = TemplateWordNode("location")
        root.append(node)
        self.assertEqual(len(root.children), 1)

        self._client_context.brain.properties.add_property("default-property", "unknown")

        result = node.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("unknown", result)

    def test_to_xml(self):
        root = TemplateNode()
        node = TemplateBotNode()
        node.name = TemplateWordNode("name")
        root.append(node)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><bot name="name" /></template>', xml_str)

    def test_node_exception_handling(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = MockTemplateBotNode()
        self.assertIsNotNone(node)
        node.name = TemplateWordNode("location")
        root.append(node)
        self.assertEqual(len(root.children), 1)

        self._client_context.brain.properties.add_property("location", "Scotland")

        with self.assertRaises(Exception):
            node.resolve_to_string(self._client_context)

        self.assertEqual("", root.resolve(self._client_context))

