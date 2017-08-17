import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.word import TemplateWordNode
from programy.parser.template.nodes.uniq import TemplateUniqNode
from programy.rdf.query import RDFQuery
from programy.rdf.unique import RDFUniqueStatement

from test.parser.template.base import TemplateTestsBaseClass


class TemplateUniqNodeTests(TemplateTestsBaseClass):

    def test_to_string(self):
        root = TemplateUniqNode()
        self.assertIsNotNone(root)
        self.assertEquals("UNIQ", root.to_string())

    def test_to_xml(self):
        root = TemplateNode()
        query = RDFQuery(subject=TemplateWordNode("S"), predicate=TemplateWordNode("P"), object=TemplateWordNode("O"))
        statement = RDFUniqueStatement(query)
        node = TemplateUniqNode(statement)
        root.append(node)

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><uniq><subj>S</subj><pred>P</pred><obj>O</obj></uniq></template>", xml_str)

    def test_node_defaults(self):
        root = TemplateNode()
        node = TemplateUniqNode()
        self.assertIsNotNone(node.query)
        self.assertIsInstance(node.query, RDFUniqueStatement)

        root.append(node)
        result = root.resolve(self.bot, self.clientid)
        self.assertIsNotNone(result)
        self.assertEquals("", result)

    def test_node_no_defaults(self):
        root = TemplateNode()
        query = RDFQuery(subject=TemplateWordNode("S"), predicate=TemplateWordNode("P"), object=TemplateWordNode("O"))
        statement = RDFUniqueStatement(query)
        node = TemplateUniqNode(statement)
        self.assertIsNotNone(node.query)
        self.assertIsInstance(node.query, RDFUniqueStatement)
        self.assertEquals(node.query, statement)

        root.append(node)
        result = root.resolve(self.bot, self.clientid)
        self.assertIsNotNone(result)
        self.assertEquals("", result)
