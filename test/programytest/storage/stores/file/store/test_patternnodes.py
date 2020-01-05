import os
import os.path
import unittest

from programy.parser.pattern.factory import PatternNodeFactory
from programy.storage.stores.file.config import FileStorageConfiguration
from programy.storage.stores.file.config import FileStoreConfiguration
from programy.storage.stores.file.engine import FileStorageEngine
from programy.storage.stores.file.store.nodes import FilePatternNodeStore


class FilePatternNodeStoreTests(unittest.TestCase):

    def test_initialise(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FilePatternNodeStore(engine)
        self.assertEqual(store.storage_engine, engine)

    def test_storage_path(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FilePatternNodeStore(engine)

        self.assertEquals('/tmp/nodes/pattern_nodes.conf', store._get_storage_path())
        self.assertIsInstance(store.get_storage(), FileStoreConfiguration)

    def test_load_variables(self):
        config = FileStorageConfiguration()
        config._pattern_nodes_storage = FileStoreConfiguration(file=os.path.dirname(__file__) + os.sep + "data" + os.sep + "nodes" + os.sep + "pattern_nodes.conf", fileformat="text", encoding="utf-8", delete_on_start=False)
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FilePatternNodeStore(engine)

        collection = PatternNodeFactory()
        store.load(collection)

        self.assertEqual(12, len(collection.nodes))
        self.assertTrue(collection.exists("zeroormore"))