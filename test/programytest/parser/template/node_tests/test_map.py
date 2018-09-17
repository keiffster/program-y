import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.map import TemplateMapNode
from programy.parser.template.nodes.word import TemplateWordNode

from programytest.parser.base import ParserTestsBaseClass


class MockTemplateMapNode(TemplateMapNode):
    def __init__(self):
        TemplateMapNode.__init__(self)

    def resolve_to_string(self, context):
        raise Exception("This is an error")


class TemplateMapNodeTests(ParserTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateMapNode()
        self.assertEqual("", node.resolve_children(self._client_context))

        node.name = TemplateWordNode("COLOURS")
        node.append(TemplateWordNode("BLACK"))

        root.append(node)
        self.assertEqual(len(root.children), 1)

        self._client_context.brain.maps._maps['COLOURS'] = {'BLACK': 'WHITE'}

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("WHITE", result)

    def test_no_var_defaultmap_set(self):
        self._client_context.brain.maps._maps['COLOURS'] = {'BLACK': 'WHITE'}
        self._client_context.brain.properties.add_property('default-map', "test_value")

        node = TemplateMapNode()
        node.name = TemplateWordNode("COLOURS")
        node.append(TemplateWordNode("UNKNOWN"))
        root = TemplateNode()
        root.append(node)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("test_value", result)

    def test_no_var_defaultmap_not_set(self):
        self._client_context.brain.maps._maps['COLOURS'] = {'BLACK': 'WHITE'}

        node = TemplateMapNode()
        node.name = TemplateWordNode("COLOURS")
        node.append(TemplateWordNode("UNKNOWN"))
        root = TemplateNode()
        root.append(node)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)

    def test_no_map_for_name_defaultmap_set(self):
        self._client_context.brain.maps._maps['COLOURS'] = {'BLACK': 'WHITE'}
        self._client_context.brain.properties.add_property('default-map', "test_value")

        node = TemplateMapNode()
        node.name = TemplateWordNode("UNKNOWN")
        node.append(TemplateWordNode("BLACK"))
        root = TemplateNode()
        root.append(node)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("test_value", result)

    def test_no_map_for_name_defaultmap_not_set(self):
        self._client_context.brain.maps._maps['COLOURS'] = {'BLACK': 'WHITE'}

        node = TemplateMapNode()
        node.name = TemplateWordNode("UNKNOWN")
        node.append(TemplateWordNode("BLACK"))
        root = TemplateNode()
        root.append(node)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)

    def test_internal_map_plural(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateMapNode()
        node.name = TemplateWordNode("PLURAL")
        node.append(TemplateWordNode("HORSE"))

        root.append(node)
        self.assertEqual(len(root.children), 1)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("HORSES", result)

    def test_internal_map_singular(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateMapNode()
        node.name = TemplateWordNode("SINGULAR")
        node.append(TemplateWordNode("HORSES"))

        root.append(node)
        self.assertEqual(len(root.children), 1)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("HORSE", result)

    def test_internal_map_predecessor(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateMapNode()
        node.name = TemplateWordNode("PREDECESSOR")
        node.append(TemplateWordNode("2"))

        root.append(node)
        self.assertEqual(len(root.children), 1)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("1", result)

    def test_internal_map_succesor(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateMapNode()
        node.name = TemplateWordNode("SUCCESSOR")
        node.append(TemplateWordNode("1"))

        root.append(node)
        self.assertEqual(len(root.children), 1)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("2", result)

    def test_to_xml(self):
        root = TemplateNode()
        node = TemplateMapNode()
        node.name = TemplateWordNode("COLOURS")
        node.append(TemplateWordNode("BLACK"))
        root.append(node)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><map name="COLOURS">BLACK</map></template>', xml_str)

    def test_node_exception_handling(self):
        root = TemplateNode()
        node = MockTemplateMapNode()
        root.append(node)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)