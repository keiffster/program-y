from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.indexed import TemplateIndexedNode
from programy.parser.template.nodes.word import TemplateWordNode

from programytest.parser.base import ParserTestsBaseClass


class TemplateIndexedNodeTests(ParserTestsBaseClass):

    def test_init(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateIndexedNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

    def test_get_set(self):
        node = TemplateIndexedNode()
        node.index = 3
        self.assertEqual("3", node.index.word)
        node.index = 4
        self.assertEqual("4", node.index.word)

    def test_attrib_name_index_only(self):
        node = TemplateIndexedNode()
        node.set_attrib('index', TemplateWordNode("3"))
        self.assertEqual("3", node.index.word)

    def test_invalid_attrib_name(self):
        with self.assertRaises(Exception):
            node = TemplateIndexedNode()
            node.set_attrib('rubbish', TemplateWordNode("3"))
