import xml.etree.ElementTree as ET

from programy.parser.template.nodes import *
from programy.bot import Bot
from programy.brain import Brain
from programy.dialog import Conversation, Question

from test.parser.template.base import TemplateTestsBaseClass
from programy.config import BrainConfiguration, BotConfiguration, BrainFileConfiguration

######################################################################################################################
#
class TemplateNodeBasicTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

    def test_to_xml(self):
        root = TemplateNode()
        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template />", xml_str)


######################################################################################################################
#
class TemplateWordNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        root.append(TemplateWordNode("Hello"))
        root.append(TemplateWordNode("World!"))
        self.assertEqual(len(root.children), 2)

        resolved = root.resolve(self.bot, self.clientid)
        self.assertIsNotNone(resolved)
        self.assertEqual(resolved, "Hello World!")

    def test_to_xml(self):
        root = TemplateNode()
        root.append(TemplateWordNode("Hello"))

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template>Hello</template>", xml_str)


######################################################################################################################
#
class TemplateRandomNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        random = TemplateRandomNode()
        random.append(TemplateWordNode("Test1"))
        random.append(TemplateWordNode("Test2"))
        random.append(TemplateWordNode("Test3"))
        self.assertEqual(len(random.children), 3)

        root.append(random)

        resolved = root.resolve(self.bot, self.clientid)
        self.assertIsNotNone(resolved)
        self.assertOneOf(resolved, ["Test1", "Test2", "Test3"])

    def test_to_xml(self):
        root = TemplateNode()
        random = TemplateRandomNode()
        root.append(random)
        random.append(TemplateWordNode("Test1"))
        random.append(TemplateWordNode("Test2"))

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><random><li>Test1</li><li>Test2</li></random></template>", xml_str)


######################################################################################################################
#
class TemplateSRAINodeTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateSRAINode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        node.append(TemplateWordNode("Hello"))
        self.assertEqual(len(node.children), 1)

        self.bot.response = "Hiya"
        self.assertEqual(root.resolve(self.bot, self.clientid), "Hiya")

    def test_to_xml(self):
        root = TemplateNode()
        node = TemplateSRAINode()
        root.append(node)
        node.append(TemplateWordNode("Hello"))

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><srai>Hello</srai></template>", xml_str)


######################################################################################################################
#
class TemplateSrNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateSrNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

    def test_to_xml(self):
        root = TemplateNode()
        node = TemplateSrNode()
        root.append(node)

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><sr /></template>", xml_str)


#######################################################################################################################
#
class TemplateIndexedNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateIndexedNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)


######################################################################################################################
#
class TemplateStarNodeTests(TemplateTestsBaseClass):

    def test_node_defaults(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateStarNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

    def test_to_xml_defaults(self):
        root = TemplateNode()
        node = TemplateStarNode()
        root.append(node)

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><star /></template>", xml_str)

    def test_node_no_defaults(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateStarNode(position=3, index=2)
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)
        self.assertEqual(2, node.index)
        self.assertEqual(3, node.position)

    def test_to_xml_no_defaults(self):
        root = TemplateNode()
        node = TemplateStarNode(position=2, index=3)
        root.append(node)

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><star index="3" position="2" /></template>', xml_str)


######################################################################################################################
#
class TemplateGetNodeTests(TemplateTestsBaseClass):

    def test_local_get(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateGetNode()
        node.name = TemplateWordNode("name")
        node.local = True
        node.append(TemplateWordNode("Fred"))
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        conversation = self.bot.get_conversation(self.clientid)
        self.assertIsNotNone(conversation)
        question = Question.create_from_text("Hello")
        conversation.record_dialog(question)
        self.assertIsNotNone(conversation.current_question())
        question.current_sentence().set_predicate("name", "keith")

        result = root.resolve(self.bot, self.clientid)
        self.assertIsNotNone(result)
        self.assertEqual("keith", result)

    def test_to_xml_local_get(self):
        root = TemplateNode()
        node = TemplateGetNode()
        node.name = TemplateWordNode("name")
        node.local = True
        root.append(node)

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><get var="name" /></template>', xml_str)

    def test_local_no_value(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateGetNode()
        node.name = TemplateWordNode("name")
        node.local = True
        node.append(TemplateWordNode("Fred"))
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        self.bot.brain.properties.add_property("default-get", "unknown")

        conversation = self.bot.get_conversation(self.clientid)
        self.assertIsNotNone(conversation)
        question = Question.create_from_text("Hello")
        conversation.record_dialog(question)

        result = root.resolve(self.bot, self.clientid)
        self.assertIsNotNone(result)
        self.assertEqual("unknown", result)

    def test_global_get(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateGetNode()
        node.name = TemplateWordNode("name")
        node.local = False
        node.append(TemplateWordNode("Fred"))
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        conversation = self.bot.get_conversation(self.clientid)
        self.assertIsNotNone(conversation)
        question = Question.create_from_text("Hello")
        conversation.record_dialog(question)
        self.assertIsNotNone(conversation.current_question())
        conversation.set_predicate("name", "keith")

        result = root.resolve(self.bot, self.clientid)
        self.assertIsNotNone(result)
        self.assertEqual("keith", result)

    def test_to_xml_global_get(self):
        root = TemplateNode()
        node = TemplateGetNode()
        node.name = TemplateWordNode("name")
        node.local = False
        root.append(node)

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><get name="name" /></template>', xml_str)

    def test_global_get_no_value(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateGetNode()
        node.name = TemplateWordNode("name")
        node.local = False
        node.append(TemplateWordNode("Fred"))
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        self.bot.brain.properties.add_property("default-get", "unknown")

        result = root.resolve(self.bot, self.clientid)
        self.assertIsNotNone(result)
        self.assertEqual("unknown", result)


######################################################################################################################
#
class TemplateSetNodeTests(TemplateTestsBaseClass):

    def test_local_set(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateSetNode()
        self.assertIsNotNone(node)
        node.name = TemplateWordNode("name")
        node.local = True
        node.append(TemplateWordNode("keith"))

        root.append(node)
        self.assertEqual(len(root.children), 1)

        conversation = self.bot.get_conversation(self.clientid)
        self.assertIsNotNone(conversation)
        question = Question.create_from_text("Hello")
        conversation.record_dialog(question)
        self.assertIsNotNone(conversation.current_question())

        result = node.resolve(self.bot, self.clientid)
        self.assertIsNotNone(result)
        self.assertEqual("keith", result)

        self.assertEqual("keith", question.current_sentence().predicate("name"))

    def test_to_xml_local_set(self):
        root = TemplateNode()
        node = TemplateSetNode()
        node.name = TemplateWordNode("name")
        node.local = True
        root.append(node)
        node.append(TemplateWordNode("keith"))

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><set var="name">keith</set></template>', xml_str)

    def test_global_set(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateSetNode()
        self.assertIsNotNone(node)
        node.name = TemplateWordNode("name")
        node.local = False
        node.append(TemplateWordNode("keith"))

        root.append(node)
        self.assertEqual(len(root.children), 1)

        conversation = self.bot.get_conversation(self.clientid)
        self.assertIsNotNone(conversation)
        question = Question.create_from_text("Hello")
        conversation.record_dialog(question)
        self.assertIsNotNone(conversation.current_question())

        result = node.resolve(self.bot, self.clientid)
        self.assertIsNotNone(result)
        self.assertEqual("keith", result)

        self.assertEqual("keith", conversation.predicate("name"))

    def test_to_xml_global_set(self):
        root = TemplateNode()
        node = TemplateSetNode()
        node.name = TemplateWordNode("name")
        node.local = False
        root.append(node)
        node.append(TemplateWordNode("keith"))

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><set name="name">keith</set></template>', xml_str)


######################################################################################################################
#
class TemplateBotNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateBotNode()
        self.assertIsNotNone(node)
        node.name = TemplateWordNode("location")
        root.append(node)
        self.assertEqual(len(root.children), 1)

        self.bot.brain.properties.add_property("location", "Scotland")

        result = node.resolve(self.bot, self.clientid)
        self.assertIsNotNone(result)
        self.assertEqual("Scotland", result)

    def test_node_no_value(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateBotNode()
        self.assertIsNotNone(node)
        node.name = TemplateWordNode("location")
        root.append(node)
        self.assertEqual(len(root.children), 1)

        self.bot.brain.properties.add_property("default-property", "unknown")

        result = node.resolve(self.bot, self.clientid)
        self.assertIsNotNone(result)
        self.assertEqual("unknown", result)

    def test_to_xml(self):
        root = TemplateNode()
        node = TemplateBotNode()
        node.name = TemplateWordNode("name")
        root.append(node)

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><bot name="name" /></template>', xml_str)


#######################################################################################################################
#
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
        node = TemplateConditionListItemNode("name1", value="value1")
        node.append(TemplateWordNode("Hello"))
        root.append(node)

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><li name="name1" value="value1">Hello</li></template>', xml_str)

    def test_to_xml_local(self):
        root = TemplateNode()
        node = TemplateConditionListItemNode("name1", value="value1", local=True)
        node.append(TemplateWordNode("Hello"))
        root.append(node)

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><li value="value1" var="name1">Hello</li></template>', xml_str)


class TemplateConditionNodeTests(TemplateTestsBaseClass):

    def test_get_predicate_value(self):
        node = TemplateConditionNode()
        self.assertIsNotNone(node)

        self.bot.conversation(self.clientid)._predicates['name1'] = "value1"

        value = node._get_predicate_value(self.bot, self.clientid, "name1", False)
        self.assertEqual(value, "value1")

        question = Question.create_from_text("Hello")
        self.bot.conversation(self.clientid).record_dialog(question)
        self.bot.conversation(self.clientid).current_question().current_sentence()._predicates["var1"] = "value2"

        value = node._get_predicate_value(self.bot, self.clientid, "var1", True)
        self.assertEqual(value, "value2")

        value = node._get_predicate_value(self.bot, self.clientid, "unknown", True)
        self.assertEqual(value, "")

        self.bot.brain.properties.add_property("default-get", "Unknown")
        value = node._get_predicate_value(self.bot, self.clientid, "name3", False)
        self.assertEqual(value, "Unknown")


class TemplateType1ConditionNodeTests(TemplateTestsBaseClass):

    def test_node_global_match(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateType1ConditionNode("name1", "value1", local=False)
        self.assertIsNotNone(node)
        self.assertEqual(node.name, "name1")
        self.assertEqual(node.value, "value1")
        self.assertFalse(node.local)

        node.append(TemplateWordNode("Hello"))
        root.append(node)
        self.assertEqual(len(root.children), 1)

        self.bot.conversation(self.clientid)._predicates['name1'] = "value1"

        result = root.resolve(self.bot, self.clientid)
        self.assertIsNotNone(result)
        self.assertEqual(result, "Hello")

    def test_node_global_nomatch(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateType1ConditionNode("name1", "value1", local=False)
        self.assertIsNotNone(node)
        self.assertEqual(node.name, "name1")
        self.assertEqual(node.value, "value1")
        self.assertFalse(node.local)

        node.append(TemplateWordNode("Hello"))
        root.append(node)
        self.assertEqual(len(root.children), 1)

        self.bot.conversation(self.clientid)._predicates['name1'] = "value2"

        result = root.resolve(self.bot, self.clientid)
        self.assertIsNotNone(result)
        self.assertEqual(result, "")

    def test_node_local_match(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateType1ConditionNode("var1", "value1", local=True)
        self.assertIsNotNone(node)
        self.assertEqual(node.name, "var1")
        self.assertEqual(node.value, "value1")
        self.assertTrue(node.local)

        node.append(TemplateWordNode("Hello"))
        root.append(node)
        self.assertEqual(len(root.children), 1)

        question = Question.create_from_text("Hello")
        self.bot.conversation(self.clientid).record_dialog(question)
        self.bot.conversation(self.clientid).current_question().current_sentence()._predicates["var1"] = "value1"

        result = root.resolve(self.bot, self.clientid)
        self.assertIsNotNone(result)
        self.assertEqual(result, "Hello")

    def test_node_local_nomatch(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateType1ConditionNode("var1", "value1", local=True)
        self.assertIsNotNone(node)
        self.assertEqual(node.name, "var1")
        self.assertEqual(node.value, "value1")
        self.assertTrue(node.local)

        node.append(TemplateWordNode("Hello"))
        root.append(node)
        self.assertEqual(len(root.children), 1)

        question = Question.create_from_text("Hello")
        self.bot.conversation(self.clientid).record_dialog(question)
        self.bot.conversation(self.clientid).current_question().current_sentence()._predicates["var1"] = "value2"

        result = root.resolve(self.bot, self.clientid)
        self.assertIsNotNone(result)
        self.assertEqual(result, "")

    def test_to_xml_global(self):
        root = TemplateNode()
        node = TemplateType1ConditionNode("name1", "value1", local=False)
        node.append(TemplateWordNode("Hello"))
        root.append(node)

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><condition name="name1" value="value1">Hello</condition></template>', xml_str)

    def test_to_xml_local(self):
        root = TemplateNode()
        node = TemplateType1ConditionNode("name1", "value1", local=True)
        node.append(TemplateWordNode("Hello"))
        root.append(node)

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><condition value="value1" var="name1">Hello</condition></template>', xml_str)


class TestTemplateConditionNodeWithChildren(TemplateTestsBaseClass):

    def test_get_default(self):
        node = TemplateConditionNodeWithChildren()
        self.assertIsNotNone(node)

        node.append(TemplateConditionListItemNode("cond1", "value1"))
        node.append(TemplateConditionListItemNode("cond2", "value2"))
        node.append(TemplateConditionListItemNode("cond3"))

        self.assertEqual(3, len(node.children))

        default = node.get_default()
        self.assertIsNotNone(default)
        self.assertEqual(default.name, "cond3")


class TemplateType2ConditionNodeTests(TemplateTestsBaseClass):

    def test_node_global(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateType2ConditionNode("cond1")
        self.assertIsNotNone(node)
        cond1 = TemplateConditionListItemNode(value="value1")
        cond1.append(TemplateWordNode("Word1"))
        node.append(cond1)
        cond2 = TemplateConditionListItemNode(value="value2")
        cond2.append(TemplateWordNode("Word2"))
        node.append(cond2)
        cond3 = TemplateConditionListItemNode()
        cond3.append(TemplateWordNode("Word3"))
        node.append(cond3)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        self.bot.conversation(self.clientid)._predicates['cond1'] = "value2"

        result = root.resolve(self.bot, self.clientid)
        self.assertIsNotNone(result)
        self.assertEqual("Word2", result)

    def test_node_local(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateType2ConditionNode("var1", local=True)
        self.assertIsNotNone(node)
        cond1 = TemplateConditionListItemNode(value="value1")
        cond1.append(TemplateWordNode("Word1"))
        node.append(cond1)
        cond2 = TemplateConditionListItemNode(value="value2")
        cond2.append(TemplateWordNode("Word2"))
        node.append(cond2)
        cond3 = TemplateConditionListItemNode()
        cond3.append(TemplateWordNode("Word3"))
        node.append(cond3)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        question = Question.create_from_text("Hello")
        self.bot.conversation(self.clientid).record_dialog(question)
        self.bot.conversation(self.clientid).current_question().current_sentence()._predicates["var1"] = "value2"

        result = root.resolve(self.bot, self.clientid)
        self.assertIsNotNone(result)
        self.assertEqual("Word2", result)

    # TODO Add unit tests for <loop /> construct

    def test_to_xml_global(self):
        root = TemplateNode()

        node = TemplateType2ConditionNode("cond1")
        self.assertIsNotNone(node)
        cond1 = TemplateConditionListItemNode(value="value1")
        cond1.append(TemplateWordNode("Word1"))
        node.append(cond1)
        cond2 = TemplateConditionListItemNode(value="value2")
        cond2.append(TemplateWordNode("Word2"))
        node.append(cond2)
        cond3 = TemplateConditionListItemNode()
        cond3.append(TemplateWordNode("Word3"))
        node.append(cond3)

        root.append(node)

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><condition name="cond1"><li value="value1">Word1</li><li value="value2">Word2</li><li>Word3</li></condition></template>', xml_str)

    def test_to_xml_local(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateType2ConditionNode("var1", local=True)
        self.assertIsNotNone(node)
        cond1 = TemplateConditionListItemNode(value="value1")
        cond1.append(TemplateWordNode("Word1"))
        node.append(cond1)
        cond2 = TemplateConditionListItemNode(value="value2")
        cond2.append(TemplateWordNode("Word2"))
        node.append(cond2)
        cond3 = TemplateConditionListItemNode()
        cond3.append(TemplateWordNode("Word3"))
        node.append(cond3)

        root.append(node)

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><condition var="var1"><li value="value1">Word1</li><li value="value2">Word2</li><li>Word3</li></condition></template>', xml_str)


class TemplateType3ConditionNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateType3ConditionNode()
        self.assertIsNotNone(node)

        cond1 = TemplateConditionListItemNode(name="name1", value="value1" )
        cond1.append(TemplateWordNode("Word1"))
        node.append(cond1)

        cond2 = TemplateConditionListItemNode(name="name2", value="value1", local=True )
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

        cond1 = TemplateConditionListItemNode(name="name1", value="value1" )
        cond1.append(TemplateWordNode("Word1"))
        node.append(cond1)

        cond2 = TemplateConditionListItemNode(name="name2", value="value1", local=True )
        cond2.append(TemplateWordNode("Word2"))
        node.append(cond2)

        cond3 = TemplateConditionListItemNode(name="name3")
        cond3.append(TemplateWordNode("Word3"))
        node.append(cond3)

        root.append(node)

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><condition><li name="name1" value="value1">Word1</li><li value="value1" var="name2">Word2</li><li name="name3">Word3</li></condition></template>', xml_str)


######################################################################################################################
#
class TemplateSRAIXNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateSRAIXNode()
        self.assertIsNotNone(node)
        node.host       = "http://somebot.org"
        node.botid      = "1234567890"
        node.hint       = "The usual"
        node.apikey     = "ABCDEF"
        node.service    = "api"

        root.append(node)
        self.assertEqual(len(root.children), 1)

        #TODO Better unit testing of external service calls required

    def test_to_xml(self):
        root = TemplateNode()

        node = TemplateSRAIXNode()
        self.assertIsNotNone(node)
        node.host = "http://somebot.org"
        node.botid = "1234567890"
        node.hint = "The usual"
        node.apikey = "ABCDEF"
        node.service = "api"

        root.append(node)
        node.append(TemplateWordNode("Hello"))

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><sraix apikey="ABCDEF" botid="1234567890" hint="The usual" host="http://somebot.org" service="api">Hello</sraix></template>', xml_str)


######################################################################################################################
#
class TemplateMapNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateMapNode()
        node.name = TemplateWordNode("colours")
        node.append(TemplateWordNode("Black"))
        root.append(node)
        self.assertEqual(len(root.children), 1)

        self.bot.brain.maps._maps['colours'] = {'Black': 'White'}

        result = root.resolve(self.bot, self.clientid)
        self.assertIsNotNone(result)
        self.assertEqual("White", result)

    def test_to_xml(self):
        root = TemplateNode()
        node = TemplateMapNode()
        node.name = TemplateWordNode("colours")
        node.append(TemplateWordNode("Black"))
        root.append(node)

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><map name="colours">Black</map></template>', xml_str)


######################################################################################################################
#
class TemplateThinkNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateThinkNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

    # TODO More unit tests for different variations here please

    def test_to_xml(self):
        root = TemplateNode()
        node = TemplateThinkNode()
        root.append(node)
        node.append(TemplateWordNode("Test"))

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><think>Test</think></template>", xml_str)


######################################################################################################################
#
class TemplateLowercaseNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateLowercaseNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        word = TemplateWordNode("This is a Sentence")
        node.append(word)

        self.assertEqual(root.resolve(self.bot, self.clientid), "this is a sentence")

    def test_to_xml(self):
        root = TemplateNode()
        node = TemplateLowercaseNode()
        root.append(node)
        node.append(TemplateWordNode("Test"))

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><lowercase>Test</lowercase></template>", xml_str)


######################################################################################################################
#
class TemplateUppercaseNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateUppercaseNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        word = TemplateWordNode("This is a Sentence")
        node.append(word)

        self.assertEqual(root.resolve(self.bot, self.clientid), "THIS IS A SENTENCE")

    def test_to_xml(self):
        root = TemplateNode()
        node = TemplateUppercaseNode()
        root.append(node)
        node.append(TemplateWordNode("Test"))

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><uppercase>Test</uppercase></template>", xml_str)


######################################################################################################################
#
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


######################################################################################################################
#
class TemplateSentenceNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateSentenceNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        word = TemplateWordNode("this is a sentence")
        node.append(word)

        self.assertEqual(root.resolve(self.bot, self.clientid), "This is a sentence")

    def test_to_xml(self):
        root = TemplateNode()
        node = TemplateSentenceNode()
        root.append(node)
        node.append(TemplateWordNode("Test"))

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><sentence>Test</sentence></template>", xml_str)


######################################################################################################################
#
class TemplateNormalizeNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateNormalizeNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        node.append(TemplateWordNode(" shouldnt "))
        self.bot.brain.normals.process_splits([" shouldnt "," should not "])

        self.assertEqual(root.resolve(self.bot, self.clientid), "should not")

    def test_to_xml(self):
        root = TemplateNode()
        node = TemplateNormalizeNode()
        root.append(node)
        node.append(TemplateWordNode("Test"))

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><normalize>Test</normalize></template>", xml_str)


######################################################################################################################
#
class TemplateDenormalizeNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateDenormalizeNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        node.append(TemplateWordNode(" dot uk "))
        self.bot.brain.denormals.process_splits([" dot uk ",".uk"])

        self.assertEqual(root.resolve(self.bot, self.clientid), ".uk")

    def test_to_xml(self):
        root = TemplateNode()
        node = TemplateDenormalizeNode()
        root.append(node)
        node.append(TemplateWordNode("Test"))

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><denormalize>Test</denormalize></template>", xml_str)


######################################################################################################################
#
class TemplatePersonNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplatePersonNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        node.append(TemplateWordNode(" me "))
        self.bot.brain.persons.process_splits([" me "," you "])

        self.assertEqual(root.resolve(self.bot, self.clientid), "you")

    def test_to_xml(self):
        root = TemplateNode()
        node = TemplatePersonNode()
        root.append(node)
        node.append(TemplateWordNode("Test"))

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><person>Test</person></template>", xml_str)


######################################################################################################################
#
class TemplatePerson2NodeTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplatePerson2Node()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        node.append(TemplateWordNode(" me "))
        self.bot.brain.person2s.process_splits([" me "," him or her "])

        self.assertEqual(root.resolve(self.bot, self.clientid), "him or her")

    def test_to_xml(self):
        root = TemplateNode()
        node = TemplatePerson2Node()
        root.append(node)
        node.append(TemplateWordNode("Test"))

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><person2>Test</person2></template>", xml_str)


######################################################################################################################
#
class TemplateGenderNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateGenderNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        node.append(TemplateWordNode(" to him "))
        self.bot.brain.genders.process_splits([" to him "," to her "])

        self.assertEqual(root.resolve(self.bot, self.clientid), "to her")

    def test_to_xml(self):
        root = TemplateNode()
        node = TemplateGenderNode()
        root.append(node)
        node.append(TemplateWordNode("Test"))

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><gender>Test</gender></template>", xml_str)


######################################################################################################################
#
class TemplateIdNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateIdNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        self.assertEqual(root.resolve(None, "clientid"), "clientid")

    def test_to_xml(self):
        root = TemplateNode()
        root.append(TemplateIdNode())

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><id /></template>", xml_str)

######################################################################################################################
#
class TemplateVocabularyNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        test_bot = Bot(Brain(BrainConfiguration()), BotConfiguration())

        topic_element = ET.fromstring('<topic>*</topic>')
        that_element = ET.fromstring('<that>*</that>')
        pattern_element = ET.fromstring("<pattern>hello world</pattern>")
        test_bot.brain._aiml_parser.pattern_parser.add_pattern_to_graph(pattern_element, topic_element, that_element, None)

        test_bot.brain._sets_collection.add_set("testset", ["val1", "val2", "val3"])

        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateVocabularyNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        self.assertEquals(root.resolve(test_bot, "testid"), '5')

    def test_to_xml(self):
        root = TemplateNode()
        node = TemplateVocabularyNode()
        root.append(node)
        node.append(TemplateWordNode("Test"))

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><vocabulary>Test</vocabulary></template>", xml_str)


######################################################################################################################
#
class TemplateProgramNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        test_bot = Bot(Brain(BrainConfiguration()), BotConfiguration())

        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateProgramNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        test_bot.brain.properties.add_property("fullname", "testbot")
        test_bot.brain.properties.add_property("version", "1.0.0")

        self.assertEqual(root.resolve(test_bot, "testid"), "testbot 1.0.0")

    def test_to_xml(self):
        root = TemplateNode()
        node = TemplateProgramNode()
        root.append(node)

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><program /></template>", xml_str)


######################################################################################################################
#
class TemplateExplodeNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateExplodeNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        node.append(TemplateWordNode("Hello World"))
        self.assertEqual(root.resolve(self.bot, self.clientid), "H e l l o W o r l d")

    def test_to_xml(self):
        root = TemplateNode()
        node = TemplateExplodeNode()
        root.append(node)
        node.append(TemplateWordNode("Test"))

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><explode>Test</explode></template>", xml_str)


######################################################################################################################
#
class TemplateImplodeNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateImplodeNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        node.append(TemplateWordNode("H e l l o W o r l d"))
        self.assertEqual(root.resolve(self.bot, self.clientid), "HelloWorld")

    def test_to_xml(self):
        root = TemplateNode()
        node = TemplateImplodeNode()
        root.append(node)
        node.append(TemplateWordNode("Test"))

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><implode>Test</implode></template>", xml_str)


#####################################################################################################################
#
class TemplateThatNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateThatNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

    def test_to_xml_defaults(self):
        root = TemplateNode()
        node = TemplateThatNode()
        root.append(node)

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><that /></template>", xml_str)

    def test_node_no_defaults(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateThatNode(position=3, index=2)
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)
        self.assertEqual(2, node.index)
        self.assertEqual(3, node.position)

    def test_to_xml_no_defaults(self):
        root = TemplateNode()
        node = TemplateThatNode(position=2, index=3)
        root.append(node)

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><that index="3" position="2" /></template>', xml_str)


#####################################################################################################################
#
class TemplateThatStarNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateThatStarNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

    def test_to_xml_defaults(self):
        root = TemplateNode()
        node = TemplateThatStarNode()
        root.append(node)

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><thatstar /></template>", xml_str)

    def test_node_no_defaults(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateThatStarNode(position=3, index=2)
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)
        self.assertEqual(2, node.index)
        self.assertEqual(3, node.position)

    def test_to_xml_no_defaults(self):
        root = TemplateNode()
        node = TemplateThatStarNode(position=2, index=3)
        root.append(node)

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><thatstar index="3" position="2" /></template>', xml_str)


#####################################################################################################################
#
class TemplateTopicStarNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateTopicStarNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

    def test_to_xml_defaults(self):
        root = TemplateNode()
        node = TemplateTopicStarNode()
        root.append(node)

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><topicstar /></template>", xml_str)

    def test_node_no_defaults(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateTopicStarNode(position=3, index=2)
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)
        self.assertEqual(2, node.index)
        self.assertEqual(3, node.position)

    def test_to_xml_no_defaults(self):
        root = TemplateNode()
        node = TemplateTopicStarNode(position=2, index=3)
        root.append(node)

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><topicstar index="3" position="2" /></template>', xml_str)


#####################################################################################################################
#
class TemplateInputNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateInputNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        conversation = Conversation("testid", self.bot)
        question = Question.create_from_text("Hello world")
        question.current_sentence()._response = "Hello matey"
        conversation._questions.append(question)
        self.bot._conversations["testid"] = conversation

        response = root.resolve(self.bot, "testid")
        self.assertIsNotNone(response)
        self.assertEqual(response, "Hello world")

    def test_to_xml_defaults(self):
        root = TemplateNode()
        node = TemplateInputNode()
        root.append(node)

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><input /></template>", xml_str)

    def test_node_no_defaults(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateInputNode(position=3, index=2)
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)
        self.assertEqual(2, node.index)
        self.assertEqual(3, node.position)

    def test_to_xml_no_defaults(self):
        root = TemplateNode()
        node = TemplateInputNode(position=2, index=3)
        root.append(node)

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><input index="3" position="2" /></template>', xml_str)


#####################################################################################################################
#
class TemplateRequestNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateRequestNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        conversation = Conversation("testid", self.bot)
        question = Question.create_from_text("Hello world")
        question.current_sentence()._response = "Hello matey"
        conversation._questions.append(question)
        self.bot._conversations["testid"] = conversation

        response = root.resolve(self.bot, "testid")
        self.assertIsNotNone(response)
        self.assertEqual(response, "Hello world")

    def test_to_xml_defaults(self):
        root = TemplateNode()
        node = TemplateRequestNode()
        root.append(node)

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><request /></template>", xml_str)

    def test_node_no_defaults(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateRequestNode(position=3, index=2)
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)
        self.assertEqual(2, node.index)
        self.assertEqual(3, node.position)

    def test_to_xml_no_defaults(self):
        root = TemplateNode()
        node = TemplateRequestNode(position=2, index=3)
        root.append(node)

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><request index="3" position="2" /></template>', xml_str)


#####################################################################################################################
#
class TemplateResponseNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateResponseNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        conversation = Conversation("testid", self.bot)
        question = Question.create_from_text("Hello world")
        question.current_sentence()._response = "Hello Matey"
        conversation._questions.append(question)
        self.bot._conversations["testid"] = conversation

        response = root.resolve(self.bot, "testid")
        self.assertIsNotNone(response)
        self.assertEqual(response, "Hello Matey")

    def test_to_xml_defaults(self):
        root = TemplateNode()
        node = TemplateResponseNode()
        root.append(node)

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><response /></template>", xml_str)

    def test_node_no_defaults(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateResponseNode(position=3, index=2)
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)
        self.assertEqual(2, node.index)
        self.assertEqual(3, node.position)

    def test_to_xml_no_defaults(self):
        root = TemplateNode()
        node = TemplateResponseNode(position=2, index=3)
        root.append(node)

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><response index="3" position="2" /></template>', xml_str)


#####################################################################################################################
#
class TemplateDateNodeTests(TemplateTestsBaseClass):

    DEFAULT_DATETIME_REGEX = "^.{3}\s*.{3}\s*\d{1,}\s\d{2}:\d{2}:\d{2}\s\d{4}"

    def test_node_default_format(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateDateNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)
        self.assertRegex(root.resolve(self.bot, self.clientid), TemplateDateNodeTests.DEFAULT_DATETIME_REGEX)

    def test_node_custom_format(self):
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


#####################################################################################################################
#
class TemplateIntervalNodeTests(TemplateTestsBaseClass):

    def test_node_years(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateIntervalNode()
        node._format = TemplateWordNode("%c")
        node._style = TemplateWordNode("years")
        node._from = TemplateWordNode("Thu Oct  6 16:35:11 2014")
        node._to = TemplateWordNode("Fri Oct  7 16:35:11 2016")

        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        response = root.resolve(self.bot, self.clientid)
        self.assertIsNotNone(response)
        self.assertEqual(response, "2")

    def test_node_months(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateIntervalNode()
        node._format = TemplateWordNode("%c")
        node._style = TemplateWordNode("months")
        node._from = TemplateWordNode("Thu Jul  6 16:35:11 2014")
        node._to = TemplateWordNode("Fri Oct  7 16:35:11 2016")

        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        response = root.resolve(self.bot, self.clientid)
        self.assertIsNotNone(response)
        self.assertEqual(response, "3")

    def test_node_weeks(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateIntervalNode()
        node._format = TemplateWordNode("%c")
        node._style = TemplateWordNode("weeks")
        node._from = TemplateWordNode("Thu Oct  1 16:35:11 2016")
        node._to = TemplateWordNode("Fri Oct  14 16:35:11 2016")

        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        response = root.resolve(self.bot, self.clientid)
        self.assertIsNotNone(response)
        self.assertEqual(response, "1")

    def test_node_days(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateIntervalNode()
        node._format = TemplateWordNode("%c")
        node._style = TemplateWordNode("days")
        node._from = TemplateWordNode("Thu Oct  6 16:35:11 2016")
        node._to = TemplateWordNode("Fri Oct  7 16:35:11 2016")

        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        response = root.resolve(self.bot, self.clientid)
        self.assertIsNotNone(response)
        self.assertEqual(response, "1")

    def test_node_hours(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateIntervalNode()
        node._format = TemplateWordNode("%c")
        node._style = TemplateWordNode("hours")
        node._from = TemplateWordNode("Thu Oct  7 12:35:11 2016")
        node._to = TemplateWordNode("Fri Oct  7 16:35:11 2016")

        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        response = root.resolve(self.bot, self.clientid)
        self.assertIsNotNone(response)
        self.assertEqual(response, "4")

    def test_node_minutes(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateIntervalNode()
        node._format = TemplateWordNode("%c")
        node._style = TemplateWordNode("minutes")
        node._from = TemplateWordNode("Thu Oct 7 16:33:09 2016")
        node._to = TemplateWordNode("Fri Oct 7 16:35:11 2016")

        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        response = root.resolve(self.bot, self.clientid)
        self.assertIsNotNone(response)
        self.assertEqual(response, "2")

    def test_node_seconds(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateIntervalNode()
        node._format = TemplateWordNode("%c")
        node._style = TemplateWordNode("seconds")
        node._from = TemplateWordNode("Thu Oct 7 16:35:09 2016")
        node._to = TemplateWordNode("Fri Oct 7 16:35:11 2016")

        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        response = root.resolve(self.bot, self.clientid)
        self.assertIsNotNone(response)
        self.assertEqual(response, "2")

    def test_node_ymdhms(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateIntervalNode()
        node._format = TemplateWordNode("%c")
        node._style = TemplateWordNode("ymdhms")
        node._from = TemplateWordNode("Thu Jul 14 16:33:09 2014")
        node._to = TemplateWordNode("Fri Oct 7 16:35:11 2016")

        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        response = root.resolve(self.bot, self.clientid)
        self.assertIsNotNone(response)
        self.assertEqual(response, "2 years, 2 months, 23 days, 0 hours, 2 minutes, 2 seconds")

    def test_to_xml(self):
        root = TemplateNode()
        node = TemplateIntervalNode()
        node._format = TemplateWordNode("%c")
        node._style = TemplateWordNode("years")
        node._from = TemplateWordNode("Thu Oct 6 16:35:11 2014")
        node._to = TemplateWordNode("Fri Oct 7 16:35:11 2016")
        root.append(node)

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><interval format="%c" style="years"><from>Thu Oct 6 16:35:11 2014</from><to>Fri Oct 7 16:35:11 2016</to></interval></template>', xml_str)


#####################################################################################################################
#
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


#####################################################################################################################
#
class TemplateSizeNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateSizeNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        response = root.resolve(self.bot, self.clientid)
        self.assertIsNotNone(response)
        self.assertEqual(response, "0")

    def test_to_xml(self):
        root = TemplateNode()
        node = TemplateSizeNode()
        root.append(node)

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><size /></template>", xml_str)


#####################################################################################################################
#
class TemplateEvalNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)

        eval = TemplateEvalNode()
        root.append(eval)

        eval.append(TemplateWordNode("hello"))

        self.assertEqual(len(root.children), 1)

        resolved = root.resolve(self.bot, self.clientid)
        self.assertIsNotNone(resolved)
        self.assertEqual("hello", resolved)

    def test_to_xml(self):
        root = TemplateNode()
        node = TemplateEvalNode()
        root.append(node)
        node.append(TemplateWordNode("Test"))

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><eval>Test</eval></template>", xml_str)


#####################################################################################################################
#
class TemplateLearnNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)

        learn = TemplateLearnNode()
        self.assertIsNotNone(learn)
        learn._pattern = ET.fromstring("<pattern>HELLO LEARN</pattern>")
        learn._topic = ET.fromstring("<topic>*</topic>")
        learn._that = ET.fromstring("<that>*</that>")
        learn._template = TemplateWordNode("LEARN")

        root.append(learn)
        self.assertEqual(1, len(root.children))

        resolved = root.resolve(self.bot, self.clientid)
        self.assertIsNotNone(resolved)
        self.assertEqual("", resolved)

    def test_to_xml(self):
        root = TemplateNode()
        learn = TemplateLearnNode()
        learn._pattern = ET.fromstring("<pattern>HELLO LEARN</pattern>")
        learn._topic = ET.fromstring("<topic>*</topic>")
        learn._that = ET.fromstring("<that>*</that>")
        learn._template = TemplateWordNode("LEARN")
        root.append(learn)

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><learn><pattern>HELLO LEARN</pattern><topic>*</topic><that>*</that><template>LEARN</template></learn></template>", xml_str)


#####################################################################################################################
#
class TemplateLearnfNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)

        learn = TemplateLearnfNode()
        self.assertIsNotNone(learn)
        learn._pattern = ET.fromstring("<pattern>HELLO LEARN</pattern>")
        learn._topic = ET.fromstring("<topic>*</topic>")
        learn._that = ET.fromstring("<that>*</that>")
        learn._template = TemplateWordNode("LEARN")

        root.append(learn)
        self.assertEqual(1, len(root.children))

        self.bot.brain._configuration._aiml_files = BrainFileConfiguration("/tmp", ".aiml", False)

        resolved = root.resolve(self.bot, self.clientid)
        self.assertIsNotNone(resolved)
        self.assertEqual("", resolved)

    def test_to_xml(self):
        root = TemplateNode()
        learn = TemplateLearnfNode()
        learn._pattern = ET.fromstring("<pattern>HELLO LEARN</pattern>")
        learn._topic = ET.fromstring("<topic>*</topic>")
        learn._that = ET.fromstring("<that>*</that>")
        learn._template = TemplateWordNode("LEARN")
        root.append(learn)

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><learnf><pattern>HELLO LEARN</pattern><topic>*</topic><that>*</that><template>LEARN</template></learnf></template>", xml_str)


######################################################################################################################
#
class TemplateNodeMixedTests(TemplateTestsBaseClass):

    def test_multirandom(self):
        root = TemplateNode()
        self.assertIsNotNone(root)

        random1 = TemplateRandomNode()
        random1.append(TemplateWordNode("Test1"))
        random1.append(TemplateWordNode("Test2"))
        self.assertEqual(len(random1.children), 2)

        random2 = TemplateRandomNode()
        random2.append(TemplateWordNode("Test3"))
        random2.append(TemplateWordNode("Test4"))
        self.assertEqual(len(random1.children), 2)

        root.append(random1)
        root.append(random2)

        resolved = root.resolve(self.bot, self.clientid)
        self.assertIsNotNone(resolved)
        self.assertOneOf(resolved, ["Test1 Test3",
                                    "Test1 Test4",
                                    "Test2 Test3",
                                    "Test2 Test4"])

    def test_nestedrandom(self):
        root = TemplateNode()
        self.assertIsNotNone(root)

        random1 = TemplateRandomNode()
        random1.append(TemplateWordNode("Test1"))
        random1.append(TemplateWordNode("Test2"))
        self.assertEqual(len(random1.children), 2)

        random2 = TemplateRandomNode()
        random2.append(TemplateWordNode("Test3"))
        random2.append(TemplateWordNode("Test4"))
        self.assertEqual(len(random1.children), 2)

        random3 = TemplateRandomNode()
        random3.append(random1)
        random3.append(random1)
        random3.append(random2)

        root.append(random3)

        resolved = root.resolve(self.bot, self.clientid)
        self.assertIsNotNone(resolved)
        self.assertOneOf(resolved, ["Test1",
                                    "Test2",
                                    "Test3",
                                    "Test4"])

    def test_mixednodes(self):
        root = TemplateNode()
        self.assertIsNotNone(root)

        random1 = TemplateRandomNode()
        random1.append(TemplateWordNode("Test1"))
        random1.append(TemplateWordNode("Test2"))
        random1.append(TemplateWordNode("Test3"))
        self.assertEqual(len(random1.children), 3)

        root.append(TemplateWordNode("Hello"))
        root.append(random1)
        root.append(TemplateWordNode("World!"))

        self.assertEqual(len(root.children), 3)

        resolved = root.resolve(self.bot, self.clientid)
        self.assertIsNotNone(resolved)
        self.assertOneOf(resolved, ["Hello Test1 World!", "Hello Test2 World!", "Hello Test3 World!"])

    def test_to_xml(self):
        # TODO Add unit testing here
        pass

