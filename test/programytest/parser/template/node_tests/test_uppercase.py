import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.word import TemplateWordNode
from programy.parser.template.nodes.uppercase import TemplateUppercaseNode

from programytest.parser.base import ParserTestsBaseClass


class MockTemplateUppercaseNode(TemplateUppercaseNode):
    def __init__(self):
        TemplateUppercaseNode.__init__(self)

    def resolve(self, context):
        raise Exception("This is a failure!")

class TemplateUppercaseNodeTests(ParserTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateUppercaseNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        word = TemplateWordNode("This is a Sentence")
        node.append(word)

        self.assertEqual(root.resolve(self._client_context), "THIS IS A SENTENCE")

    def test_to_xml(self):
        root = TemplateNode()
        node = TemplateUppercaseNode()
        root.append(node)
        node.append(TemplateWordNode("Test"))

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><uppercase>Test</uppercase></template>", xml_str)

    def test_exception_handling(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = MockTemplateUppercaseNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        word = TemplateWordNode("This is a Sentence")
        node.append(word)

        self.assertEqual(root.resolve(self._client_context), "")

    def test_node_exception_handling(self):
        root = TemplateNode()
        node = MockTemplateUppercaseNode()
        root.append(node)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)