import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.authorise import TemplateAuthoriseNode
from programy.parser.template.nodes.word import TemplateWordNode

from programytest.parser.base import ParserTestsBaseClass


class MockTemplateAuthoriseNode(TemplateAuthoriseNode):

    def __init__(self):
        TemplateAuthoriseNode.__init__(self)

    def resolve_to_string(self, context):
        raise Exception ("This is a failure")

class TemplateAuthoriseNodeTests(ParserTestsBaseClass):

    def test_node_init(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateAuthoriseNode()
        node.role = "root"
        self.assertIsNotNone(node)
        self.assertEqual("root", node.role)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        self.assertEqual("[AUTHORISE (role=root)]", node.to_string())

    def test_node_init_optiona_srai(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateAuthoriseNode()
        node.role = "root"
        self.assertIsNotNone(node)
        self.assertEqual("root", node.role)

        node.denied_srai = "ACCESS_DENIED"
        self.assertIsNotNone(node)
        self.assertEqual("ACCESS_DENIED", node.denied_srai)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        self.assertEqual("[AUTHORISE (role=root, denied_srai=ACCESS_DENIED)]", node.to_string())

    def test_to_xml_service_no_content(self):
        root = TemplateNode()

        node = TemplateAuthoriseNode()
        node.role = "root"
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><authorise role="root" /></template>', xml_str)

    def test_to_xml_service_with_content(self):
        root = TemplateNode()

        node = TemplateAuthoriseNode()
        node.role = "root"
        self.assertIsNotNone(node)

        node.append(TemplateWordNode("Hello"))

        root.append(node)
        self.assertEqual(len(root.children), 1)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><authorise role="root">Hello</authorise></template>', xml_str)

    def test_to_xml_service_no_content_and_optional_srai(self):
        root = TemplateNode()

        node = TemplateAuthoriseNode()
        node.role = "root"
        node.denied_srai = "ACCESS_DENIED"
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><authorise denied_srai="ACCESS_DENIED" role="root" /></template>', xml_str)

    def test_node_exception_handling(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = MockTemplateAuthoriseNode()
        node.role = "root"
        self.assertIsNotNone(node)
        self.assertEqual("root", node.role)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        with self.assertRaises(Exception):
            node.resolve_to_string(self._client_context)

        self.assertEqual("", root.resolve(self._client_context))
