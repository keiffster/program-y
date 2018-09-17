import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.richmedia.list import TemplateListNode
from programy.parser.template.nodes.word import TemplateWordNode

from programytest.parser.base import ParserTestsBaseClass

class TemplateListNodeTests(ParserTestsBaseClass):

    def test_list_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        list = TemplateListNode()

        list._items.append(TemplateWordNode("Item1"))
        list._items.append(TemplateWordNode("Item2"))

        root.append(list)

        resolved = root.resolve(self._client_context)

        self.assertIsNotNone(resolved)
        self.assertEqual("<list><item>Item1</item><item>Item2</item></list>", resolved)

        self.assertEqual("<list><item>Item1</item><item>Item2</item></list>", root.to_xml(self._client_context))

