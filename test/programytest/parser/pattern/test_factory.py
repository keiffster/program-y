import unittest
import os

from programy.parser.pattern.factory import PatternNodeFactory
from programy.parser.pattern.nodes.root import PatternRootNode
from programy.parser.pattern.nodes.word import PatternWordNode

class PatternFactoryTests(unittest.TestCase):

    def test_init(self):
        factory = PatternNodeFactory()
        self.assertIsNotNone(factory)
        self.assertEqual({}, factory._nodes_config)
        self.assertEqual("Pattern", factory._type)

    def assert_nodes(self, factory):
        self.assertEqual(12, len(factory._nodes_config))

        self.assertTrue("root" in factory._nodes_config)
        instance = factory._nodes_config["root"]
        root = instance()
        self.assertIsInstance(root, PatternRootNode)

        self.assertTrue("word" in factory._nodes_config)
        instance = factory._nodes_config["word"]
        word = instance("test")
        self.assertIsInstance(word, PatternWordNode)

