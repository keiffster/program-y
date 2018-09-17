import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.denormalise import TemplateDenormalizeNode
from programy.parser.template.nodes.word import TemplateWordNode

from programytest.parser.base import ParserTestsBaseClass
import re

class MockTemplateDenormalizeNode(TemplateDenormalizeNode):

    def __init__(self):
        TemplateDenormalizeNode.__init__(self)

    def resolve_to_string(self, context):
        raise Exception ("This is an error")


class TemplateDenormalizeNodeTests(ParserTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateDenormalizeNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        node.append(TemplateWordNode("keiff dot com"))
        self._client_context.brain.denormals.add_to_lookup(" DOT COM ", [re.compile("(^DOT COM | DOT COM | DOT COM$)", re.IGNORECASE), ".com"])

        self.assertEqual(root.resolve(self._client_context), "keiff.com")

    def test_to_xml(self):
        root = TemplateNode()
        node = TemplateDenormalizeNode()
        root.append(node)
        node.append(TemplateWordNode("Test"))

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><denormalize>Test</denormalize></template>", xml_str)

    def test_node_exception_handling(self):
        root = TemplateNode()
        node = MockTemplateDenormalizeNode()
        root.append(node)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)

    def test_node_exception_handling(self):
        root = TemplateNode()
        node = MockTemplateDenormalizeNode()
        root.append(node)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)
