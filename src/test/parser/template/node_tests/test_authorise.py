import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.sraix import TemplateAuthoriseNode
from programy.parser.template.nodes.word import TemplateWordNode
from programy.utils.services.service import Service, ServiceFactory
from programy.config.sections.brain.brain import BrainConfiguration
from programy.config.sections.brain.service import BrainServiceConfiguration

from test.parser.template.base import TemplateTestsBaseClass

class TemplateAuthoriseNodeTests(TemplateTestsBaseClass):

    def test_node_unsupported_attributes(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateAuthoriseNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        self.assertEqual("AUTHORISE ()", node.to_string())

    def test_node_user(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateAuthoriseNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        self.assertEqual("AUTHORISE ()", node.to_string())

    def test_node_role(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateAuthoriseNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        self.assertEqual("AUTHORISE ()", node.to_string())

    def test_node_group(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateAuthoriseNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        self.assertEqual("AUTHORISE ()", node.to_string())

    def test_node_no_attribs(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateAuthoriseNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        self.assertEqual("AUTHORISE ()", node.to_string())

    def test_to_xml_service(self):
        root = TemplateNode()

        node = TemplateAuthoriseNode()
        node.service = "api"

        root.append(node)
        node.append(TemplateWordNode("Hello"))

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><sraix service="api">Hello</sraix></template>', xml_str)

