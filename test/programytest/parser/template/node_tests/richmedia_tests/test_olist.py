import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.richmedia.olist import TemplateOrderedListNode
from programy.parser.template.nodes.word import TemplateWordNode

from programytest.parser.base import ParserTestsBaseClass

class TemplateListNodeTests(ParserTestsBaseClass):

    def test_olist_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        list = TemplateOrderedListNode()

        list._items.append(TemplateWordNode("Item1"))
        list._items.append(TemplateWordNode("Item2"))

        root.append(list)

        resolved = root.resolve(self._client_context)

        self.assertIsNotNone(resolved)
        self.assertEqual("<olist><item>Item1</item><item>Item2</item></olist>", resolved)

        self.assertEqual("<olist><item>Item1</item><item>Item2</item></olist>", root.to_xml(self._client_context))

