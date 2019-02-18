import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.word import TemplateWordNode
from programy.parser.template.nodes.uniq import TemplateUniqNode

from programytest.parser.base import ParserTestsBaseClass

class MockTemplateUniqNode(TemplateUniqNode):
    def __init__(self):
        TemplateUniqNode.__init__(self)

    def resolve_to_string(self, context):
        raise Exception("This is an error")

class TemplateUniqNodeTests(ParserTestsBaseClass):

    def test_to_string(self):
        root = TemplateUniqNode()
        self.assertIsNotNone(root)
        self.assertEqual("[UNIQ]", root.to_string())

    def test_to_xml(self):
        root = TemplateNode()
        node = TemplateUniqNode(subj=TemplateWordNode("S"), pred=TemplateWordNode("P"), obj=TemplateWordNode("O"))
        root.append(node)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><uniq><subj>S</subj><pred>P</pred><obj>O</obj></uniq></template>", xml_str)

    def test_node_defaults(self):
        root = TemplateNode()
        node = TemplateUniqNode()

        root.append(node)
        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)

    def test_node_no_defaults(self):
        root = TemplateNode()
        node = TemplateUniqNode(subj=TemplateWordNode("S"), pred=TemplateWordNode("P"), obj=TemplateWordNode("O"))

        root.append(node)
        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)

    def test_node_exception_handling(self):
        root = TemplateNode()
        node = MockTemplateUniqNode()
        root.append(node)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)