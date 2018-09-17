import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.implode import TemplateImplodeNode
from programy.parser.template.nodes.word import TemplateWordNode

from programytest.parser.base import ParserTestsBaseClass

class MockTemplateImplodeNode(TemplateImplodeNode):
    def __init__(self):
        TemplateImplodeNode.__init__(self)

    def resolve_to_string(self, context):
        raise Exception("This is an error")

class TemplateImplodeNodeTests(ParserTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateImplodeNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        node.append(TemplateWordNode("H e l l o W o r l d"))
        self.assertEqual(root.resolve(self._client_context), "HelloWorld")

    def test_to_xml(self):
        root = TemplateNode()
        node = TemplateImplodeNode()
        root.append(node)
        node.append(TemplateWordNode("Test"))

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><implode>Test</implode></template>", xml_str)

    def test_node_exception_handling(self):
        root = TemplateNode()
        node = MockTemplateImplodeNode()
        root.append(node)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)
