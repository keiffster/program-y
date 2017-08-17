import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.select import TemplateSelectNode
from programy.rdf.select import RDFSelectStatement

from test.parser.template.base import TemplateTestsBaseClass


class TemplateSelectNodeTests(TemplateTestsBaseClass):

    def test_to_string(self):
        root = TemplateSelectNode()
        self.assertIsNotNone(root)
        self.assertEquals("SELECT", root.to_string())

    def test_to_xml(self):
        root = TemplateNode()
        node = TemplateSelectNode()
        root.append(node)

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><select><vars /></select></template>", xml_str)

    def test_node_default(self):
        root = TemplateNode()
        node = TemplateSelectNode()
        self.assertIsNotNone(node.query)
        self.assertIsInstance(node.query, RDFSelectStatement)
        root.append(node)

        result = root.resolve(self.bot, self.clientid)
        self.assertIsNotNone(result)
        self.assertEquals("", result)
