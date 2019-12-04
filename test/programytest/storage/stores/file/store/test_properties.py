import os
import os.path
from unittest.mock import patch
from programy.mappings.properties import PropertiesCollection
from programy.storage.stores.file.config import FileStorageConfiguration
from programy.storage.stores.file.engine import FileStorageEngine
from programy.storage.stores.file.store.properties import FilePropertyStore
from programytest.storage.asserts.store.assert_properties import PropertyStoreAsserts
from programy.storage.stores.file.config import FileStoreConfiguration


class FilePropertyStoreTests(PropertyStoreAsserts):

    def test_initialise(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FilePropertyStore(engine)
        self.assertEqual(store.storage_engine, engine)

    def test_storage_path(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FilePropertyStore(engine)

        self.assertEquals('/tmp/properties/properties.txt', store._get_storage_path())
        self.assertIsInstance(store.get_storage(), FileStoreConfiguration)

    def test_load_properties(self):
        config = FileStorageConfiguration()
        config._properties_storage = FileStoreConfiguration(file=os.path.dirname(__file__) + os.sep + "data" + os.sep + "lookups" + os.sep + "text" + os.sep + "properties.txt", fileformat="text", encoding="utf-8", delete_on_start=False)
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FilePropertyStore(engine)

        collection = PropertiesCollection()
        store.load(collection)

        self.assertTrue(collection.has_key("name"))
        self.assertTrue("Y-Bot", collection.value("name"))
        self.assertTrue(collection.has_key("firstname"))
        self.assertTrue("Y", collection.value("firstname"))
        self.assertTrue(collection.has_key("middlename"))
        self.assertTrue("AIML", collection.value("middlename"))

    def test_process_line(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FilePropertyStore(engine)

        self.assertFalse(store._process_line("", {}))
        self.assertFalse(store._process_line("#name:Y-Bot", {}))
        self.assertTrue(store._process_line("name:Y-Bot", {}))
