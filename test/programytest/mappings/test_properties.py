import unittest
import os

from programy.mappings.properties import PropertiesCollection
from programy.storage.factory import StorageFactory
from programy.storage.stores.file.config import FileStorageConfiguration
from programy.storage.stores.file.engine import FileStorageEngine
from programy.storage.stores.file.config import FileStoreConfiguration

class PropertysTests(unittest.TestCase):

    def test_initialise_collection(self):
        collection = PropertiesCollection()
        self.assertIsNotNone(collection)

    def test_properties_operations(self):
        collection = PropertiesCollection()
        self.assertIsNotNone(collection)

        collection.add_property("name", "KeiffBot 1.0")
        collection.add_property("firstname", "Keiff")
        collection.add_property("middlename", "AIML")
        collection.add_property("lastname", "BoT")
        collection.add_property("fullname", "KeiffBot")

        self.assertTrue(collection.has_property("name"))
        self.assertFalse(collection.has_property("age"))

        self.assertEqual("KeiffBot 1.0", collection.property("name"))
        self.assertIsNone(collection.property("age"))

    def test_load_from_file(self):
        storage_factory = StorageFactory()

        file_store_config = FileStorageConfiguration()
        file_store_config._properties_storage = FileStoreConfiguration(file=os.path.dirname(__file__) + os.sep + "test_files" + os.sep + "properties.txt", format="text", extension="txt", encoding="utf-8", delete_on_start=False)

        storage_engine = FileStorageEngine(file_store_config)

        storage_factory._storage_engines[StorageFactory.PROPERTIES] = storage_engine
        storage_factory._store_to_engine_map[StorageFactory.PROPERTIES] = storage_engine

        collection = PropertiesCollection()
        self.assertIsNotNone(collection)

        collection.load(storage_factory)

        self.assertTrue(collection.has_property("name"))
        self.assertFalse(collection.has_property("age"))

        self.assertEqual("KeiffBot 1.0", collection.property("name"))
        self.assertIsNone(collection.property("age"))

    def test_reload_from_file(self):
        storage_factory = StorageFactory()

        file_store_config = FileStorageConfiguration()
        file_store_config._properties_storage = FileStoreConfiguration(file=os.path.dirname(__file__) + os.sep + "test_files" + os.sep + "properties.txt", format="text", extension="txt", encoding="utf-8", delete_on_start=False)

        storage_engine = FileStorageEngine(file_store_config)

        storage_factory._storage_engines[StorageFactory.PROPERTIES] = storage_engine
        storage_factory._store_to_engine_map[StorageFactory.PROPERTIES] = storage_engine

        collection = PropertiesCollection()
        self.assertIsNotNone(collection)

        collection.load(storage_factory)

        self.assertTrue(collection.has_property("name"))
        self.assertFalse(collection.has_property("age"))

        self.assertEqual("KeiffBot 1.0", collection.property("name"))
        self.assertIsNone(collection.property("age"))

        collection.remove()

        collection.reload_file(storage_factory)

        self.assertTrue(collection.has_property("name"))
        self.assertFalse(collection.has_property("age"))

        self.assertEqual("KeiffBot 1.0", collection.property("name"))
        self.assertIsNone(collection.property("age"))

