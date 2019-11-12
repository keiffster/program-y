import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.condition import TemplateConditionListItemNode
from programy.parser.template.nodes.condition import TemplateConditionNode
from programy.parser.template.nodes.word import TemplateWordNode
from programytest.parser.base import ParserTestsBaseClass


class TemplateConditionType3NodeTests(ParserTestsBaseClass):

    def test_type3_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateConditionNode(condition_type=3)
        self.assertIsNotNone(node)

        cond1 = TemplateConditionListItemNode(name="name1", value=TemplateWordNode("value1"), var_type=TemplateConditionNode.GLOBAL )
        cond1.append(TemplateWordNode("Word1"))
        node.append(cond1)

        cond2 = TemplateConditionListItemNode(name="name2", value=TemplateWordNode("value1"), var_type=TemplateConditionNode.LOCAL )
        cond2.append(TemplateWordNode("Word2"))
        node.append(cond2)

        cond3 = TemplateConditionListItemNode(name="name3", value=TemplateWordNode("value3"), var_type=TemplateConditionNode.BOT )
        cond3.append(TemplateWordNode("Word3"))
        node.append(cond3)

        cond3 = TemplateConditionListItemNode(name="name3")
        cond3.append(TemplateWordNode("Word3"))
        node.append(cond3)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        self._client_context.bot.get_conversation(self._client_context).set_property('name1', "value1")
        self._client_context.brain.properties.add_property('name3', "value3")

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("Word1", result)

        self._client_context.bot.get_conversation(self._client_context).set_property('name1', "value2")

        self._client_context.brain.properties.add_property('name3', "value3")
        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("Word3", result)

    def test_type3_to_xml(self):
        root = TemplateNode()

        node = TemplateConditionNode(condition_type=3)
        self.assertIsNotNone(node)

        cond1 = TemplateConditionListItemNode(name="name1", value=TemplateWordNode("value1"), var_type=TemplateConditionNode.GLOBAL)
        cond1.append(TemplateWordNode("Word1"))
        node.append(cond1)

        cond2 = TemplateConditionListItemNode(name="name2", value=TemplateWordNode("value1"), var_type=TemplateConditionNode.LOCAL )
        cond2.append(TemplateWordNode("Word2"))
        node.append(cond2)

        cond3 = TemplateConditionListItemNode(name="name3", value=TemplateWordNode("value3"), var_type=TemplateConditionNode.BOT )
        cond3.append(TemplateWordNode("Word3"))
        node.append(cond3)

        cond4 = TemplateConditionListItemNode(name="name4")
        cond4.append(TemplateWordNode("Word4"))
        node.append(cond4)

        root.append(node)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><condition><li name="name1"><value>value1</value>Word1</li> <li var="name2"><value>value1</value>Word2</li> <li bot="name3"><value>value3</value>Word3</li> <li name="name4">Word4</li></condition></template>', xml_str)

