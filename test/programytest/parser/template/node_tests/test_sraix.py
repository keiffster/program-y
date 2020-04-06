import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.sraix import TemplateSRAIXNode
from programy.parser.template.nodes.word import TemplateWordNode
from programy.services.base import Service
from programy.services.config import ServiceConfiguration
from programytest.parser.base import ParserTestsBaseClass


class MockService(Service):

    def __init__(self, config):
        Service.__init__(self, config)

    def ask_question(self, context: str, question: str):
        return "asked"


class MockTemplateSRAIXNode(TemplateSRAIXNode):
    def __init__(self):
        TemplateSRAIXNode.__init__(self)

    def resolve_to_string(self, context):
        raise Exception("This is an error")


class TemplateSRAIXNodeTests(ParserTestsBaseClass):

    def test_node_unsupported_attributes(self):
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

        self.assertEqual("[SRAIX (service=api)]", node.to_string())

    def test_node_service(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateSRAIXNode()
        self.assertIsNotNone(node)
        node.service = "api"
        self.assertEqual("api", node.service)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        self.assertEqual("[SRAIX (service=api)]", node.to_string())

    def test_node_no_service(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateSRAIXNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        self.assertEqual("[SRAIX ()]", node.to_string())

    def test_to_xml_service(self):
        root = TemplateNode()

        node = TemplateSRAIXNode()
        node.service = "api"

        root.append(node)
        node.append(TemplateWordNode("Hello"))

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><sraix service="api">Hello</sraix></template>', xml_str)

    def test_to_xml_no_service(self):
        root = TemplateNode()

        node = TemplateSRAIXNode()

        root.append(node)
        node.append(TemplateWordNode("Hello"))

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><sraix>Hello</sraix></template>', xml_str)

    def test_call_service(self):

        self._client_context.brain.service_handler.add_service("mock", MockService(ServiceConfiguration(service_type='library')))

        root = TemplateNode()

        node = TemplateSRAIXNode()
        node.service = "mock"
        root.append(node)
        node.append(TemplateWordNode("Hello"))

        self.assertEqual("asked", node.resolve(self._client_context))

    def test_call_no_service_exists(self):

        root = TemplateNode()

        node = TemplateSRAIXNode()
        node.service = "mock"
        root.append(node)
        node.append(TemplateWordNode("Hello"))

        self.assertEqual("", node.resolve(self._client_context))

    def test_call_no_service_defined(self):

        root = TemplateNode()

        node = TemplateSRAIXNode()
        root.append(node)
        node.append(TemplateWordNode("Hello"))

        self.assertEqual("", node.resolve(self._client_context))

    def test_node_exception_handling(self):
        root = TemplateNode()
        node = MockTemplateSRAIXNode()
        root.append(node)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)