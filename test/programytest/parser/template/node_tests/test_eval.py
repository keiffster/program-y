import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.eval import TemplateEvalNode
from programy.parser.template.nodes.word import TemplateWordNode

from programytest.parser.base import ParserTestsBaseClass

class MockTemplateEvalNode(TemplateEvalNode):

    def __init__(self):
        TemplateEvalNode.__init__(self)

    def resolve_to_string(self, context):
        raise Exception ("This is an error")

class TemplateEvalNodeTests(ParserTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)

        eval = TemplateEvalNode()
        root.append(eval)

        eval.append(TemplateWordNode("hello"))

        self.assertEqual(len(root.children), 1)

        resolved = root.resolve(self._client_context)
        self.assertIsNotNone(resolved)
        self.assertEqual("hello", resolved)

    def test_to_xml(self):
        root = TemplateNode()
        node = TemplateEvalNode()
        root.append(node)
        node.append(TemplateWordNode("Test"))

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><eval>Test</eval></template>", xml_str)

    def test_node_exception_handling(self):
        root = TemplateNode()
        node = MockTemplateEvalNode()
        root.append(node)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)
