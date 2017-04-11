import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.map import TemplateMapNode
from programy.parser.template.nodes.word import TemplateWordNode

from test.parser.template.base import TemplateTestsBaseClass


class TemplateMapNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateMapNode()
        node.name = TemplateWordNode("COLOURS")
        node.append(TemplateWordNode("BLACK"))
        root.append(node)
        self.assertEqual(len(root.children), 1)

        self.bot.brain.maps._maps['COLOURS'] = {'BLACK': 'WHITE'}

        result = root.resolve(self.bot, self.clientid)
        self.assertIsNotNone(result)
        self.assertEqual("WHITE", result)

    def test_to_xml(self):
        root = TemplateNode()
        node = TemplateMapNode()
        node.name = TemplateWordNode("COLOURS")
        node.append(TemplateWordNode("BLACK"))
        root.append(node)

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><map name="COLOURS">BLACK</map></template>', xml_str)

