from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.indexed import TemplateIndexedNode
from programy.parser.exceptions import ParserException

from test.parser.template.base import TemplateTestsBaseClass


class TemplateIndexedNodeTests(TemplateTestsBaseClass):

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
        node.position = 3
        self.assertEqual(3, node.position)
        node.position = 4
        self.assertEqual(4, node.position)

        node.index = 3
        self.assertEqual(3, node.index)
        node.index = 4
        self.assertEqual(4, node.index)

    def test_attrib_name_index_only(self):
        node = TemplateIndexedNode()
        node.set_attrib('index', 3)
        self.assertEqual(1, node.position)
        self.assertEqual(3, node.index)

    def test_attrib_name_position_and_index(self):
        node = TemplateIndexedNode()
        node.set_attrib('index', "1,3")
        self.assertEqual(1, node.position)
        self.assertEqual(3, node.index)

    def test_attrib_name_position_and_index_as_star(self):
        node = TemplateIndexedNode()
        node.set_attrib('index', "1,*")
        self.assertEqual(1, node.position)
        self.assertEqual(1, node.index)

    def test_attrib_name_position_and_index_invalid(self):
        node = TemplateIndexedNode()

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


    def test_invalid_attrib_name(self):
        with self.assertRaises(Exception):
            node = TemplateIndexedNode()
            node.set_attrib('rubbish', 3)