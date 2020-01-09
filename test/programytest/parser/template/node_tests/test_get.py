import xml.etree.ElementTree as ET

from programy.dialog.question import Question
from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.get import TemplateGetNode
from programy.parser.template.nodes.select import TemplateSelectNode
from programy.parser.template.nodes.word import TemplateWordNode
from programytest.parser.base import ParserTestsBaseClass


class MockTemplateGetNode(TemplateGetNode):
    def __init__(self):
        TemplateGetNode.__init__(self)

    def resolve_to_string(self, context):
        raise Exception("This is an error")


class TemplateGetNodeTests(ParserTestsBaseClass):

    def test_decode_tuples_as_json_list(self):
        self.assertEqual([[["x","1"], ["y","2"], ["z", "3"]]], TemplateGetNode.decode_tuples('[[["x","1"], ["y","2"], ["z", "3"]]]'))

    def test_decode_tuples_as_list(self):
        self.assertEqual([[["x","1"], ["y","2"], ["z", "3"]]], TemplateGetNode.decode_tuples([[["x","1"], ["y","2"], ["z", "3"]]]))

    def test_get_tuples(self):
        node = TemplateGetNode()
        node.tuples = TemplateWordNode('[[["x","1"], ["y","2"], ["z", "3"]]]')
        self.assertEquals([[["x","1"], ["y","2"], ["z", "3"]]], node._get_tuples(self._client_context))

    def test_get_tuples_invalid_json(self):
        node = TemplateGetNode()
        node.tuples = TemplateWordNode('"1", "2", "3"')
        self.assertEquals([], node._get_tuples(self._client_context))

    def test_default_value_properties(self):
        self._client_context.bot.brain.properties.add_property("default_get", "test123")
        self.assertEqual("test123", TemplateGetNode.get_default_value(self._client_context))

    def test_default_value_default_get(self):
        self._client_context.bot.brain.configuration.defaults._default_get = "test456"
        self.assertEqual("test456", TemplateGetNode.get_default_value(self._client_context))

    def test_default_value_no_value(self):
        self._client_context.bot.brain.configuration.defaults._default_get = None
        self.assertEqual("unknown", TemplateGetNode.get_default_value(self._client_context))

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

        conversation = self._client_context.bot.get_conversation(self._client_context)
        self.assertIsNotNone(conversation)
        question = Question.create_from_text(self._client_context, "Hello", self._client_context.bot.sentence_splitter)
        conversation.record_dialog(question)
        self.assertIsNotNone(conversation.current_question())
        question.set_property("name", "keith")

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("keith", result)

    def test_to_xml_local_get(self):
        root = TemplateNode()
        node = TemplateGetNode()
        node.name = TemplateWordNode("name")
        node.local = True
        root.append(node)

        xml = root.xml_tree(self._client_context)
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

        self._client_context.brain.properties.add_property("default_get", "unknown")

        conversation = self._client_context.bot.get_conversation(self._client_context)
        self.assertIsNotNone(conversation)
        question = Question.create_from_text(self._client_context, "Hello", self._client_context.bot.sentence_splitter)
        conversation.record_dialog(question)

        result = root.resolve(self._client_context)
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

        conversation = self._client_context.bot.get_conversation(self._client_context)
        self.assertIsNotNone(conversation)
        question = Question.create_from_text(self._client_context, "Hello", self._client_context.bot.sentence_splitter)
        conversation.record_dialog(question)
        self.assertIsNotNone(conversation.current_question())
        conversation.set_property("name", "keith")

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("keith", result)

    def test_to_xml_global_get(self):
        root = TemplateNode()
        node = TemplateGetNode()
        node.name = TemplateWordNode("name")
        node.local = False
        root.append(node)

        xml = root.xml_tree(self._client_context)
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
        self.assertEqual("[GET [Global] - [WORD]name]", node.to_string())

        root.append(node)
        self.assertEqual(len(root.children), 1)

        self._client_context.brain.properties.add_property("default_get", "unknown")

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("unknown", result)

    def test_global_no_name(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateGetNode()
        node.append(TemplateWordNode("Fred"))
        self.assertIsNotNone(node)
        self.assertEqual("[GET [Global] - None]", node.to_string())

        root.append(node)
        self.assertEqual(len(root.children), 1)

        self._client_context.brain.properties.add_property("default_get", "unknown")

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)

    def test_tuples_no_tuples(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        select = TemplateSelectNode()
        self.assertIsNotNone(select)

        node = TemplateGetNode()
        node.name = TemplateWordNode("?x ?y")
        node.tuples = select

        root.append(node)
        self.assertEqual(len(root.children), 1)

        self.assertEqual("[GET [Tuples] - ([WORD]?x ?y)]", node.to_string())

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><get var="?x ?y"><select /></get></template>', xml_str)

        result = root.resolve_to_string(self._client_context)
        self.assertEquals("unknown", result)

    def test_tuples_string(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        select = TemplateWordNode("Hello")
        self.assertIsNotNone(select)

        node = TemplateGetNode()
        node.name = TemplateWordNode("?x ?y")
        node.tuples = select

        root.append(node)
        self.assertEqual(len(root.children), 1)

        self.assertEqual("[GET [Tuples] - ([WORD]?x ?y)]", node.to_string())

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><get var="?x ?y">Hello</get></template>', xml_str)

        result = root.resolve_to_string(self._client_context)

    def test_node_exception_handling(self):
        root = TemplateNode()
        node = MockTemplateGetNode()
        root.append(node)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)

    def test_resolve_tuple_no_data(self):
        node = TemplateGetNode()
        node.name = TemplateWordNode("x")
        node.tuples = TemplateWordNode("")
        self.assertEqual("unknown", node.resolve_tuple(self._client_context))

    def test_resolve_tuple_as_results_no_vars(self):
        node = TemplateGetNode()
        node.tuples = TemplateWordNode('[[["x","1"], ["y","2"], ["z", "3"]]]')
        self.assertEqual("1 2 3", node.resolve_tuple(self._client_context))

    def test_resolve_tuple_as_results_with_vars(self):
        node = TemplateGetNode()
        node.name = TemplateWordNode("x")
        node.tuples = TemplateWordNode('[[["x","1"], ["y","2"], ["z", "3"]]]')
        self.assertEqual("1", node.resolve_tuple(self._client_context))

    def test_resolve_tuple_as_data_with_vars(self):
        node = TemplateGetNode()
        node.name = TemplateWordNode("x")
        node.tuples = TemplateWordNode('[["x", "1"]]')
        self.assertEqual("1", node.resolve_tuple(self._client_context))

    def test_resolve_tuple_as_data_with_vars_mismatch(self):
        node = TemplateGetNode()
        node.name = TemplateWordNode("y")
        node.tuples = TemplateWordNode('[["x", "1"]]')
        self.assertEqual("unknown", node.resolve_tuple(self._client_context))

    def test_resolve_tuple_as_results_with_vars_mismatch(self):
        node = TemplateGetNode()
        node.name = TemplateWordNode("a")
        node.tuples = TemplateWordNode('[[["x","1"], ["y","2"], ["z", "3"]]]')
        self.assertEqual("unknown", node.resolve_tuple(self._client_context))
