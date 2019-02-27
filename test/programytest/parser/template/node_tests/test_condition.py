import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.word import TemplateWordNode
from programy.parser.template.nodes.condition import TemplateConditionVariable
from programy.parser.template.nodes.condition import TemplateConditionNode
from programy.parser.template.nodes.condition import TemplateConditionListItemNode
from programy.dialog.question import Question

from programytest.parser.base import ParserTestsBaseClass

class TemplateConditionVariableTests(ParserTestsBaseClass):

    def test_init_defaults(self):
        var = TemplateConditionVariable()
        self.assertIsNotNone(var)
        self.assertIsNone(var.name)
        self.assertIsNone(var.value)
        self.assertEqual(var.var_type, TemplateConditionVariable.GLOBAL)
        self.assertFalse(var.loop)

    def test_init_global_as_default(self):
        var = TemplateConditionVariable(name="var1", value=TemplateWordNode("value1"))
        self.assertIsNotNone(var)
        self.assertEqual(var.name, "var1")
        self.assertEqual(var.value.word, "value1")
        self.assertEqual(var.var_type, TemplateConditionVariable.GLOBAL)
        self.assertFalse(var.loop)

    def test_init_global(self):
        var = TemplateConditionVariable(name="var1", value=TemplateWordNode("value1"), var_type=TemplateConditionVariable.GLOBAL)
        self.assertIsNotNone(var)
        self.assertEqual(var.name, "var1")
        self.assertEqual(var.value.word, "value1")
        self.assertEqual(var.var_type, TemplateConditionVariable.GLOBAL)
        self.assertFalse(var.loop)

    def test_init_global_with_loop(self):
        var = TemplateConditionVariable(name="var1", value=TemplateWordNode("value1"), var_type=TemplateConditionVariable.GLOBAL,loop=True)
        self.assertIsNotNone(var)
        self.assertEqual(var.name, "var1")
        self.assertEqual(var.value.word, "value1")
        self.assertEqual(var.var_type, TemplateConditionVariable.GLOBAL)
        self.assertTrue(var.loop)

    def test_init_local(self):
        var = TemplateConditionVariable(name="var1", value=TemplateWordNode("value1"), var_type=TemplateConditionVariable.LOCAL)
        self.assertIsNotNone(var)
        self.assertEqual(var.name, "var1")
        self.assertEqual(var.value.word, "value1")
        self.assertEqual(var.var_type, TemplateConditionVariable.LOCAL)
        self.assertFalse(var.loop)

    def test_init_local_with_loop(self):
        var = TemplateConditionVariable(name="var1", value=TemplateWordNode("value1"), var_type=TemplateConditionVariable.LOCAL, loop=True)
        self.assertIsNotNone(var)
        self.assertEqual(var.name, "var1")
        self.assertEqual(var.value.word, "value1")
        self.assertEqual(var.var_type, TemplateConditionVariable.LOCAL)
        self.assertTrue(var.loop)

    def test_init_bot(self):
        var = TemplateConditionVariable(name="var1", value=TemplateWordNode("value1"), var_type=TemplateConditionVariable.BOT)
        self.assertIsNotNone(var)
        self.assertEqual(var.name, "var1")
        self.assertEqual(var.value.word, "value1")
        self.assertEqual(var.var_type, TemplateConditionVariable.BOT)
        self.assertFalse(var.loop)

    def test_init_bot_with_loop(self):
        var = TemplateConditionVariable(name="var1", value=TemplateWordNode("value1"), var_type=TemplateConditionVariable.BOT, loop=True)
        self.assertIsNotNone(var)
        self.assertEqual(var.name, "var1")
        self.assertEqual(var.value.word, "value1")
        self.assertEqual(var.var_type, TemplateConditionVariable.BOT)
        self.assertTrue(var.loop)


class TemplateConditionListItemNodeTests(ParserTestsBaseClass):

    def test_init_defaults(self):
        var = TemplateConditionListItemNode()
        self.assertIsNotNone(var)
        self.assertIsNone(var.name)
        self.assertIsNone(var.value)
        self.assertEqual(var.var_type, TemplateConditionListItemNode.GLOBAL)
        self.assertFalse(var.loop)
        self.assertTrue(var.is_default())
        self.assertEqual("[CONDITIONLIST]", var.to_string())
        self.assertEqual("<li></li>", var.to_xml(self._client_context))

    def test_init_global_as_default(self):
        var = TemplateConditionListItemNode(name="var1", value=TemplateWordNode("value1"))
        self.assertIsNotNone(var)
        self.assertEqual(var.name, "var1")
        self.assertEqual(var.value.word, "value1")
        self.assertEqual(var.var_type, TemplateConditionListItemNode.GLOBAL)
        self.assertFalse(var.loop)
        self.assertFalse(var.is_default())
        self.assertEqual("[CONDITIONLIST(var1=[WORD]value1)]", var.to_string())
        self.assertEqual('<li name="var1"><value>value1</value></li>', var.to_xml(self._client_context))

    def test_init_global(self):
        var = TemplateConditionListItemNode(name="var1", value=TemplateWordNode("value1"), var_type=TemplateConditionListItemNode.GLOBAL)
        self.assertIsNotNone(var)
        self.assertEqual(var.name, "var1")
        self.assertEqual(var.value.word, "value1")
        self.assertEqual(var.var_type, TemplateConditionListItemNode.GLOBAL)
        self.assertFalse(var.loop)
        self.assertFalse(var.is_default())
        self.assertEqual("[CONDITIONLIST(var1=[WORD]value1)]", var.to_string())
        self.assertEqual('<li name="var1"><value>value1</value></li>', var.to_xml(self._client_context))

    def test_init_global_with_loop(self):
        var = TemplateConditionListItemNode(name="var1", value=TemplateWordNode("value1"), var_type=TemplateConditionListItemNode.GLOBAL,loop=True)
        self.assertIsNotNone(var)
        self.assertEqual(var.name, "var1")
        self.assertEqual(var.value.word, "value1")
        self.assertEqual(var.var_type, TemplateConditionListItemNode.GLOBAL)
        self.assertTrue(var.loop)
        self.assertFalse(var.is_default())
        self.assertEqual("[CONDITIONLIST(var1=[WORD]value1)]", var.to_string())
        self.assertEqual('<li name="var1"><value>value1</value><loop /></li>', var.to_xml(self._client_context))

    def test_init_local(self):
        var = TemplateConditionListItemNode(name="var1", value=TemplateWordNode("value1"), var_type=TemplateConditionListItemNode.LOCAL)
        self.assertIsNotNone(var)
        self.assertEqual(var.name, "var1")
        self.assertEqual(var.value.word, "value1")
        self.assertEqual(var.var_type, TemplateConditionListItemNode.LOCAL)
        self.assertFalse(var.loop)
        self.assertFalse(var.is_default())
        self.assertEqual("[CONDITIONLIST(var1=[WORD]value1)]", var.to_string())
        self.assertEqual('<li var="var1"><value>value1</value></li>', var.to_xml(self._client_context))

    def test_init_local_with_loop(self):
        var = TemplateConditionListItemNode(name="var1", value=TemplateWordNode("value1"), var_type=TemplateConditionListItemNode.LOCAL, loop=True)
        self.assertIsNotNone(var)
        self.assertEqual(var.name, "var1")
        self.assertEqual(var.value.word, "value1")
        self.assertEqual(var.var_type, TemplateConditionListItemNode.LOCAL)
        self.assertTrue(var.loop)
        self.assertFalse(var.is_default())
        self.assertEqual("[CONDITIONLIST(var1=[WORD]value1)]", var.to_string())
        self.assertEqual('<li var="var1"><value>value1</value><loop /></li>', var.to_xml(self._client_context))

    def test_init_bot(self):
        var = TemplateConditionListItemNode(name="var1", value=TemplateWordNode("value1"), var_type=TemplateConditionListItemNode.BOT)
        self.assertIsNotNone(var)
        self.assertEqual(var.name, "var1")
        self.assertEqual(var.value.word, "value1")
        self.assertEqual(var.var_type, TemplateConditionListItemNode.BOT)
        self.assertFalse(var.loop)
        self.assertFalse(var.is_default())
        self.assertEqual("[CONDITIONLIST(var1=[WORD]value1)]", var.to_string())
        self.assertEqual('<li bot="var1"><value>value1</value></li>', var.to_xml(self._client_context))

    def test_init_bot_with_loop(self):
        var = TemplateConditionListItemNode(name="var1", value=TemplateWordNode("value1"), var_type=TemplateConditionListItemNode.BOT, loop=True)
        self.assertIsNotNone(var)
        self.assertEqual(var.name, "var1")
        self.assertEqual(var.value.word, "value1")
        self.assertEqual(var.var_type, TemplateConditionListItemNode.BOT)
        self.assertTrue(var.loop)
        self.assertFalse(var.is_default())
        self.assertEqual("[CONDITIONLIST(var1=[WORD]value1)]", var.to_string())
        self.assertEqual('<li bot="var1"><value>value1</value><loop /></li>', var.to_xml(self._client_context))


class TemplateConditionNodeTests(ParserTestsBaseClass):

    ###################################################################################################################
    # Type 1 Global
    #

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

    ###################################################################################################################
    # Type 1 Local
    #

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

    ###################################################################################################################
    # Type 1 Global
    #

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

    ###################################################################################################################
    # Type 2 Global
    #

    def test_type2_node_global(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateConditionNode("cond1", condition_type=2)
        self.assertIsNotNone(node)
        cond1 = TemplateConditionListItemNode(value=TemplateWordNode("value1"))
        cond1.append(TemplateWordNode("Word1"))
        node.append(cond1)
        cond2 = TemplateConditionListItemNode(value=TemplateWordNode("value2"))
        cond2.append(TemplateWordNode("Word2"))
        node.append(cond2)
        cond3 = TemplateConditionListItemNode()
        cond3.append(TemplateWordNode("Word3"))
        node.append(cond3)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        self._client_context.bot.get_conversation(self._client_context).set_property('cond1', "value2")

        question = Question.create_from_text(self._client_context, "Hello")
        self._client_context.bot.get_conversation(self._client_context).record_dialog(question)
        self._client_context.bot.get_conversation(self._client_context).current_question().set_property("cond1", "value2")

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("Word2", result)

    def test_type2_to_xml_global(self):
        root = TemplateNode()

        node = TemplateConditionNode("cond1", condition_type=2)
        self.assertIsNotNone(node)
        cond1 = TemplateConditionListItemNode(value=TemplateWordNode("value1"))
        cond1.append(TemplateWordNode("Word1"))
        node.append(cond1)
        cond2 = TemplateConditionListItemNode(value=TemplateWordNode("value2"))
        cond2.append(TemplateWordNode("Word2"))
        node.append(cond2)
        cond3 = TemplateConditionListItemNode()
        cond3.append(TemplateWordNode("Word3"))
        node.append(cond3)

        root.append(node)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><condition name="cond1"><li><value>value1</value>Word1</li> <li><value>value2</value>Word2</li> <li>Word3</li></condition></template>', xml_str)

    ###################################################################################################################
    # Type 2 Local
    #

    def test_type2_node_local(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateConditionNode("var1", var_type=TemplateConditionNode.LOCAL, condition_type=2)
        self.assertIsNotNone(node)
        cond1 = TemplateConditionListItemNode(value=TemplateWordNode("value1"), var_type=TemplateConditionNode.LOCAL)
        cond1.append(TemplateWordNode("Word1"))
        node.append(cond1)
        cond2 = TemplateConditionListItemNode(value=TemplateWordNode("value2"), var_type=TemplateConditionNode.LOCAL)
        cond2.append(TemplateWordNode("Word2"))
        node.append(cond2)
        cond3 = TemplateConditionListItemNode()
        cond3.append(TemplateWordNode("Word3"))
        node.append(cond3)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        question = Question.create_from_text(self._client_context, "Hello")
        self._client_context.bot.get_conversation(self._client_context).record_dialog(question)
        self._client_context.bot.get_conversation(self._client_context).current_question().set_property("var1", "value2")

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("Word2", result)

    def test_type2_to_xml_local(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateConditionNode("var1", var_type=TemplateConditionNode.LOCAL, condition_type=2)
        self.assertIsNotNone(node)
        cond1 = TemplateConditionListItemNode(value=TemplateWordNode("value1"), var_type=TemplateConditionNode.LOCAL)
        cond1.append(TemplateWordNode("Word1"))
        node.append(cond1)
        cond2 = TemplateConditionListItemNode(value=TemplateWordNode("value2"), var_type=TemplateConditionNode.LOCAL)
        cond2.append(TemplateWordNode("Word2"))
        node.append(cond2)
        cond3 = TemplateConditionListItemNode()
        cond3.append(TemplateWordNode("Word3"))
        node.append(cond3)

        root.append(node)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><condition var="var1"><li><value>value1</value>Word1</li> <li><value>value2</value>Word2</li> <li>Word3</li></condition></template>', xml_str)

    ###################################################################################################################
    # Type 2 Bot
    #

    def test_type2_node_bot(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateConditionNode("cond1", var_type=TemplateConditionNode.BOT, condition_type=2)
        self.assertIsNotNone(node)
        cond1 = TemplateConditionListItemNode(value=TemplateWordNode("value1"), var_type=TemplateConditionNode.BOT)
        cond1.append(TemplateWordNode("Word1"))
        node.append(cond1)
        cond2 = TemplateConditionListItemNode(value=TemplateWordNode("value2"), var_type=TemplateConditionNode.BOT)
        cond2.append(TemplateWordNode("Word2"))
        node.append(cond2)
        cond3 = TemplateConditionListItemNode()
        cond3.append(TemplateWordNode("Word3"))
        node.append(cond3)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        self._client_context.brain.properties.add_property('cond1', "value2")

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("Word2", result)

    def test_type2_to_xml_bot(self):
        root = TemplateNode()

        node = TemplateConditionNode("cond1", var_type=TemplateConditionNode.BOT, condition_type=2)
        self.assertIsNotNone(node)
        cond1 = TemplateConditionListItemNode(value=TemplateWordNode("value1"))
        cond1.append(TemplateWordNode("Word1"))
        node.append(cond1)
        cond2 = TemplateConditionListItemNode(value=TemplateWordNode("value2"))
        cond2.append(TemplateWordNode("Word2"))
        node.append(cond2)
        cond3 = TemplateConditionListItemNode()
        cond3.append(TemplateWordNode("Word3"))
        node.append(cond3)

        root.append(node)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><condition bot="cond1"><li><value>value1</value>Word1</li> <li><value>value2</value>Word2</li> <li>Word3</li></condition></template>', xml_str)

    ###################################################################################################################
    # Type 3

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

