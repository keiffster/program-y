import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.person2 import TemplatePerson2Node
from programy.parser.template.nodes.word import TemplateWordNode

from test.parser.template.base import TemplateTestsBaseClass

class TemplatePerson2NodeTests(TemplateTestsBaseClass):

    def test_node(self):

        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplatePerson2Node()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        node.append(TemplateWordNode("me"))
        self.bot.brain.person2s.process_splits(["me","him or her"])

        self.assertEqual(root.resolve(self.bot, self.clientid), "him or her")

    def test_to_xml(self):
        root = TemplateNode()
        node = TemplatePerson2Node()
        root.append(node)
        node.append(TemplateWordNode("Test"))

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><person2>Test</person2></template>", xml_str)


#