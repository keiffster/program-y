import unittest
import os
import os.path

from programy.storage.stores.file.store.nodes import FilePatternNodeStore
from programy.storage.stores.file.engine import FileStorageEngine
from programy.storage.stores.file.config import FileStorageConfiguration
from programy.parser.pattern.factory import PatternNodeFactory
from programy.storage.stores.file.config import FileStoreConfiguration


class FilePatternNodeStoreTests(unittest.TestCase):

    def test_initialise(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FilePatternNodeStore(engine)
        self.assertEqual(store.storage_engine, engine)

    def test_load_variables(self):
        config = FileStorageConfiguration()
        config._pattern_nodes_storage = FileStoreConfiguration(file=os.path.dirname(__file__) + os.sep + "data" + os.sep + "nodes" + os.sep + "pattern_nodes.conf", format="text", encoding="utf-8", delete_on_start=False)
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FilePatternNodeStore(engine)

        collection = PatternNodeFactory()
        store.load(collection)

        self.assertEqual(12, len(collection.nodes))
        self.assertTrue(collection.exists("zeroormore"))