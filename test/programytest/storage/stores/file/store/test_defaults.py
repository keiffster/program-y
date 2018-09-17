import unittest
import os
import os.path

from programy.storage.stores.file.store.properties import FileDefaultVariablesStore
from programy.storage.stores.file.engine import FileStorageEngine
from programy.storage.stores.file.config import FileStorageConfiguration
from programy.mappings.properties import PropertiesCollection
from programy.storage.stores.file.config import FileStoreConfiguration


class FileDefaultVariablesStoreTests(unittest.TestCase):

    def test_initialise(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileDefaultVariablesStore(engine)
        self.assertEqual(store.storage_engine, engine)

    def test_load_variables(self):
        config = FileStorageConfiguration()
        config._defaults_storage = FileStoreConfiguration(file=os.path.dirname(__file__) + os.sep + "data" + os.sep + "lookups" + os.sep + "text" + os.sep + "defaults.txt", format="text", encoding="utf-8", delete_on_start=False)
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileDefaultVariablesStore(engine)

        collection = PropertiesCollection()
        store.load(collection)

        self.assertTrue(collection.has_property("var1"))
        self.assertTrue("val1", collection.property("var1"))
        self.assertTrue(collection.has_property("var2"))
        self.assertTrue("val2", collection.property("val2"))
