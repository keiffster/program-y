import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.srai import TemplateSRAINode
from programy.parser.template.nodes.word import TemplateWordNode

from programytest.parser.base import ParserTestsBaseClass

class MockTemplateSRAINode(TemplateSRAINode):
    def __init__(self):
        TemplateSRAINode.__init__(self)

    def resolve_to_string(self, context):
        raise Exception("This is an error")

class TemplateSRAINodeTests(ParserTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateSRAINode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        node.append(TemplateWordNode("Hello"))
        self.assertEqual(len(node.children), 1)

        self._client_context.bot.response = "Hiya"
        self.assertEqual(root.resolve(self._client_context), "Hiya")

    def test_to_xml(self):
        root = TemplateNode()
        node = TemplateSRAINode()
        root.append(node)
        node.append(TemplateWordNode("Hello"))

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><srai>Hello</srai></template>", xml_str)

    def test_node_exception_handling(self):
        root = TemplateNode()
        node = MockTemplateSRAINode()
        root.append(node)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)