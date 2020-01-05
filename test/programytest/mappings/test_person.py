import os
import re
import unittest
from unittest.mock import patch
from programy.mappings.person import PersonCollection
from programy.storage.factory import StorageFactory
from programy.storage.stores.file.config import FileStorageConfiguration
from programy.storage.stores.file.config import FileStoreConfiguration
from programy.storage.stores.file.engine import FileStorageEngine


class PersonTests(unittest.TestCase):

    def test_initialise_collection(self):
        collection = PersonCollection()
        self.assertIsNotNone(collection)

    def test_collection_operations(self):
        person_text = """
        " with you "," with me2 "
        " with me "," with you2 "
        " are you "," am I2 "
        " with me "," with you2 "
        """

        collection = PersonCollection()
        self.assertIsNotNone(collection)

        collection.load_from_text(person_text)

        self.assertEqual(collection.personalise_string(" with me "), "with you2")
        self.assertEqual(collection.personalise_string("Hello are you with me"), "Hello am i2 with you2")

        pattern = collection.person(" with you ")
        self.assertIsNotNone(pattern)
        self.assertEqual(" WITH ME2 ", pattern[1])

    def test_load(self):
        storage_factory = StorageFactory()

        file_store_config = FileStorageConfiguration()
        file_store_config._person_storage = FileStoreConfiguration(file=os.path.dirname(__file__) + os.sep + "test_files" + os.sep + "person.txt", fileformat="text", extension="txt", encoding="utf-8", delete_on_start=False)

        storage_engine = FileStorageEngine(file_store_config)

        storage_factory._storage_engines[StorageFactory.PERSON] = storage_engine
        storage_factory._store_to_engine_map[StorageFactory.PERSON] = storage_engine

        collection = PersonCollection()
        self.assertIsNotNone(collection)

        self.assertTrue(collection.load(storage_factory))

        self.assertEqual(collection.personalise_string(" with me "), "with you2")
        self.assertEqual(collection.personalise_string("Hello are you with me"), "Hello am i2 with you2")

        self.assertEqual([re.compile('(^WITH YOU | WITH YOU | WITH YOU$)', re.IGNORECASE), ' WITH ME2 '], collection.person(" WITH YOU "))
        self.assertEqual(None, collection.person(" WITH XXX "))

    def test_reload(self):
        storage_factory = StorageFactory()

        file_store_config = FileStorageConfiguration()
        file_store_config._person_storage = FileStoreConfiguration(file=os.path.dirname(__file__) + os.sep + "test_files" + os.sep + "person.txt", fileformat="text", extension="txt", encoding="utf-8", delete_on_start=False)

        storage_engine = FileStorageEngine(file_store_config)

        storage_factory._storage_engines[StorageFactory.PERSON] = storage_engine
        storage_factory._store_to_engine_map[StorageFactory.PERSON] = storage_engine

        collection = PersonCollection()
        self.assertIsNotNone(collection)

        self.assertTrue(collection.load(storage_factory))

        self.assertEqual(collection.personalise_string(" with me "), "with you2")
        self.assertEqual(collection.personalise_string("Hello are you with me"), "Hello am i2 with you2")

        self.assertTrue(collection.reload(storage_factory))

        self.assertEqual(collection.personalise_string(" with me "), "with you2")
        self.assertEqual(collection.personalise_string("Hello are you with me"), "Hello am i2 with you2")

    def patch_load_collection(self, lookups_engine):
        raise Exception("Mock Exception")

    @patch("programy.mappings.person.PersonCollection._load_collection", patch_load_collection)
    def test_load_with_exception(self):
        storage_factory = StorageFactory()

        file_store_config = FileStorageConfiguration()
        file_store_config._person_storage = FileStoreConfiguration(file=os.path.dirname(__file__) + os.sep + "test_files" + os.sep + "person.txt", fileformat="text", extension="txt", encoding="utf-8", delete_on_start=False)

        storage_engine = FileStorageEngine(file_store_config)

        storage_factory._storage_engines[StorageFactory.PERSON] = storage_engine
        storage_factory._store_to_engine_map[StorageFactory.PERSON] = storage_engine

        collection = PersonCollection()
        self.assertIsNotNone(collection)

        self.assertFalse(collection.load(storage_factory))
