import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.formal import TemplateFormalNode
from programy.parser.template.nodes.word import TemplateWordNode

from test.parser.template.base import TemplateTestsBaseClass


class TemplateFormalNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateFormalNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        word = TemplateWordNode("This is a Sentence")
        node.append(word)

        self.assertEqual(root.resolve(self.bot, self.clientid), "This Is A Sentence")

    def test_to_xml(self):
        root = TemplateNode()
        node = TemplateFormalNode()
        root.append(node)
        node.append(TemplateWordNode("Test"))

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><formal>Test</formal></template>", xml_str)
