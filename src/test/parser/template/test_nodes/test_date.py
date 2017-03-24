import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.date import TemplateDateNode
from programy.parser.template.nodes.word import TemplateWordNode

from test.parser.template.base import TemplateTestsBaseClass


class TemplateDateNodeTests(TemplateTestsBaseClass):

    DEFAULT_DATETIME_REGEX = "^.{3}\s*.{3}\s*\d{1,}\s\d{2}:\d{2}:\d{2}\s\d{4}"

    def test_node_defaultformat(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateDateNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)
        self.assertRegex(root.resolve(self.bot, self.clientid), TemplateDateNodeTests.DEFAULT_DATETIME_REGEX)

    def test_node_customformat(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateDateNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)
        self.assertRegex(root.resolve(self.bot, self.clientid), TemplateDateNodeTests.DEFAULT_DATETIME_REGEX)

    def test_to_xml_defaults(self):
        root = TemplateNode()
        node = TemplateDateNode()
        root.append(node)
        node.append(TemplateWordNode("Mon Sep 30 07:06:05 2013"))
        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><date format="%c">Mon Sep 30 07:06:05 2013</date></template>', xml_str)
