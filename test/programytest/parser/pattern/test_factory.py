import unittest
import os

from programy.parser.pattern.factory import PatternNodeFactory
from programy.parser.pattern.nodes.root import PatternRootNode
from programy.parser.pattern.nodes.word import PatternWordNode

class PatternFactoryTests(unittest.TestCase):

    def test_init(self):
        factory = PatternNodeFactory()
        self.assertIsNotNone(factory)
        self.assertEquals({}, factory._nodes_config)
        self.assertEqual("Pattern", factory._type)

    def assert_nodes(self, factory):
        self.assertEquals(12, len(factory._nodes_config))

        self.assertTrue("root" in factory._nodes_config)
        instance = factory._nodes_config["root"]
        root = instance()
        self.assertIsInstance(root, PatternRootNode)

        self.assertTrue("word" in factory._nodes_config)
        instance = factory._nodes_config["word"]
        word = instance("test")
        self.assertIsInstance(word, PatternWordNode)

    def test_load_nodes_config_from_file(self):
        factory = PatternNodeFactory()
        factory.load_nodes_config_from_file(os.path.dirname(__file__) + os.sep + "pattern_nodes.conf")
        self.assert_nodes(factory)

    def test_load_nodes_config_from_file_invalid_filename(self):
        factory = PatternNodeFactory()
        factory.load_nodes_config_from_file("some_rubbish.txt")
        self.assert_nodes(factory)

