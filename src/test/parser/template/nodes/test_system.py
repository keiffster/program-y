import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.word import TemplateWordNode
from programy.parser.template.nodes.system import TemplateSystemNode

from test.parser.template.base import TemplateTestsBaseClass


class TemplateSystemNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateSystemNode()
        self.assertIsNotNone(node)
        node.append(TemplateWordNode('echo "Hello World"'))

        root.append(node)
        self.assertEqual(len(root.children), 1)

        response = root.resolve(self.bot, self.clientid)
        self.assertIsNotNone(response)
        self.assertEqual(response, "Hello World")

    def test_to_xml(self):
        root = TemplateNode()
        node = TemplateSystemNode()
        root.append(node)
        node.append(TemplateWordNode('echo "Hello World"'))

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><system>echo "Hello World"</system></template>', xml_str)
