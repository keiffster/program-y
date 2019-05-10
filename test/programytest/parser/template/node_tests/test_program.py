import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.program import TemplateProgramNode


from programytest.parser.base import ParserTestsBaseClass


class MockTemplateProgramNode(TemplateProgramNode):
    def __init__(self):
        TemplateProgramNode.__init__(self)

    def resolve_to_string(self, context):
        raise Exception("This is an error")

class TemplateProgramNodeTests(ParserTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateProgramNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        self._client_context.brain.properties.add_property("fullname", "testbot")
        self._client_context.brain.properties.add_property("version", "1.0.0")

        self.assertEqual(root.resolve(self._client_context), "testbot 1.0.0")

    def test_to_xml(self):
        root = TemplateNode()
        node = TemplateProgramNode()
        root.append(node)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><program /></template>", xml_str)

    def test_node_exception_handling(self):
        root = TemplateNode()
        node = MockTemplateProgramNode()
        root.append(node)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)