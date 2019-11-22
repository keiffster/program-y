import os
import unittest
from unittest.mock import patch
from programy.mappings.sets import SetCollection
from programy.storage.factory import StorageFactory
from programy.storage.stores.file.config import FileStorageConfiguration
from programy.storage.stores.file.config import FileStoreConfiguration
from programy.storage.stores.file.engine import FileStorageEngine


class SetTests(unittest.TestCase):

    def test_initialise_collection(self):
        collection = SetCollection()
        self.assertIsNotNone(collection)
        self.assertIsNotNone(collection.sets)
        self.assertIsNotNone(collection.stores)

    def test_collection_operations(self):
        collection = SetCollection()
        collection.add_set("TESTSET", {"A": [["A", "B", "C"]], "D": [["D"]], "E": [["E", "F"]]}, "teststore")
        collection.add_set("TESTSET2", {"1": [["1", "2", "3"]], "4": [["4"]], "5": [["5", "6"]]}, "teststore")

        self.assertIsNotNone(collection.sets)
        self.assertIsNotNone(collection.stores)

        self.assertTrue(collection.contains("TESTSET"))
        self.assertTrue(collection.contains("TESTSET2"))
        self.assertFalse(collection.contains("TESTSET3"))

        self.assertEqual("teststore", collection.storename("TESTSET"))
        self.assertIsNone(collection.storename("TESTMAP4"))

        aset = collection.set("TESTSET")
        self.assertIsNotNone(aset)

        self.assertEqual(6, collection.count_words_in_sets())

        collection.remove("TESTSET2")
        self.assertTrue(collection.contains("TESTSET"))
        self.assertFalse(collection.contains("TESTSET2"))
        self.assertFalse(collection.contains("TESTSET3"))

        collection.empty()

        self.assertIsNotNone(collection.sets)
        self.assertIsNotNone(collection.stores)

        self.assertFalse(collection.contains("TESTSET"))
        self.assertIsNone(collection.set("TESTSET"))
        self.assertNotEquals(collection.storename("TESTSET"), "teststore")

    def test_add_set_exists(self):
        collection = SetCollection()
        collection.add_set("TESTSET", {"A": [["A", "B", "C"]], "D": [["D"]], "E": [["E", "F"]]}, "teststore")
        with self.assertRaises(Exception):
            collection.add_set("TESTSET", {"1": [["1", "2", "3"]], "4": [["4"]], "5": [["5", "6"]]}, "teststore")

    def test_load_from_file(self):
        storage_factory = StorageFactory()

        file_store_config = FileStorageConfiguration()
        file_store_config._sets_storage = FileStoreConfiguration(dirs=[os.path.dirname(__file__) + os.sep + "test_files" + os.sep + "sets"])
        storage_engine = FileStorageEngine(file_store_config)

        storage_factory._storage_engines[StorageFactory.SETS] = storage_engine
        storage_factory._store_to_engine_map[StorageFactory.SETS] = storage_engine

        collection = SetCollection()
        self.assertIsNotNone(collection)

        self.assertTrue(collection.load(storage_factory) > 0 )

        self.assertIsNotNone(collection._sets)
        self.assertEqual(len(collection._sets), 1)

        self.assertIsNotNone(collection._stores)
        self.assertEqual(len(collection._stores), 1)

        self.assertTrue("TEST_SET" in collection._sets)
        self.assertTrue("TEST_SET" in collection._stores)

        self.assertTrue(collection.contains('TEST_SET'))

        aset = collection.set('TEST_SET')
        self.assertIsNotNone(aset)
        values = aset['AIR']
        self.assertIsNotNone(values)
        self.assertTrue(['Air', 'Force', 'blue'] in values)

    def test_reload_from_file(self):
        storage_factory = StorageFactory()

        file_store_config = FileStorageConfiguration()
        file_store_config._sets_storage = FileStoreConfiguration(dirs=[os.path.dirname(__file__) + os.sep + "test_files" + os.sep + "sets"])
        storage_engine = FileStorageEngine(file_store_config)

        storage_factory._storage_engines[StorageFactory.SETS] = storage_engine
        storage_factory._store_to_engine_map[StorageFactory.SETS] = storage_engine

        collection = SetCollection()
        self.assertIsNotNone(collection)

        self.assertTrue(collection.load(storage_factory) > 0 )

        self.assertIsNotNone(collection._sets)
        self.assertEqual(len(collection._sets), 1)

        self.assertIsNotNone(collection._stores)
        self.assertEqual(len(collection._stores), 1)

        self.assertTrue("TEST_SET" in collection._sets)
        self.assertTrue("TEST_SET" in collection._stores)

        self.assertTrue(collection.contains('TEST_SET'))

        aset = collection.set('TEST_SET')
        self.assertIsNotNone(aset)
        self.assertTrue(['Air', 'Force', 'blue'] in aset['AIR'])

        self.assertTrue(collection.reload(storage_factory, "TEST_SET" ) > 0)

        self.assertIsNotNone(collection._sets)
        self.assertEqual(len(collection._sets), 1)

        self.assertIsNotNone(collection._stores)
        self.assertEqual(len(collection._stores), 1)

        self.assertTrue("TEST_SET" in collection._sets)
        self.assertTrue("TEST_SET" in collection._stores)

        self.assertTrue(collection.contains('TEST_SET'))

        self.assertIsNotNone(collection.set('TEST_SET'))
        self.assertTrue(['Air', 'Force', 'blue'] in collection.set('TEST_SET')['AIR'])

    def patch_load_collection(self, lookups_engine):
        raise Exception("Mock Exception")

    @patch("programy.mappings.sets.SetCollection._load_collection", patch_load_collection)
    def test_load_with_exception(self):
        storage_factory = StorageFactory()

        file_store_config = FileStorageConfiguration()
        file_store_config._sets_storage = FileStoreConfiguration(dirs=[os.path.dirname(__file__) + os.sep + "test_files" + os.sep + "sets"])
        storage_engine = FileStorageEngine(file_store_config)

        storage_factory._storage_engines[StorageFactory.SETS] = storage_engine
        storage_factory._store_to_engine_map[StorageFactory.SETS] = storage_engine

        collection = SetCollection()
        self.assertIsNotNone(collection)

        self.assertTrue(collection.load(storage_factory) == 0 )

    def patch_reload_collection(self, lookups_engine, set_name):
        raise Exception("Mock Exception")

    @patch("programy.mappings.sets.SetCollection._reload_collection", patch_reload_collection)
    def test_reload_with_exception(self):
        storage_factory = StorageFactory()

        file_store_config = FileStorageConfiguration()
        file_store_config._sets_storage = FileStoreConfiguration(dirs=[os.path.dirname(__file__) + os.sep + "test_files" + os.sep + "sets"])
        storage_engine = FileStorageEngine(file_store_config)

        storage_factory._storage_engines[StorageFactory.SETS] = storage_engine
        storage_factory._store_to_engine_map[StorageFactory.SETS] = storage_engine

        collection = SetCollection()
        self.assertIsNotNone(collection)

        self.assertTrue(collection.load(storage_factory) > 0 )

        self.assertTrue(collection.reload(storage_factory, "TEST_SET") > 0)

    def test_reload_no_storage(self):
        storage_factory = StorageFactory()

        file_store_config = FileStorageConfiguration()
        file_store_config._sets_storage = FileStoreConfiguration(dirs=[os.path.dirname(__file__) + os.sep + "test_files" + os.sep + "sets"])

        collection = SetCollection()
        self.assertIsNotNone(collection)

        self.assertTrue(collection.reload(storage_factory, "TEST_SET") == 0)
