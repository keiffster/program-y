import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.select import Query
from programy.parser.template.nodes.select import TemplateSelectNode
from programy.parser.template.nodes.word import TemplateWordNode
from programytest.parser.base import ParserTestsBaseClass


class MockTemplateSelectNode(TemplateSelectNode):
    def __init__(self):
        TemplateSelectNode.__init__(self)

    def resolve_to_string(self, context):
        raise Exception("This is an error")


class TemplateSelectNodeTests(ParserTestsBaseClass):

    def test_init(self):
        root = TemplateSelectNode()
        self.assertEqual([], root.queries)
        self.assertEqual([], root.vars)
        self.assertEqual("<select></select>", root.to_xml(self._client_context))

    def test_init_with_queries(self):
        root = TemplateSelectNode(queries=[Query(TemplateWordNode("subj"), TemplateWordNode("pred"), TemplateWordNode("obj"))])
        self.assertEqual(1, len(root.queries))
        self.assertEqual(0, len(root.vars))
        self.assertEqual("<select><q><subj>subj</subj><pred>pred</pred><obj>obj</obj></q></select>", root.to_xml(self._client_context))

    def test_init_with_queries_and_vars(self):
        root = TemplateSelectNode(queries=[Query(TemplateWordNode("subj"), TemplateWordNode("pred"), TemplateWordNode("obj"))], variables=["?subj", "?pred"])
        self.assertEqual(1, len(root.queries))
        self.assertEqual(2, len(root.vars))
        self.assertEqual("<select><vars>?subj ?pred</vars><q><subj>subj</subj><pred>pred</pred><obj>obj</obj></q></select>", root.to_xml(self._client_context))

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
