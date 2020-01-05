import unittest

from programy.parser.factory import NodeFactory


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

