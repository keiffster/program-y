import os
import re
import unittest
from unittest.mock import patch
from programy.mappings.gender import GenderCollection
from programy.storage.factory import StorageFactory
from programy.storage.stores.file.config import FileStorageConfiguration
from programy.storage.stores.file.config import FileStoreConfiguration
from programy.storage.stores.file.engine import FileStorageEngine


class GenderiseTests(unittest.TestCase):

    def test_initialise_collection(self):
        collection = GenderCollection()
        self.assertIsNotNone(collection)

    def test_collection_operations(self):
        collection = GenderCollection()
        self.assertIsNotNone(collection)

        collection.add_to_lookup(" WITH HIM ", [re.compile('(^WITH HIM | WITH HIM | WITH HIM$)', re.IGNORECASE), ' WITH HER '])

        self.assertTrue(collection.has_key(" WITH HIM "))
        self.assertEqual([re.compile('(^WITH HIM | WITH HIM | WITH HIM$)', re.IGNORECASE), ' WITH HER '], collection.value(" WITH HIM "))

        self.assertEqual(collection.gender(" WITH HIM "), [re.compile('(^WITH HIM | WITH HIM | WITH HIM$)', re.IGNORECASE), ' WITH HER '])
        self.assertEqual(collection.genderise_string("This is with him "), "This is with her")

    def test_load(self):
        storage_factory = StorageFactory()

        file_store_config = FileStorageConfiguration()
        file_store_config._gender_storage = FileStoreConfiguration(file=os.path.dirname(__file__) + os.sep + "test_files" + os.sep + "gender.txt", fileformat="text", extension="txt", encoding="utf-8", delete_on_start=False)

        storage_engine = FileStorageEngine(file_store_config)

        storage_factory._storage_engines[StorageFactory.GENDER] = storage_engine
        storage_factory._store_to_engine_map[StorageFactory.GENDER] = storage_engine

        collection = GenderCollection()
        self.assertIsNotNone(collection)

        self.assertTrue(collection.load(storage_factory))

        self.assertEqual(collection.gender(" WITH HIM "), [re.compile('(^WITH HIM | WITH HIM | WITH HIM$)', re.IGNORECASE), ' WITH HER '])
        self.assertEqual(collection.genderise_string("This is with him "), "This is with her")

    def test_reload(self):
        storage_factory = StorageFactory()

        file_store_config = FileStorageConfiguration()
        file_store_config._gender_storage = FileStoreConfiguration(file=os.path.dirname(__file__) + os.sep + "test_files" + os.sep + "gender.txt", fileformat="text", extension="txt", encoding="utf-8", delete_on_start=False)

        storage_engine = FileStorageEngine(file_store_config)

        storage_factory._storage_engines[StorageFactory.GENDER] = storage_engine
        storage_factory._store_to_engine_map[StorageFactory.GENDER] = storage_engine

        collection = GenderCollection()
        self.assertIsNotNone(collection)

        self.assertTrue(collection.load(storage_factory))

        self.assertEqual(collection.gender(" WITH HIM "), [re.compile('(^WITH HIM | WITH HIM | WITH HIM$)', re.IGNORECASE), ' WITH HER '])
        self.assertEqual(collection.genderise_string("This is with him "), "This is with her")
        self.assertEqual(collection.gender(" WITH XXX "), None)

        self.assertTrue(collection.reload(storage_factory))

        self.assertEqual(collection.gender(" WITH HIM "), [re.compile('(^WITH HIM | WITH HIM | WITH HIM$)', re.IGNORECASE), ' WITH HER '])
        self.assertEqual(collection.genderise_string("This is with him "), "This is with her")

    def patch_load_collection(self, lookups_engine):
        raise Exception("Mock Exception")

    @patch("programy.mappings.gender.GenderCollection._load_collection", patch_load_collection)
    def test_load_with_exception(self):
        storage_factory = StorageFactory()

        file_store_config = FileStorageConfiguration()
        file_store_config._gender_storage = FileStoreConfiguration(file=os.path.dirname(__file__) + os.sep + "test_files" + os.sep + "gender.txt", fileformat="text", extension="txt", encoding="utf-8", delete_on_start=False)

        storage_engine = FileStorageEngine(file_store_config)

        storage_factory._storage_engines[StorageFactory.GENDER] = storage_engine
        storage_factory._store_to_engine_map[StorageFactory.GENDER] = storage_engine

        collection = GenderCollection()
        self.assertIsNotNone(collection)

        self.assertFalse(collection.load(storage_factory))

