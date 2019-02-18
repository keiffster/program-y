import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.richmedia.delay import TemplateDelayNode
from programy.parser.template.nodes.word import TemplateWordNode

from programytest.parser.base import ParserTestsBaseClass

class TemplateDelayNodeTests(ParserTestsBaseClass):

    def test_delay_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        delay = TemplateDelayNode()
        delay._seconds = TemplateWordNode("10")

        root.append(delay)

        resolved = root.resolve(self._client_context)
        self.assertIsNotNone(resolved)
        self.assertEqual("<delay><seconds>10</seconds></delay>", resolved)

        self.assertEqual("<delay><seconds>10</seconds></delay>", root.to_xml(self._client_context))

