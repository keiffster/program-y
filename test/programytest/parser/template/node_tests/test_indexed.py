from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.indexed import TemplateIndexedNode
from programy.parser.template.nodes.indexed import TemplateDoubleIndexedNode
from programy.parser.exceptions import ParserException

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
        self.assertEqual(3, node.index)
        node.index = 4
        self.assertEqual(4, node.index)

    def test_attrib_name_index_only(self):
        node = TemplateIndexedNode()
        node.set_attrib('index', 3)
        self.assertEqual(3, node.index)

    def test_invalid_attrib_name(self):
        with self.assertRaises(Exception):
            node = TemplateIndexedNode()
            node.set_attrib('rubbish', 3)


class TemplateDoubleIndexedNodeTests(ParserTestsBaseClass):

    def test_init(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateDoubleIndexedNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

    def test_get_set(self):
        node = TemplateDoubleIndexedNode()
        node.index = 3
        self.assertEqual(3, node.index)
        node.index = 4
        self.assertEqual(4, node.index)

    def test_attrib_name_position_and_index(self):
        node = TemplateDoubleIndexedNode()
        node.set_attrib('index', "1,3")
        self.assertEqual(1, node.question)
        self.assertEqual(3, node.sentence)

    def test_attrib_name_position_and_index_as_star(self):
        node = TemplateDoubleIndexedNode()
        node.set_attrib('index', "1,*")
        self.assertEqual(1, node.question)
        self.assertEqual(-1, node.sentence)

    def test_attrib_name_position_and_index_invalid(self):
        node = TemplateDoubleIndexedNode()

        with self.assertRaises(ParserException):
            node.set_attrib('index', "1 3")

        with self.assertRaises(ParserException):
            node.set_attrib('index', "0,1")

        with self.assertRaises(ParserException):
            node.set_attrib('index', "1,0")

        with self.assertRaises(ParserException):
            node.set_attrib('index', "0,0")

        with self.assertRaises(ParserException):
            node.set_attrib('index', "1,x")

        with self.assertRaises(ParserException):
            node.set_attrib('index', "x,1")

        with self.assertRaises(ParserException):
            node.set_attrib('index', "x,x")

