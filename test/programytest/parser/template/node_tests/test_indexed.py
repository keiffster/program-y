from programy.parser.exceptions import ParserException
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

    def test_resolve(self):
        node = TemplateIndexedNode()
        with self.assertRaises(NotImplementedError):
            node.resolve_to_string(None)

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
        with self.assertRaises(ParserException):
            node = TemplateIndexedNode()
            node.set_attrib('rubbish', TemplateWordNode("3"))

    def test_valid_index_value(self):
        node = TemplateIndexedNode()

        node.set_attrib("index", TemplateWordNode("1"))

        node.set_attrib("index", TemplateWordNode("1, 2"))

        node.set_attrib("index", "1")

        node.set_attrib("index", "1, 2")

        node.set_attrib("index", "1, *")

    def test_invalid_index_value(self):
        node = TemplateIndexedNode()

        with self.assertRaises(ParserException):
            node.set_attrib("index", TemplateWordNode("x"))

        with self.assertRaises(ParserException):
            node.set_attrib("index", TemplateWordNode("x, 1"))

        with self.assertRaises(ParserException):
            node.set_attrib("index", TemplateWordNode("1, x"))

        with self.assertRaises(ParserException):
            node.set_attrib("index", TemplateWordNode("x, x"))

        with self.assertRaises(ParserException):
            node.set_attrib("index", TemplateWordNode("*, 1"))

        with self.assertRaises(ParserException):
            node.set_attrib("index", TemplateWordNode("1, 2, 3"))
