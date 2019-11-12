import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.rest import TemplateRestNode
from programy.parser.template.nodes.word import TemplateWordNode
from programytest.parser.base import ParserTestsBaseClass


class MockTemplateRestNode(TemplateRestNode):
    def __init__(self):
        TemplateRestNode.__init__(self)

    def resolve_to_string(self, context):
        raise Exception("This is an error")


class MockJSONTemplateRestNode(TemplateRestNode):
    def __init__(self, json):
        TemplateRestNode.__init__(self)
        self._json = json

    def resolve_children_to_string(self, context):
        return self._json


class TemplateRestNodeTests(ParserTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateRestNode()
        self.assertIsNotNone(node)

        root.append(node)
        word1 = TemplateWordNode("Word1")
        node.append(word1)
        word2 = TemplateWordNode("Word2")
        node.append(word2)
        word3 = TemplateWordNode("Word3")
        node.append(word3)

        self.assertEqual(root.resolve(self._client_context), "Word2 Word3")

    def test_node_one_word(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateRestNode()
        self.assertIsNotNone(node)

        root.append(node)
        word1 = TemplateWordNode("Word1")
        node.append(word1)

        self.assertEqual(root.resolve(self._client_context), "NIL")

    def test_to_xml(self):
        root = TemplateNode()
        node = TemplateRestNode()
        root.append(node)
        word1 = TemplateWordNode("Word1")
        node.append(word1)
        word2 = TemplateWordNode("Word2")
        node.append(word2)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><rest>Word1 Word2</rest></template>", xml_str)

    def test_node_no_words(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateRestNode()
        self.assertIsNotNone(node)

        root.append(node)

        self.assertEqual(root.resolve(self._client_context), "NIL")

    def test_to_xml_no_words(self):
        root = TemplateNode()
        node = TemplateRestNode()
        root.append(node)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><rest /></template>", xml_str)

    def test_node_exception_handling(self):
        root = TemplateNode()
        node = MockTemplateRestNode()
        root.append(node)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)

    def test_valid_json_not_list(self):
        rest = MockJSONTemplateRestNode('{"test": "value"}')

        self.assertEquals('"value"}', rest.resolve(self._client_context))

    def test_valid_json_list(self):
        rest = MockJSONTemplateRestNode('[{"test1": "value1"}, {"test2": "value2"}, {"test3": "value3"}]')

        self.assertEquals('[{"test2": "value2"}, {"test3": "value3"}]', rest.resolve(self._client_context))

    def test_invalid_json_no_value(self):
        rest = MockJSONTemplateRestNode('test')

        self.assertEquals('NIL', rest.resolve(self._client_context))

    def test_invalid_json(self):
        rest = MockJSONTemplateRestNode('test value')

        self.assertEquals('value', rest.resolve(self._client_context))

    def test_invalid_json_multi(self):
        rest = MockJSONTemplateRestNode('test value value2')

        self.assertEquals('value value2', rest.resolve(self._client_context))