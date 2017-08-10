import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.word import TemplateWordNode
from programy.parser.template.nodes.uniq import TemplateUniqNode

from test.parser.template.base import TemplateTestsBaseClass


class TemplateUniqNodeTests(TemplateTestsBaseClass):

    def test_to_string(self):
        root = TemplateUniqNode()
        self.assertIsNotNone(root)
        self.assertEquals("UNIQ", root.to_string())

    def test_to_xml(self):
        root = TemplateNode()
        node = TemplateUniqNode(subject=TemplateWordNode("S"), predicate=TemplateWordNode("P"), obj=TemplateWordNode("O"))
        root.append(node)

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><uniq><subj>S</subj><pred>P</pred><obj>O</obj></uniq></template>", xml_str)

    def test_node(self):
        root = TemplateNode()
        node = TemplateUniqNode(subject=TemplateWordNode("S"), predicate=TemplateWordNode("P"), obj=TemplateWordNode("O"))
        root.append(node)

        result = root.resolve(self.bot, self.clientid)
        self.assertIsNotNone(result)
        self.assertEquals("", result)
