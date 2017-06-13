import unittest
import os

from programy.parser.factory import NodeFactory
from programy.parser.pattern.nodes.root import PatternRootNode
from programy.parser.pattern.nodes.word import PatternWordNode

class FactoryTests(unittest.TestCase):

    def test_init(self):
        factory = NodeFactory("Test")
        self.assertIsNotNone(factory)
        self.assertEquals({}, factory._nodes_config)
        self.assertEqual("Test", factory._type)

    def test_process_config_line(self):
        factory = NodeFactory("Test")

        factory.process_config_line("word=programy.parser.pattern.nodes.word.PatternWordNode")
        self.assertTrue("word" in factory._nodes_config)
        self.assertTrue(1, len(factory._nodes_config))

        factory.process_config_line("# X2=Y")
        self.assertTrue("word" in factory._nodes_config)
        self.assertFalse("X2" in factory._nodes_config)

        factory.process_config_line("X3 Y")
        self.assertTrue("word" in factory._nodes_config)
        self.assertFalse("X3" in factory._nodes_config)

        factory.process_config_line("")
        self.assertTrue("word" in factory._nodes_config)

    def test_valid_line(self):
        factory = NodeFactory("Test")

        self.assertTrue(factory.valid_config_line("X=Y"))
        self.assertTrue(factory.valid_config_line(" X=Y"))
        self.assertTrue(factory.valid_config_line("X=Y "))
        self.assertTrue(factory.valid_config_line(" X=Y "))
        self.assertTrue(factory.valid_config_line(" X = Y "))

        self.assertFalse(factory.valid_config_line(""))
        self.assertFalse(factory.valid_config_line("#"))
        self.assertFalse(factory.valid_config_line("# X"))
        self.assertFalse(factory.valid_config_line("X Y "))

    def test_load_nodes_config_from_file(self):
        factory = NodeFactory("Test")
        factory.load_nodes_config_from_file(os.path.dirname(__file__) + os.sep + "pattern_nodes.conf")
        self.assertEquals(2, len(factory._nodes_config))

        self.assertTrue("root" in factory._nodes_config)
        instance = factory._nodes_config["root"]
        root = instance()
        self.assertIsInstance(root, PatternRootNode)

        self.assertTrue("word" in factory._nodes_config)
        instance = factory._nodes_config["word"]
        word = instance("test")
        self.assertIsInstance(word, PatternWordNode)


    def test_load_nodes_config_from_text(self):
        factory = NodeFactory("Test")
        factory.load_nodes_config_from_text("""
            # Text examples
            root = programy.parser.pattern.nodes.root.PatternRootNode
            word = programy.parser.pattern.nodes.word.PatternWordNode

            # Comment with blank lines around it

        """)
        self.assertEquals(2, len(factory._nodes_config))

        self.assertTrue("root" in factory._nodes_config)
        instance = factory._nodes_config["root"]
        root = instance()
        self.assertIsInstance(root, PatternRootNode)

        self.assertTrue("word" in factory._nodes_config)
        instance = factory._nodes_config["word"]
        word = instance("test")
        self.assertIsInstance(word, PatternWordNode)
