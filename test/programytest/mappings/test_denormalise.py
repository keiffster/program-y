import unittest
import re
import os

from programy.mappings.denormal import DenormalCollection
from programy.storage.factory import StorageFactory
from programy.storage.stores.file.config import FileStorageConfiguration
from programy.storage.stores.file.engine import FileStorageEngine
from programy.storage.stores.file.config import FileStoreConfiguration


class DenormaliseTests(unittest.TestCase):

    def test_initialise_collection(self):
        collection = DenormalCollection()
        self.assertIsNotNone(collection)

    def test_collection_operations(self):
        collection = DenormalCollection()
        self.assertIsNotNone(collection)

        collection.add_to_lookup(" DOT COM ", [re.compile("(^DOT COM | DOT COM | DOT COM$)", re.IGNORECASE), ".com"])

        self.assertTrue(collection.has_key(" DOT COM "))
        self.assertEqual([re.compile("(^DOT COM | DOT COM | DOT COM$)", re.IGNORECASE), ".com"], collection.value(" DOT COM "))

        self.assertEqual(collection.denormalise_string("keithsterling dot com"), "keithsterling.com")
        self.assertIsNone(collection.denormalise(" dot cox "))

    def test_load(self):
        storage_factory = StorageFactory()

        file_store_config = FileStorageConfiguration()
        file_store_config._denormal_storage = FileStoreConfiguration(file=os.path.dirname(__file__) + os.sep + "test_files" + os.sep + "denormal.txt", format="text", extension="txt", encoding="utf-8", delete_on_start=False)

        storage_engine = FileStorageEngine(file_store_config)

        storage_factory._storage_engines[StorageFactory.DENORMAL] = storage_engine
        storage_factory._store_to_engine_map[StorageFactory.DENORMAL] = storage_engine

        collection = DenormalCollection()
        self.assertIsNotNone(collection)

        collection.load(storage_factory)

        self.assertEqual(collection.denormalise_string("keithsterling dot com"), "keithsterling.com")
        self.assertIsNone(collection.denormalise(" dot cox "))

    def test_reload(self):
        storage_factory = StorageFactory()

        file_store_config = FileStorageConfiguration()
        file_store_config._denormal_storage = FileStoreConfiguration(file=os.path.dirname(__file__) + os.sep + "test_files" + os.sep + "denormal.txt", format="text", extension="txt", encoding="utf-8", delete_on_start=False)

        storage_engine = FileStorageEngine(file_store_config)

        storage_factory._storage_engines[StorageFactory.DENORMAL] = storage_engine
        storage_factory._store_to_engine_map[StorageFactory.DENORMAL] = storage_engine

        collection = DenormalCollection()
        self.assertIsNotNone(collection)

        collection.load(storage_factory)

        collection.reload(storage_factory)
