import unittest
from unittest.mock import patch
from programy.storage.stores.file.config import FileStorageConfiguration
from programy.storage.stores.file.engine import FileStorageEngine
from programy.storage.stores.file.store.nodes import FileNodeStore


class MockNodeFactory:

    def __init__(self):
        self.nodes = []
        self.type = "Mock"

    def add_node(self, node_name, node_class):
        self.nodes.append(node_name)


class FileNodeStoreTests(unittest.TestCase):

    def test_initialise(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileNodeStore(engine)
        self.assertEqual(store.storage_engine, engine)

    def test_valid_config_line(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileNodeStore(engine)

        self.assertFalse(store.valid_config_line("", "filename.txt"))
        self.assertFalse(store.valid_config_line("#not valud", "filename.txt"))
        self.assertFalse(store.valid_config_line("root:baseline", "filename.txt"))
        self.assertTrue(store.valid_config_line("x=y", "filename.txt"))

    def test_process_config_line(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileNodeStore(engine)

        node_factory = MockNodeFactory()

        self.assertFalse(store.process_config_line(node_factory, "", "nodes.txt"))
        self.assertFalse(store.process_config_line(node_factory, "#not valud", "nodes.txt"))
        self.assertFalse(store.process_config_line(node_factory, "root:baseline", "nodes.txt"))

        self.assertTrue(store.process_config_line(node_factory, "root=programy.parser.pattern.nodes.root.PatternRootNode", "nodes.txt"))
        self.assertFalse(store.process_config_line(node_factory, "root=programy.parser.pattern.nodes.root.PatternRootNode", "nodes.txt"))

    @staticmethod
    def patch_instantiate_class(class_string):
        raise Exception("Mock Exception")

    @patch("programy.utils.classes.loader.ClassLoader.instantiate_class", patch_instantiate_class)
    def test_process_config_line_with_exception(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileNodeStore(engine)

        node_factory = MockNodeFactory()

        self.assertFalse(store.process_config_line(node_factory, "root=programy.parser.pattern.nodes.root.PatternRootNode", "nodes.txt"))

