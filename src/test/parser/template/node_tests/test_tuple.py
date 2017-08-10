import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.star import TemplateStarNode
from programy.parser.template.nodes.tuple import TemplateTupleNode

from test.parser.template.base import TemplateTestsBaseClass


class TemplateTupleNodeTests(TemplateTestsBaseClass):

    def test_to_string(self):
        root = TemplateTupleNode()
        self.assertIsNotNone(root)
        self.assertEquals("TUPLE", root.to_string())

    def test_to_xml(self):
        root = TemplateNode()
        node = TemplateTupleNode()
        root.append(node)
        node.append(TemplateStarNode())

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><tuple><star /></tuple></template>", xml_str)

    def test_node(self):
        root = TemplateNode()
        node = TemplateTupleNode()
        root.append(node)

        result = root.resolve(self.bot, self.clientid)
        self.assertIsNotNone(result)
        self.assertEquals("", result)
