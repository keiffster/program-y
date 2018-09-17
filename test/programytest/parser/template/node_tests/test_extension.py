import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.extension import TemplateExtensionNode
from programy.parser.template.nodes.word import TemplateWordNode

from programytest.parser.base import ParserTestsBaseClass


class MockExtension(object):

    def execute(self, context, data):
        if data is None or data is "":
            return "VALID"
        else:
            return data


class MockTemplateExtensionNode(TemplateExtensionNode):
    def __init__(self):
        TemplateExtensionNode.__init__(self)

    def resolve_to_string(self, context):
        raise Exception("This is an error")


class TemplateExtensionNodeTests(ParserTestsBaseClass):

    def test_node_no_data(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateExtensionNode()
        self.assertIsNotNone(node)
        self.assertIsNone(node.path)

        node.path = "programytest.parser.template.node_tests.test_extension.MockExtension"
        self.assertEqual("programytest.parser.template.node_tests.test_extension.MockExtension", node.path)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        self.assertEqual(root.resolve(self._client_context), "VALID")

    def test_node_with_data(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateExtensionNode()
        self.assertIsNotNone(node)
        self.assertIsNone(node.path)

        node.append(TemplateWordNode("Test"))

        node.path = "programytest.parser.template.node_tests.test_extension.MockExtension"
        self.assertEqual("programytest.parser.template.node_tests.test_extension.MockExtension", node.path)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        self.assertEqual(root.resolve(self._client_context), "Test")

    def test_node_invalid_class(self):
        root = TemplateNode()
        node = TemplateExtensionNode()
        node.path = "programytest.parser.template.node_tests.test_extension.MockExtensionOther"
        root.append(node)
        self.assertEqual(root.resolve(self._client_context), "")


    def test_to_xml(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateExtensionNode()
        node.path = "programytest.parser.template.node_tests.test_extension.MockExtension"
        node.append(TemplateWordNode("Test"))
        root.append(node)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><extension path="programytest.parser.template.node_tests.test_extension.MockExtension">Test</extension></template>', xml_str)

    def test_node_exception_handling(self):
        root = TemplateNode()
        node = MockTemplateExtensionNode()
        root.append(node)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)