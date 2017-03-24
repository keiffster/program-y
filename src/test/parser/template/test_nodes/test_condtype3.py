import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.word import TemplateWordNode
from programy.parser.template.nodes.condlistitem import TemplateConditionListItemNode
from programy.parser.template.nodes.condtype3 import TemplateType3ConditionNode

from test.parser.template.base import TemplateTestsBaseClass


class TemplateType3ConditionNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateType3ConditionNode()
        self.assertIsNotNone(node)

        cond1 = TemplateConditionListItemNode(name="name1", value=TemplateWordNode("value1") )
        cond1.append(TemplateWordNode("Word1"))
        node.append(cond1)

        cond2 = TemplateConditionListItemNode(name="name2", value=TemplateWordNode("value1"), local=True )
        cond2.append(TemplateWordNode("Word2"))
        node.append(cond2)

        cond3 = TemplateConditionListItemNode(name="name3")
        cond3.append(TemplateWordNode("Word3"))
        node.append(cond3)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        self.bot.conversation(self.clientid)._predicates['name1'] = "value1"

        result = root.resolve(self.bot, self.clientid)
        self.assertIsNotNone(result)
        self.assertEqual("Word1", result)

    # TODO Add unit tests for <loop /> construct

    def test_to_xml(self):
        root = TemplateNode()

        node = TemplateType3ConditionNode()
        self.assertIsNotNone(node)

        cond1 = TemplateConditionListItemNode(name="name1", value=TemplateWordNode("value1"))
        cond1.append(TemplateWordNode("Word1"))
        node.append(cond1)

        cond2 = TemplateConditionListItemNode(name="name2", value=TemplateWordNode("value1"), local=True )
        cond2.append(TemplateWordNode("Word2"))
        node.append(cond2)

        cond3 = TemplateConditionListItemNode(name="name3")
        cond3.append(TemplateWordNode("Word3"))
        node.append(cond3)

        root.append(node)

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><condition><li name="name1"><value>value1</value>Word1</li><li var="name2"><value>value1</value>Word2</li><li name="name3">Word3</li></condition></template>', xml_str)

