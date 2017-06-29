import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.extension import TemplateExtensionNode
from programy.parser.template.nodes.word import TemplateWordNode

from test.parser.template.base import TemplateTestsBaseClass

class MockExtension(object):
    def execute(self, bot, clientid, data):
        if data is None or data is "":
            return "VALID"
        else:
            return data

class TemplateExtensionNodeTests(TemplateTestsBaseClass):

    def test_node_no_data(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateExtensionNode()
        self.assertIsNotNone(node)
        self.assertIsNone(node.path)

        node.path = "test.parser.template.node_tests.test_extension.MockExtension"
        self.assertEqual("test.parser.template.node_tests.test_extension.MockExtension", node.path)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        self.assertEqual(root.resolve(self.bot, self.clientid), "VALID")

    def test_node_with_data(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateExtensionNode()
        self.assertIsNotNone(node)
        self.assertIsNone(node.path)

        node.append(TemplateWordNode("Test"))

        node.path = "test.parser.template.node_tests.test_extension.MockExtension"
        self.assertEqual("test.parser.template.node_tests.test_extension.MockExtension", node.path)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        self.assertEqual(root.resolve(self.bot, self.clientid), "Test")

    def test_node_invalid_class(self):
        root = TemplateNode()
        node = TemplateExtensionNode()
        node.path = "test.parser.template.node_tests.test_extension.MockExtensionOther"
        root.append(node)
        self.assertEqual(root.resolve(self.bot, self.clientid), "")


    def test_to_xml(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateExtensionNode()
        node.path = "test.parser.template.node_tests.test_extension.MockExtension"
        node.append(TemplateWordNode("Test"))
        root.append(node)

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><extension path="test.parser.template.node_tests.test_extension.MockExtension">Test</extension></template>', xml_str)
