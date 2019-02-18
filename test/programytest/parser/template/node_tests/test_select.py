import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.select import TemplateSelectNode

from programytest.parser.base import ParserTestsBaseClass

class MockTemplateSelectNode(TemplateSelectNode):
    def __init__(self):
        TemplateSelectNode.__init__(self)

    def resolve_to_string(self, context):
        raise Exception("This is an error")

class TemplateSelectNodeTests(ParserTestsBaseClass):

    def test_to_string(self):
        root = TemplateSelectNode()
        self.assertIsNotNone(root)
        self.assertEqual("[SELECT]", root.to_string())

    def test_to_xml(self):
        root = TemplateNode()
        node = TemplateSelectNode()
        root.append(node)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><select /></template>", xml_str)

    def test_node_default(self):
        root = TemplateNode()
        node = TemplateSelectNode()
        root.append(node)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)

    def test_node_exception_handling(self):
        root = TemplateNode()
        node = MockTemplateSelectNode()
        root.append(node)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)