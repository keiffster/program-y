import xml.etree.ElementTree as ET
import os

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.word import TemplateWordNode
from programy.parser.template.nodes.system import TemplateSystemNode
from programy.parser.exceptions import ParserException

from programytest.parser.base import ParserTestsBaseClass


class MockTemplateSystemNode(TemplateSystemNode):
    def __init__(self):
        TemplateSystemNode.__init__(self)

    def resolve_to_string(self, context):
        raise Exception("This is an error")


class TemplateSystemNodeTests(ParserTestsBaseClass):

    def test_node_no_timeout(self):

        self._client_context.brain.configuration.overrides._allow_system_aiml = True

        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateSystemNode()
        self.assertIsNotNone(node)
        node.append(TemplateWordNode('echo "Hello World"'))

        root.append(node)
        self.assertEqual(len(root.children), 1)

        response = root.resolve(self._client_context)
        self.assertIsNotNone(response)

        if os.name == 'posix':
            self.assertEqual(response, "Hello World")
        elif os.name == 'nt':
                self.assertEqual(response, '"Hello World"')
        else:
            self.assertFalse(True)

    def test_node_with_timeout(self):

        self._client_context.brain.configuration.overrides._allow_system_aiml = True

        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateSystemNode()
        node.timeout = 1000
        self.assertIsNotNone(node)
        node.append(TemplateWordNode('echo "Hello World"'))

        root.append(node)
        self.assertEqual(len(root.children), 1)

        response = root.resolve(self._client_context)
        self.assertIsNotNone(response)
        if os.name == 'posix':
            self.assertEqual(response, "Hello World")
        elif os.name == 'nt':
                self.assertEqual(response, '"Hello World"')
        else:
            self.assertFalse(True)

    def test_node_with_system_switched_off(self):

        self._client_context.brain.configuration.overrides._allow_system_aiml = False

        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateSystemNode()
        node.timeout = 1000
        self.assertIsNotNone(node)
        node.append(TemplateWordNode('echo "Hello World"'))

        root.append(node)
        self.assertEqual(len(root.children), 1)

        response = root.resolve(self._client_context)
        self.assertIsNotNone(response)
        self.assertEqual(response, "")

    def test_set_attrib(self):
        node = TemplateSystemNode()
        node.set_attrib("timeout", TemplateWordNode("1000"))
        self.assertEqual("1000", node._timeout.word)

        with self.assertRaises(ParserException):
            node.set_attrib("unknown", 1000)

    def test_to_xml_no_timeout(self):
        root = TemplateNode()
        node = TemplateSystemNode()
        root.append(node)
        node.append(TemplateWordNode('echo "Hello World"'))

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><system>echo "Hello World"</system></template>', xml_str)

    def test_to_xml_with_timeout(self):
        root = TemplateNode()
        node = TemplateSystemNode()
        root.append(node)
        node.append(TemplateWordNode('echo "Hello World"'))

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><system>echo "Hello World"</system></template>', xml_str)

    def test_node_exception_handling(self):
        root = TemplateNode()
        node = MockTemplateSystemNode()
        root.append(node)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)