import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.lowercase import TemplateLowercaseNode
from programy.parser.template.nodes.word import TemplateWordNode

from programytest.parser.base import ParserTestsBaseClass


class MockTemplateLowercaseNode(TemplateLowercaseNode):
    def __init__(self):
        TemplateLowercaseNode.__init__(self)

    def resolve_to_string(self, context):
        raise Exception("This is an error")

class TemplateLowercaseNodeTests(ParserTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateLowercaseNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        word = TemplateWordNode("This is a Sentence")
        node.append(word)

        self.assertEqual(root.resolve(self._client_context), "this is a sentence")

    def test_to_xml(self):
        root = TemplateNode()
        node = TemplateLowercaseNode()
        root.append(node)
        node.append(TemplateWordNode("Test"))

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><lowercase>Test</lowercase></template>", xml_str)

    def test_node_exception_handling(self):
        root = TemplateNode()
        node = MockTemplateLowercaseNode()
        root.append(node)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)