import unittest
import os

from programy.parser.factory import NodeFactory
from programy.parser.pattern.nodes.root import PatternRootNode
from programy.parser.pattern.nodes.word import PatternWordNode

class FactoryTests(unittest.TestCase):

    def test_init(self):
        factory = NodeFactory("Test")
        self.assertIsNotNone(factory)
        self.assertEqual({}, factory._nodes_config)
        self.assertEqual("Test", factory._type)

