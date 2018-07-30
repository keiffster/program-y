from programytest.storage.asserts.store.assert_properties import PropertyStoreAsserts
import os
import os.path

from programy.storage.stores.file.store.properties import FilePropertyStore
from programy.storage.stores.file.engine import FileStorageEngine
from programy.storage.stores.file.config import FileStorageConfiguration
from programy.mappings.properties import PropertiesCollection
from programy.storage.stores.file.config import FileStoreConfiguration


class FilePropertyStoreTests(PropertyStoreAsserts):

    def test_initialise(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FilePropertyStore(engine)
        self.assertEquals(store.storage_engine, engine)

    def test_properties_storage(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FilePropertyStore(engine)

        self.assert_properties_storage(store)

    def test_property_storage(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FilePropertyStore(engine)

        self.assert_property_storage(store)

    def test_empty_properties(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FilePropertyStore(engine)

        self.assert_empty_properties(store)

    def test_load_properties(self):
        config = FileStorageConfiguration()
        config._properties_storage = FileStoreConfiguration(file=os.path.dirname(__file__) + os.sep + "data" + os.sep + "lookups" + os.sep + "text" + os.sep + "properties.txt", format="text", encoding="utf-8", delete_on_start=False)
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