import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.oob import TemplateOOBNode
from programy.parser.template.nodes.word import TemplateWordNode

from programytest.parser.base import ParserTestsBaseClass

class MockTemplateOOBNode(TemplateOOBNode):
    def __init__(self):
        TemplateOOBNode.__init__(self)

    def resolve_to_string(self, context):
        raise Exception("This is an error")

class TemplateOOBNodeTests(ParserTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)

        oob = TemplateOOBNode()
        root.append(oob)

        oob.append(TemplateWordNode("hello"))

        self.assertEqual(len(root.children), 1)

        resolved = root.resolve(self._client_context)
        self.assertIsNotNone(resolved)
        self.assertEqual("<oob>hello</oob>", resolved)

    def test_to_xml(self):
        root = TemplateNode()
        node = TemplateOOBNode()
        root.append(node)
        node.append(TemplateWordNode("Test"))

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><oob>Test</oob></template>", xml_str)

    def test_node_exception_handling(self):
        root = TemplateNode()
        node = MockTemplateOOBNode()
        root.append(node)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)