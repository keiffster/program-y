import os
import unittest
from unittest.mock import patch
from programy.mappings.properties import PropertiesCollection
from programy.storage.factory import StorageFactory
from programy.storage.stores.file.config import FileStorageConfiguration
from programy.storage.stores.file.config import FileStoreConfiguration
from programy.storage.stores.file.engine import FileStorageEngine


class PropertiesTests(unittest.TestCase):

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
        file_store_config._properties_storage = FileStoreConfiguration(file=os.path.dirname(__file__) + os.sep + "test_files" + os.sep + "properties.txt", fileformat="text", extension="txt", encoding="utf-8", delete_on_start=False)

        storage_engine = FileStorageEngine(file_store_config)

        storage_factory._storage_engines[StorageFactory.PROPERTIES] = storage_engine
        storage_factory._store_to_engine_map[StorageFactory.PROPERTIES] = storage_engine

        collection = PropertiesCollection()
        self.assertIsNotNone(collection)

        self.assertTrue(collection.load(storage_factory))

        self.assertTrue(collection.has_property("name"))
        self.assertFalse(collection.has_property("age"))

        self.assertEqual("KeiffBot 1.0", collection.property("name"))
        self.assertIsNone(collection.property("age"))

    def test_reload_from_file(self):
        storage_factory = StorageFactory()

        file_store_config = FileStorageConfiguration()
        file_store_config._properties_storage = FileStoreConfiguration(file=os.path.dirname(__file__) + os.sep + "test_files" + os.sep + "properties.txt", fileformat="text", extension="txt", encoding="utf-8", delete_on_start=False)

        storage_engine = FileStorageEngine(file_store_config)

        storage_factory._storage_engines[StorageFactory.PROPERTIES] = storage_engine
        storage_factory._store_to_engine_map[StorageFactory.PROPERTIES] = storage_engine

        collection = PropertiesCollection()
        self.assertIsNotNone(collection)

        self.assertTrue(collection.load(storage_factory))

        self.assertTrue(collection.has_property("name"))
        self.assertFalse(collection.has_property("age"))

        self.assertEqual("KeiffBot 1.0", collection.property("name"))
        self.assertIsNone(collection.property("age"))

        collection.remove()

        self.assertTrue(collection.reload(storage_factory))

        self.assertTrue(collection.has_property("name"))
        self.assertFalse(collection.has_property("age"))

        self.assertEqual("KeiffBot 1.0", collection.property("name"))
        self.assertIsNone(collection.property("age"))

    def patch_load_collection(self, lookups_engine):
        raise Exception("Mock Exception")

    @patch("programy.mappings.properties.PropertiesCollection._load_collection", patch_load_collection)
    def test_load_with_exception(self):
        storage_factory = StorageFactory()

        file_store_config = FileStorageConfiguration()
        file_store_config._properties_storage = FileStoreConfiguration(file=os.path.dirname(__file__) + os.sep + "test_files" + os.sep + "properties.txt", fileformat="text", extension="txt", encoding="utf-8", delete_on_start=False)

        storage_engine = FileStorageEngine(file_store_config)

        storage_factory._storage_engines[StorageFactory.PROPERTIES] = storage_engine
        storage_factory._store_to_engine_map[StorageFactory.PROPERTIES] = storage_engine

        collection = PropertiesCollection()
        self.assertIsNotNone(collection)

        self.assertFalse(collection.load(storage_factory))
