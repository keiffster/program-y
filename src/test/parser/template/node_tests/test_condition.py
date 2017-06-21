import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.word import TemplateWordNode
from programy.parser.template.nodes.condition import TemplateConditionNode, TemplateConditionListItemNode
from programy.dialog import Question

from test.parser.template.base import TemplateTestsBaseClass


class TemplateConditionNodeTests(TemplateTestsBaseClass):

    def test_type1_node_global_match(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateConditionNode("name1", TemplateWordNode("value1"), local=False)
        self.assertIsNotNone(node)

        node.append(TemplateWordNode("Hello"))
        root.append(node)
        self.assertEqual(len(root.children), 1)

        self.bot.conversation(self.clientid)._predicates['name1'] = "value1"

        result = root.resolve(self.bot, self.clientid)
        self.assertIsNotNone(result)
        self.assertEqual(result, "Hello")

    def test_type1_node_global_nomatch(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateConditionNode("name1", TemplateWordNode("value1"), local=False)
        self.assertIsNotNone(node)

        node.append(TemplateWordNode("Hello"))
        root.append(node)
        self.assertEqual(len(root.children), 1)

        self.bot.conversation(self.clientid)._predicates['name1'] = "value2"

        result = root.resolve(self.bot, self.clientid)
        self.assertIsNotNone(result)
        self.assertEqual(result, "")

    def test_type1_node_local_match(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateConditionNode("var1", TemplateWordNode("value1"), local=True)
        self.assertIsNotNone(node)

        node.append(TemplateWordNode("Hello"))
        root.append(node)
        self.assertEqual(len(root.children), 1)

        question = Question.create_from_text("Hello")
        self.bot.conversation(self.clientid).record_dialog(question)
        self.bot.conversation(self.clientid).current_question().set_predicate("var1", "value1")

        result = root.resolve(self.bot, self.clientid)
        self.assertIsNotNone(result)
        self.assertEqual(result, "Hello")

    def test_type1_node_local_nomatch(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateConditionNode("var1", TemplateWordNode("value1"), local=True)
        self.assertIsNotNone(node)

        node.append(TemplateWordNode("Hello"))
        root.append(node)
        self.assertEqual(len(root.children), 1)

        question = Question.create_from_text("Hello")
        self.bot.conversation(self.clientid).record_dialog(question)
        self.bot.conversation(self.clientid).current_question().set_predicate("var1", "value2")

        result = root.resolve(self.bot, self.clientid)
        self.assertIsNotNone(result)
        self.assertEqual(result, "")

    def test_type1_to_xml_global(self):
        root = TemplateNode()
        node = TemplateConditionNode("name1", TemplateWordNode("value1"), local=False)
        node.append(TemplateWordNode("Hello"))
        root.append(node)

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><condition name="name1"><value>value1</value>Hello</condition></template>', xml_str)

    def test_type1_to_xml_local(self):
        root = TemplateNode()
        node = TemplateConditionNode("name1", TemplateWordNode("value1"), local=True)
        node.append(TemplateWordNode("Hello"))
        root.append(node)

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><condition var="name1"><value>value1</value>Hello</condition></template>', xml_str)

    def test_type2_node_global(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateConditionNode("cond1", type=2)
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

        self.bot.conversation(self.clientid)._predicates['cond1'] = "value2"

        question = Question.create_from_text("Hello")
        self.bot.conversation(self.clientid).record_dialog(question)
        self.bot.conversation(self.clientid).current_question().set_predicate("cond1", "value2")

        result = root.resolve(self.bot, self.clientid)
        self.assertIsNotNone(result)
        self.assertEqual("Word2", result)

    def test_type2_node_local(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateConditionNode("var1", local=True, type=2)
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

        question = Question.create_from_text("Hello")
        self.bot.conversation(self.clientid).record_dialog(question)
        self.bot.conversation(self.clientid).current_question().set_predicate("var1", "value2")

        result = root.resolve(self.bot, self.clientid)
        self.assertIsNotNone(result)
        self.assertEqual("Word2", result)

    # TODO Add unit aiml_tests for <loop /> construct

    def test_type2_to_xml_global(self):
        root = TemplateNode()

        node = TemplateConditionNode("cond1", type=2)
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

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><condition name="cond1"><li><value>value1</value>Word1</li><li><value>value2</value>Word2</li><li>Word3</li></condition></template>', xml_str)

    def test_type2_to_xml_local(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateConditionNode("var1", local=True, type=2)
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

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><condition var="var1"><li><value>value1</value>Word1</li><li><value>value2</value>Word2</li><li>Word3</li></condition></template>', xml_str)

    def test_type3_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateConditionNode(type=3)
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

    # TODO Add unit aiml_tests for <loop /> construct

    def test_type3_to_xml(self):
        root = TemplateNode()

        node = TemplateConditionNode(type=3)
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

