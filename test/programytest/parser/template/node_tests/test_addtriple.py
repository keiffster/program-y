import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.word import TemplateWordNode
from programy.parser.template.nodes.addtriple import TemplateAddTripleNode
from programytest.parser.base import ParserTestsBaseClass

class MockTemplateAddTripleNode(TemplateAddTripleNode):

    def __init__(self, subj=None, pred=None, obj=None):
        TemplateAddTripleNode.__init__(self, subj, pred, obj)

    def resolve_to_string(self, context):
        raise Exception ("This is a failure!")


class TemplateAddTripleNodeTests(ParserTestsBaseClass):

    def test_to_string(self):
        root = TemplateAddTripleNode()
        self.assertIsNotNone(root)
        self.assertEqual("[ADDTRIPLE]", root.to_string())

    def test_to_xml(self):
        root = TemplateNode()
        node = TemplateAddTripleNode(subj=TemplateWordNode("S"), pred=TemplateWordNode("P"), obj=TemplateWordNode("O"))
        root.append(node)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><addtriple><subj>S</subj><pred>P</pred><obj>O</obj></addtriple></template>", xml_str)

    def test_node(self):
        root = TemplateNode()
        node = TemplateAddTripleNode(subj=TemplateWordNode("S"), pred=TemplateWordNode("P"), obj=TemplateWordNode("O"))
        root.append(node)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)

    def test_exception_handling(self):

        root = TemplateNode()
        node = MockTemplateAddTripleNode(subj=TemplateWordNode("S"), pred=TemplateWordNode("P"), obj=TemplateWordNode("O"))
        root.append(node)

        with self.assertRaises(Exception):
            node.resolve_to_string(self._client_context)

        self.assertEqual("", root.resolve(self._client_context))

