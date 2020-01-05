from unittest.mock import patch
import xml.etree.ElementTree as ET
from programy.dialog.question import Question
from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.condition import TemplateConditionNode
from programy.parser.template.nodes.condition import TemplateConditionVariable
from programy.parser.template.nodes.word import TemplateWordNode
from programytest.parser.base import ParserTestsBaseClass


class TemplateConditionType1NodeTests(ParserTestsBaseClass):

    def test_type1_node_global_match(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateConditionNode("name1", TemplateWordNode("value1"), var_type=TemplateConditionNode.GLOBAL)
        self.assertIsNotNone(node)

        node.append(TemplateWordNode("Hello"))
        root.append(node)
        self.assertEqual(len(root.children), 1)

        self._client_context.bot.get_conversation(self._client_context).set_property('name1', "value1")

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual(result, "Hello")

    def patch_resolve_type1_to_string(self, client_context):
        raise Exception ("Mock Exception")

    @patch("programy.parser.template.nodes.condition.TemplateConditionNode._resolve_type1_to_string", patch_resolve_type1_to_string)
    def test_type1_resolve_exception(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateConditionNode("name1", TemplateWordNode("value1"), var_type=TemplateConditionNode.GLOBAL)
        self.assertIsNotNone(node)

        node.append(TemplateWordNode("Hello"))
        root.append(node)
        self.assertEqual(len(root.children), 1)

        self._client_context.bot.get_conversation(self._client_context).set_property('name1', "value1")

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual(result, "")

    def test_type1_node_global_nomatch(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateConditionNode("name1", TemplateWordNode("value1"), var_type=TemplateConditionNode.GLOBAL)
        self.assertIsNotNone(node)

        node.append(TemplateWordNode("Hello"))
        root.append(node)
        self.assertEqual(len(root.children), 1)

        self._client_context.bot.get_conversation(self._client_context).set_property('name1', "value2")

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual(result, "")

    def test_type1_to_xml_global(self):
        root = TemplateNode()
        node = TemplateConditionNode("name1", TemplateWordNode("value1"), var_type=TemplateConditionNode.GLOBAL)
        node.append(TemplateWordNode("Hello"))
        root.append(node)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><condition name="name1"><value>value1</value>Hello</condition></template>', xml_str)

    def test_type1_node_local_match(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateConditionNode("var1", TemplateWordNode("value1"), var_type=TemplateConditionNode.LOCAL)
        self.assertIsNotNone(node)

        node.append(TemplateWordNode("Hello"))
        root.append(node)
        self.assertEqual(len(root.children), 1)

        question = Question.create_from_text(self._client_context, "Hello")
        self._client_context.bot.get_conversation(self._client_context).record_dialog(question)
        self._client_context.bot.get_conversation(self._client_context).current_question().set_property("var1", "value1")

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual(result, "Hello")

    def test_type1_node_local_nomatch(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateConditionNode("var1", TemplateWordNode("value1"), var_type=TemplateConditionNode.LOCAL)
        self.assertIsNotNone(node)

        node.append(TemplateWordNode("Hello"))
        root.append(node)
        self.assertEqual(len(root.children), 1)

        question = Question.create_from_text(self._client_context, "Hello")
        self._client_context.bot.get_conversation(self._client_context).record_dialog(question)
        self._client_context.bot.get_conversation(self._client_context).current_question().set_property("var1", "value2")

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual(result, "")

    def test_type1_to_xml_local(self):
        root = TemplateNode()
        node = TemplateConditionNode("name1", TemplateWordNode("value1"), var_type=TemplateConditionNode.LOCAL)
        node.append(TemplateWordNode("Hello"))
        root.append(node)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><condition var="name1"><value>value1</value>Hello</condition></template>', xml_str)

    def test_type1_node_bot_match(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateConditionNode("name1", TemplateWordNode("value1"), var_type=TemplateConditionNode.BOT)
        self.assertIsNotNone(node)

        node.append(TemplateWordNode("Hello"))
        root.append(node)
        self.assertEqual(len(root.children), 1)

        self._client_context.brain.properties.add_property('name1', "value1")

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual(result, "Hello")

    def test_type1_node_bot_nomatch(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateConditionNode("name1", TemplateWordNode("value1"), var_type=TemplateConditionNode.BOT)
        self.assertIsNotNone(node)

        node.append(TemplateWordNode("Hello"))
        root.append(node)
        self.assertEqual(len(root.children), 1)

        self._client_context.brain.properties.add_property('name1', "value2")

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual(result, "")

    def test_type1_to_xml_bot(self):
        root = TemplateNode()
        node = TemplateConditionNode("name1", TemplateWordNode("value1"), var_type=TemplateConditionNode.BOT)
        node.append(TemplateWordNode("Hello"))
        root.append(node)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><condition bot="name1"><value>value1</value>Hello</condition></template>', xml_str)

    def test_to_string_defaults(self):
        node = TemplateConditionNode()
        self.assertEquals('[CONDITION name="None"]', node.to_string())

    def test_to_string_defaults_global(self):
        node = TemplateConditionNode(name="global", var_type=TemplateConditionVariable.GLOBAL)
        self.assertEquals('[CONDITION name="global"]', node.to_string())

    def test_to_string_defaults_local(self):
        node = TemplateConditionNode(name="local", var_type=TemplateConditionVariable.LOCAL)
        self.assertEquals('[CONDITION var="local"]', node.to_string())

    def test_to_string_defaults_bot(self):
        node = TemplateConditionNode(name="bot", var_type=TemplateConditionVariable.BOT)
        self.assertEquals('[CONDITION bot="bot"]', node.to_string())

    def test_to_string_defaults_bot(self):
        node = TemplateConditionNode(name="default", var_type=TemplateConditionVariable.DEFAULT)
        self.assertEquals('[CONDITION default="default"]', node.to_string())

    def test_to_string_defaults_unknown(self):
        node = TemplateConditionNode(name="unknown", var_type=999)
        self.assertEquals('[CONDITION unknown="unknown"]', node.to_string())

    def test_to_xml_defaults(self):
        node = TemplateConditionNode()
        self.assertEquals('<condition></condition>', node.to_xml(self._client_context))

    def test_to_xml_with_value(self):
        node = TemplateConditionNode(value=TemplateWordNode("3"))
        self.assertEquals('<condition><value>3</value></condition>', node.to_xml(self._client_context))

    def test_to_xml_defaults_global(self):
        node = TemplateConditionNode(name="global", var_type=TemplateConditionVariable.GLOBAL)
        self.assertEquals('<condition name="global"></condition>', node.to_xml(self._client_context))

    def test_to_xml_defaults_local(self):
        node = TemplateConditionNode(name="local", var_type=TemplateConditionVariable.LOCAL)
        self.assertEquals('<condition var="local"></condition>', node.to_xml(self._client_context))

    def test_to_xml_defaults_bot(self):
        node = TemplateConditionNode(name="bot", var_type=TemplateConditionVariable.BOT)
        self.assertEquals('<condition bot="bot"></condition>', node.to_xml(self._client_context))

    def test_to_xml_defaults_default(self):
        node = TemplateConditionNode(name="default", var_type=TemplateConditionVariable.DEFAULT)
        self.assertEquals('<condition default="default"></condition>', node.to_xml(self._client_context))

    def test_to_xml_defaults_unknown(self):
        node = TemplateConditionNode(name="unknown", var_type=999)
        self.assertEquals('<condition unknown="unknown"></condition>', node.to_xml(self._client_context))

    def test_resolve_block(self):
        node = TemplateConditionNode(name="global", value="3", condition_type=TemplateConditionNode.BLOCK)
        self.assertEquals("", node.resolve_to_string(self._client_context))

    def test_resolve_single(self):
        node = TemplateConditionNode(name="global", value="3", condition_type=TemplateConditionNode.SINGLE)
        self.assertEquals("", node.resolve_to_string(self._client_context))

    def test_resolve_bot(self):
        node = TemplateConditionNode(name="global", value="3", condition_type=TemplateConditionNode.BOT)
        self.assertEquals("", node.resolve_to_string(self._client_context))

    def test_resolve_unknown(self):
        node = TemplateConditionNode(name="global", value="3", condition_type=999)
        self.assertEquals("", node.resolve_to_string(self._client_context))

