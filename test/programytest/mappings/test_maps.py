import unittest
import os

from programy.mappings.maps import MapCollection
from programy.storage.factory import StorageFactory
from programy.storage.stores.file.config import FileStorageConfiguration
from programy.storage.stores.file.engine import FileStorageEngine
from programy.storage.stores.file.config import FileStoreConfiguration


class MapTests(unittest.TestCase):

    def test_initialise_collection(self):
        collection = MapCollection()
        self.assertIsNotNone(collection)
        self.assertIsNotNone(collection.maps)
        self.assertIsNotNone(collection.stores)

    def test_collection_operations(self):
        collection = MapCollection()

        collection.add_map("TESTMAP1", {"key1": "val1", "key2": "val2"}, "teststore")
        collection.add_map("TESTMAP2", {"key4": "val4", "key5": "val5"}, "teststore")

        self.assertIsNotNone(collection.maps)
        self.assertIsNotNone(collection.stores)

        self.assertTrue(collection.contains("TESTMAP1"))
        self.assertTrue(collection.contains("TESTMAP2"))
        self.assertFalse(collection.contains("TESTMAP3"))

        self.assertEqual("teststore", collection.storename("TESTMAP1"))
        self.assertIsNone(collection.storename("TESTMAP3"))

        collection.remove("TESTMAP2")
        self.assertTrue(collection.contains("TESTMAP1"))
        self.assertFalse(collection.contains("TESTMAP2"))
        self.assertFalse(collection.contains("TESTMAP3"))

        collection.empty()
        self.assertFalse(collection.contains("TESTMAP1"))
        self.assertFalse(collection.contains("TESTMAP2"))
        self.assertFalse(collection.contains("TESTMAP3"))

    def test_load_from_file(self):
        storage_factory = StorageFactory()

        file_store_config = FileStorageConfiguration()
        file_store_config._maps_storage = FileStoreConfiguration(dirs=[os.path.dirname(__file__) + os.sep + "test_files" + os.sep + "maps"])
        storage_engine = FileStorageEngine(file_store_config)

        storage_factory._storage_engines[StorageFactory.MAPS] = storage_engine
        storage_factory._store_to_engine_map[StorageFactory.MAPS] = storage_engine

        collection = MapCollection()
        self.assertIsNotNone(collection)

        collection.load(storage_factory)

        self.assertTrue(collection.contains("TEST_MAP"))

    def test_reload_from_file(self):
        storage_factory = StorageFactory()

        file_store_config = FileStorageConfiguration()
        file_store_config._maps_storage = FileStoreConfiguration(dirs=[os.path.dirname(__file__) + os.sep + "test_files" + os.sep + "maps"])
        storage_engine = FileStorageEngine(file_store_config)

        storage_factory._storage_engines[StorageFactory.MAPS] = storage_engine
        storage_factory._store_to_engine_map[StorageFactory.MAPS] = storage_engine

        collection = MapCollection()
        self.assertIsNotNone(collection)

        collection.load(storage_factory)

        self.assertTrue(collection.contains("TEST_MAP"))

        collection.reload(storage_factory, "TEST_MAP")

        self.assertTrue(collection.contains("TEST_MAP"))
