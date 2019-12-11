from unittest.mock import patch
import xml.etree.ElementTree as ET
from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.condition import TemplateConditionListItemNode
from programy.parser.template.nodes.condition import TemplateConditionNode
from programy.parser.template.nodes.condition import TemplateConditionVariable
from programy.parser.template.nodes.word import TemplateWordNode
from programytest.parser.base import ParserTestsBaseClass


class MyLoopTemplateConditionNode(TemplateConditionNode):

    def __init__(self, name=None, value=None, var_type=TemplateConditionVariable.GLOBAL, loop=False, condition_type=TemplateConditionNode.BLOCK, next_value=None, next_value_step=0):
        TemplateConditionNode.__init__(self, name, value, var_type, loop, condition_type)
        self._next_step_count = 0
        self._next_value = next_value
        self._next_value_step = next_value_step

    def _pre_default_loop_check(self, client_context):
        self._next_step_count += 1
        if self._next_step_count == self._next_value_step:
            client_context.bot.get_conversation(client_context).set_property(self._next_value[0], self._next_value[1])


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

        cond4 = TemplateConditionListItemNode(name="name4")
        cond4.append(TemplateWordNode("Word4"))
        node.append(cond4)

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

    def test_type3_node_with_loop(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = MyLoopTemplateConditionNode(condition_type=3, next_value=('name1', "value1"), next_value_step=1)
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

        cond4 = TemplateConditionListItemNode(name="name4", loop=True)          # Default Value
        cond4.append(TemplateWordNode("Word4"))
        node.append(cond4)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        self._client_context.bot.get_conversation(self._client_context).set_property('name1', "value5")

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("Word4 Word1", result)

    def patch_resolve_type3_to_string(self, client_context):
        raise Exception ("Mock Exception")

    @patch("programy.parser.template.nodes.condition.TemplateConditionNode._resolve_type3_to_string", patch_resolve_type3_to_string)
    def test_type3_exception(self):
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
        self.assertEqual("", result)

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

