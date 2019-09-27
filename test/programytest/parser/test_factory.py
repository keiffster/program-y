import unittest
import os

from programy.parser.factory import NodeFactory
from programy.parser.pattern.nodes.root import PatternRootNode
from programy.parser.pattern.nodes.word import PatternWordNode


class MockNodeFactory(NodeFactory):

    def __init__(self, node_type):
        NodeFactory.__init__(self, node_type)

    def default_config_file(self):
        raise NotImplementedError()


class FactoryTests(unittest.TestCase):

    def test_init(self):
        factory = MockNodeFactory("Test")
        self.assertIsNotNone(factory)
        self.assertEqual({}, factory._nodes_config)
        self.assertEqual("Test", factory._type)

