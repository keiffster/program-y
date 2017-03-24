import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.word import TemplateWordNode
from programy.parser.template.nodes.condlistitem import TemplateConditionListItemNode

from test.parser.template.base import TemplateTestsBaseClass


class TemplateConditionListItemNodeTests(TemplateTestsBaseClass):

    def test_node_defaults(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateConditionListItemNode("item1")
        self.assertIsNotNone(node)
        self.assertEqual(node.name, "item1")
        self.assertIsNone(node.value)
        self.assertFalse(node.local)
        self.assertFalse(node.loop)
        self.assertTrue(node.is_default())

        root.append(node)
        self.assertEqual(len(root.children), 1)

    def test_node_value(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateConditionListItemNode("item1", value="value1")
        self.assertIsNotNone(node)
        self.assertEqual(node.name, "item1")
        self.assertEqual(node.value, "value1")
        self.assertFalse(node.local)
        self.assertFalse(node.loop)
        self.assertFalse(node.is_default())

        root.append(node)
        self.assertEqual(len(root.children), 1)

    def test_to_xml_global(self):
        root = TemplateNode()
        node = TemplateConditionListItemNode("name1", value=TemplateWordNode("value1"))
        node.append(TemplateWordNode("Hello"))
        root.append(node)

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><li name="name1"><value>value1</value>Hello</li></template>', xml_str)

    def test_to_xml_local(self):
        root = TemplateNode()
        node = TemplateConditionListItemNode("name1", value=TemplateWordNode("value1"), local=True)
        node.append(TemplateWordNode("Hello"))
        root.append(node)

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><li var="name1"><value>value1</value>Hello</li></template>', xml_str)

