import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.log import TemplateLogNode
from programy.parser.template.nodes.word import TemplateWordNode
from programy.parser.exceptions import ParserException

from programytest.parser.base import ParserTestsBaseClass

class MockTemplateLogNode(TemplateLogNode):
    def __init__(self):
        TemplateLogNode.__init__(self)

    def resolve_to_string(self, context):
        raise Exception("This is an error")

class TemplateLogNodeTests(ParserTestsBaseClass):

    def test_init(self):
        log = TemplateLogNode()

        log.level = "debug"
        self.assertEqual("debug", log.level)
        self.assertEqual("", log.resolve(self._client_context))

        log.level = "warning"
        self.assertEqual("warning", log.level)
        self.assertEqual("", log.resolve(self._client_context))

        log.level = "error"
        self.assertEqual("error", log.level)
        self.assertEqual("", log.resolve(self._client_context))

        log.level = "info"
        self.assertEqual("info", log.level)
        self.assertEqual("", log.resolve(self._client_context))

        log.level = "exception"
        self.assertEqual("exception", log.level)
        self.assertEqual("", log.resolve(self._client_context))

    def test_set_attrib(self):
        log = TemplateLogNode()

        log.set_attrib('level', TemplateWordNode('debug'))
        self.assertEqual("debug", log.level.word)

        log.set_attrib('level', TemplateWordNode('warning'))
        self.assertEqual("warning", log.level.word)

        log.set_attrib('level', TemplateWordNode('error'))
        self.assertEqual("error", log.level.word)

        log.set_attrib('level', TemplateWordNode('info'))
        self.assertEqual("info", log.level.word)

        with self.assertRaises(ParserException):
            log.set_attrib('unknown', TemplateWordNode('info'))

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)

        log = TemplateLogNode()
        self.assertIsNotNone(log)
        log.append(TemplateWordNode("Log Test"))

        root.append(log)
        self.assertEqual(1, len(root.children))

        resolved = root.resolve(self._client_context)
        self.assertIsNotNone(resolved)
        self.assertEqual("", resolved)

    def test_to_xml_default(self):

        root = TemplateNode()
        log = TemplateLogNode()

        log.append(TemplateWordNode("Log Test"))
        root.append(log)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><log level="debug">Log Test</log></template>', xml_str)

    def test_to_xml_debug(self):

        root = TemplateNode()
        log = TemplateLogNode()
        log.level = TemplateWordNode("debug")

        log.append(TemplateWordNode("Log Test"))
        root.append(log)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><log level="debug">Log Test</log></template>', xml_str)

    def test_to_xml_error(self):

        root = TemplateNode()
        log = TemplateLogNode()
        log.level = TemplateWordNode("error")

        log.append(TemplateWordNode("Log Test"))
        root.append(log)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><log level="error">Log Test</log></template>', xml_str)

    def test_to_xml_info(self):

        root = TemplateNode()
        log = TemplateLogNode()
        log.level = TemplateWordNode("info")

        log.append(TemplateWordNode("Log Test"))
        root.append(log)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><log level="info">Log Test</log></template>', xml_str)

    def test_to_xml_warning(self):

        root = TemplateNode()
        log = TemplateLogNode()
        log.level = TemplateWordNode("warning")

        log.append(TemplateWordNode("Log Test"))
        root.append(log)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><log level="warning">Log Test</log></template>', xml_str)

    def test_to_xml_unknown(self):

        root = TemplateNode()
        log = TemplateLogNode()
        log.level = None

        log.append(TemplateWordNode("Log Test"))
        root.append(log)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><log>Log Test</log></template>', xml_str)

    def test_node_exception_handling(self):
        root = TemplateNode()
        node = MockTemplateLogNode()
        root.append(node)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)