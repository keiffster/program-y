import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.word import TemplateWordNode
from programy.parser.template.nodes.uppercase import TemplateUppercaseNode


from test.parser.template.base import TemplateTestsBaseClass


class TemplateUppercaseNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateUppercaseNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        word = TemplateWordNode("This is a Sentence")
        node.append(word)

        self.assertEqual(root.resolve(self.bot, self.clientid), "THIS IS A SENTENCE")

    def test_to_xml(self):
        root = TemplateNode()
        node = TemplateUppercaseNode()
        root.append(node)
        node.append(TemplateWordNode("Test"))

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><uppercase>Test</uppercase></template>", xml_str)

