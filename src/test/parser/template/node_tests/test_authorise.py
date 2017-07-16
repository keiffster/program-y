import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.sraix import TemplateSRAIXNode
from programy.parser.template.nodes.word import TemplateWordNode
from programy.utils.services.service import Service, ServiceFactory
from programy.config.sections.brain.brain import BrainConfiguration
from programy.config.sections.brain.service import BrainServiceConfiguration

from test.parser.template.base import TemplateTestsBaseClass


class MockService(Service):

    def __init__(self, config):
        Service.__init__(self, config)

    def ask_question(self, bot, clientid: str, question: str):
        return "asked"

class TemplateSRAIXNodeTests(TemplateTestsBaseClass):

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

        self.assertEqual("SRAIX (service=api)", node.to_string())

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

        self.assertEqual("SRAIX (service=api)", node.to_string())

    def test_node_no_service(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateSRAIXNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        self.assertEqual("SRAIX ()", node.to_string())

    def test_to_xml_service(self):
        root = TemplateNode()

        node = TemplateSRAIXNode()
        node.service = "api"

        root.append(node)
        node.append(TemplateWordNode("Hello"))

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><sraix service="api">Hello</sraix></template>', xml_str)

    def test_to_xml_no_service(self):
        root = TemplateNode()

        node = TemplateSRAIXNode()

        root.append(node)
        node.append(TemplateWordNode("Hello"))

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><sraix>Hello</sraix></template>', xml_str)

    def test_call_service(self):

        service_config = BrainServiceConfiguration("mock")
        service_config._classname = 'test.utils.services.test_service.MockService'

        brain_config = BrainConfiguration()
        brain_config.services._services['mock'] = service_config

        ServiceFactory.preload_services(brain_config.services)

        root = TemplateNode()

        node = TemplateSRAIXNode()
        node.service = "mock"
        root.append(node)
        node.append(TemplateWordNode("Hello"))

        self.assertEqual("asked", node.resolve(self.bot, self.clientid))

    def test_call_no_service_exists(self):

        root = TemplateNode()

        node = TemplateSRAIXNode()
        node.service = "mock"
        root.append(node)
        node.append(TemplateWordNode("Hello"))

        self.assertEqual("", node.resolve(self.bot, self.clientid))

    def test_call_no_service_defined(self):

        root = TemplateNode()

        node = TemplateSRAIXNode()
        root.append(node)
        node.append(TemplateWordNode("Hello"))

        self.assertEqual("", node.resolve(self.bot, self.clientid))
