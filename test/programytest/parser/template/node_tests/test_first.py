import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.first import TemplateFirstNode
from programy.parser.template.nodes.word import TemplateWordNode
from programytest.parser.base import ParserTestsBaseClass


class MockTemplateFirstNode(TemplateFirstNode):
    def __init__(self):
        TemplateFirstNode.__init__(self)

    def resolve_to_string(self, context):
        raise Exception("This is an error")


class MockJSONTemplateFirstNode(TemplateFirstNode):
    def __init__(self, json):
        TemplateFirstNode.__init__(self)
        self._json = json

    def resolve_children_to_string(self, context):
        return self._json


class TemplateFirstNodeTests(ParserTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateFirstNode()
        self.assertIsNotNone(node)

        root.append(node)
        word1 = TemplateWordNode("Word1")
        node.append(word1)
        word2 = TemplateWordNode("Word2")
        node.append(word2)
        word3 = TemplateWordNode("Word3")
        node.append(word3)

        self.assertEqual(root.resolve(self._client_context), "Word1")

    def test_to_xml(self):
        root = TemplateNode()
        node = TemplateFirstNode()
        root.append(node)
        word1 = TemplateWordNode("Word1")
        node.append(word1)
        word2 = TemplateWordNode("Word2")
        node.append(word2)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><first>Word1 Word2</first></template>", xml_str)

    def test_to_xml_no_words(self):
        root = TemplateNode()
        node = TemplateFirstNode()
        root.append(node)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><first /></template>", xml_str)

    def test_node_exception_handling(self):
        root = TemplateNode()
        node = MockTemplateFirstNode()
        root.append(node)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)

    def test_node_no_words(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateFirstNode()
        self.assertIsNotNone(node)

        root.append(node)

        self.assertEqual(root.resolve(self._client_context), "NIL")

    def test_node_invalid_json_words(self):
        node = TemplateFirstNode()
        self.assertIsNotNone(node)

        node.append(TemplateWordNode("Rubbish not json"))

        self.assertEqual(node.resolve(self._client_context), "Rubbish")

    def test_node_invalid_json_word(self):
        node = TemplateFirstNode()
        self.assertIsNotNone(node)

        node.append(TemplateWordNode("Rubbish"))

        self.assertEqual(node.resolve(self._client_context), "Rubbish")

    def test_valid_json_not_list(self):
        rest = MockJSONTemplateFirstNode('{"test": "value"}')
        self.assertEquals('{"test":', rest.resolve(self._client_context))

    def test_valid_json_empty_list(self):
        rest = MockJSONTemplateFirstNode('[]')
        self.assertEquals('NIL', rest.resolve(self._client_context))

    def test_valid_json_list(self):
        rest = MockJSONTemplateFirstNode('[{"test1": "value1"}, {"test2": "value2"}, {"test3": "value3"}]')
        self.assertEquals('{"test1": "value1"}', rest.resolve(self._client_context))

    def test_valid_json_list_one_item(self):
        rest = MockJSONTemplateFirstNode('[{"test1": "value1"}]')
        self.assertEquals('{"test1": "value1"}', rest.resolve(self._client_context))

    def test_invalid_json_no_value(self):
        rest = MockJSONTemplateFirstNode('test')
        self.assertEquals('test', rest.resolve(self._client_context))

    def test_invalid_json_empty(self):
        rest = MockJSONTemplateFirstNode('  ')
        self.assertEquals('NIL', rest.resolve(self._client_context))

    def test_invalid_json_one_item(self):
        rest = MockJSONTemplateFirstNode('test')
        self.assertEquals('test', rest.resolve(self._client_context))

    def test_invalid_json(self):
        rest = MockJSONTemplateFirstNode('test value')
        self.assertEquals('test', rest.resolve(self._client_context))

    def test_invalid_json_multi(self):
        rest = MockJSONTemplateFirstNode('test value value2')
        self.assertEquals('test', rest.resolve(self._client_context))
