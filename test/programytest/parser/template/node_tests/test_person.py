import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.person import TemplatePersonNode
from programy.parser.template.nodes.word import TemplateWordNode

from programytest.parser.base import ParserTestsBaseClass


class MockTemplatePersonNode(TemplatePersonNode):
    def __init__(self):
        TemplatePersonNode.__init__(self)

    def resolve_to_string(self, context):
        raise Exception("This is an error")

class TemplatePersonNodeTests(ParserTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplatePersonNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)


    def test_to_xml(self):
        root = TemplateNode()
        node = TemplatePersonNode()
        root.append(node)
        node.append(TemplateWordNode("Test"))

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><person>Test</person></template>", xml_str)

    def test_node_exception_handling(self):
        root = TemplateNode()
        node = MockTemplatePersonNode()
        root.append(node)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)