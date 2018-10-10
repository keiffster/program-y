import unittest
import re
import os

from programy.mappings.normal import NormalCollection
from programy.storage.factory import StorageFactory
from programy.storage.stores.file.config import FileStorageConfiguration
from programy.storage.stores.file.engine import FileStorageEngine
from programy.storage.stores.file.config import FileStoreConfiguration


class NormaliseTests(unittest.TestCase):

    def test_initialise_collection(self):
        collection = NormalCollection()
        self.assertIsNotNone(collection)

    def test_collection_operations(self):
        collection = NormalCollection()
        self.assertIsNotNone(collection)

        collection.add_to_lookup(".COM", [re.compile('(^\\.COM|\\.COM|\\.COM$)', re.IGNORECASE), ' DOT COM '])

        self.assertTrue(collection.has_key(".COM"))
        self.assertEqual([re.compile('(^\\.COM|\\.COM|\\.COM$)', re.IGNORECASE), ' DOT COM '], collection.value(".COM"))

        self.assertEqual("keithsterling dot com", collection.normalise_string("keithsterling.COM"))

    def test_load(self):
        storage_factory = StorageFactory()

        file_store_config = FileStorageConfiguration()
        file_store_config._normal_storage = FileStoreConfiguration(file=os.path.dirname(__file__) + os.sep + "test_files" + os.sep + "normal.txt", format="text", extension="txt", encoding="utf-8", delete_on_start=False)

        storage_engine = FileStorageEngine(file_store_config)

        storage_factory._storage_engines[StorageFactory.NORMAL] = storage_engine
        storage_factory._store_to_engine_map[StorageFactory.NORMAL] = storage_engine

        collection = NormalCollection()
        self.assertIsNotNone(collection)

        collection.load(storage_factory)

        self.assertEqual(collection.normalise_string("keithsterling.COM"), "keithsterling dot com")

    def test_reload(self):
        storage_factory = StorageFactory()

        file_store_config = FileStorageConfiguration()
        file_store_config._normal_storage = FileStoreConfiguration(file=os.path.dirname(__file__) + os.sep + "test_files" + os.sep + "normal.txt", format="text", extension="txt", encoding="utf-8", delete_on_start=False)

        storage_engine = FileStorageEngine(file_store_config)

        storage_factory._storage_engines[StorageFactory.NORMAL] = storage_engine
        storage_factory._store_to_engine_map[StorageFactory.NORMAL] = storage_engine

        collection = NormalCollection()
        self.assertIsNotNone(collection)

        collection.load(storage_factory)

        self.assertEqual(collection.normalise_string("keithsterling.COM"), "keithsterling dot com")

        collection.reload(storage_factory)

        self.assertEqual(collection.normalise_string("keithsterling.COM"), "keithsterling dot com")
