import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.sentence import TemplateSentenceNode
from programy.parser.template.nodes.word import TemplateWordNode

from test.parser.template.base import TemplateTestsBaseClass


class TemplateSentenceNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateSentenceNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        word = TemplateWordNode("this is a sentence")
        node.append(word)

        self.assertEqual(root.resolve(self.bot, self.clientid), "This is a sentence")

    def test_to_xml(self):
        root = TemplateNode()
        node = TemplateSentenceNode()
        root.append(node)
        node.append(TemplateWordNode("Test"))

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><sentence>Test</sentence></template>", xml_str)

