import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.person2 import TemplatePerson2Node
from programy.parser.template.nodes.word import TemplateWordNode

from programytest.parser.base import ParserTestsBaseClass


class MockTemplatePerson2Node(TemplatePerson2Node):
    def __init__(self):
        TemplatePerson2Node.__init__(self)

    def resolve_to_string(self, context):
        raise Exception("This is an error")

class TemplatePerson2NodeTests(ParserTestsBaseClass):

    def test_node(self):

        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplatePerson2Node()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)


    def test_to_xml(self):
        root = TemplateNode()
        node = TemplatePerson2Node()
        root.append(node)
        node.append(TemplateWordNode("Test"))

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><person2>Test</person2></template>", xml_str)

    def test_node_exception_handling(self):
        root = TemplateNode()
        node = MockTemplatePerson2Node()
        root.append(node)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)
#