import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.word import TemplateWordNode
from programy.parser.template.nodes.deletetriple import TemplateDeleteTripleNode

from programytest.parser.base import ParserTestsBaseClass


class MockTemplateDeleteTripleNode(TemplateDeleteTripleNode):

    def __init__(self, subj, pred, obj):
        TemplateDeleteTripleNode.__init__(self, subj, pred, obj)

    def resolve_to_string(self, context):
        raise Exception("This is a failure")

class TemplateDeleteTripleNodeTests(ParserTestsBaseClass):

    def test_to_string(self):
        root = TemplateDeleteTripleNode()
        self.assertIsNotNone(root)
        self.assertEqual("[DELETETRIPLE]", root.to_string())

    def test_to_xml(self):
        root = TemplateNode()
        node = TemplateDeleteTripleNode(TemplateWordNode("S"), TemplateWordNode("P"), TemplateWordNode("O"))
        root.append(node)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><deletetriple><subj>S</subj><pred>P</pred><obj>O</obj></deletetriple></template>", xml_str)

    def test_node(self):
        root = TemplateNode()
        node = TemplateDeleteTripleNode(TemplateWordNode("S"), TemplateWordNode("P"), TemplateWordNode("O"))
        root.append(node)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)

    def test_node_exception_handling(self):
        root = TemplateNode()
        node = MockTemplateDeleteTripleNode(TemplateWordNode("S"), TemplateWordNode("P"), TemplateWordNode("O"))
        root.append(node)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)
