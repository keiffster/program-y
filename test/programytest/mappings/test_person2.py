import os
import re
import unittest
from unittest.mock import patch
from programy.mappings.person import Person2Collection
from programy.storage.factory import StorageFactory
from programy.storage.stores.file.config import FileStorageConfiguration
from programy.storage.stores.file.config import FileStoreConfiguration
from programy.storage.stores.file.engine import FileStorageEngine


class Person2Tests(unittest.TestCase):

    def test_initialise_collection(self):
        collection = Person2Collection()
        self.assertIsNotNone(collection)

    def test_collection_operations(self):
        person2_text = """
        " I was "," he or she was "
        " he was "," I was "
        " she was "," I was " 
        " I am "," he or she is "
        " I "," he or she " 
        " me "," him or her "
        " my "," his or her " 
        " myself "," him or herself "
        " mine "," his or hers "
        """

        collection = Person2Collection()
        self.assertIsNotNone(collection)

        collection.load_from_text(person2_text)

        self.assertEqual(collection.personalise_string("I was"), "he or she was")
        self.assertEqual(collection.personalise_string("hello he was over there"), "hello i was over there")

        pattern = collection.person(" I am ")
        self.assertIsNotNone(pattern)
        self.assertEqual(" HE OR SHE IS ", pattern[1])

    def test_load(self):
        storage_factory = StorageFactory()

        file_store_config = FileStorageConfiguration()
        file_store_config._person2_storage = FileStoreConfiguration(file=os.path.dirname(__file__) + os.sep + "test_files" + os.sep + "person2.txt", fileformat="text", extension="txt", encoding="utf-8", delete_on_start=False)

        storage_engine = FileStorageEngine(file_store_config)

        storage_factory._storage_engines[StorageFactory.PERSON2] = storage_engine
        storage_factory._store_to_engine_map[StorageFactory.PERSON2] = storage_engine

        collection = Person2Collection()
        self.assertIsNotNone(collection)

        self.assertTrue(collection.load(storage_factory))

        self.assertEqual(collection.personalise_string("I was"), "he or she was")
        self.assertEqual(collection.personalise_string("hello he was over there"), "hello i was over there")

        self.assertEquals([re.compile('(^I WAS | I WAS | I WAS$)', re.IGNORECASE), ' HE OR SHE WAS '], collection.person(" I WAS "))
        self.assertEquals(None, collection.person(" I XXX "))

    def test_reload(self):
        storage_factory = StorageFactory()

        file_store_config = FileStorageConfiguration()
        file_store_config._person2_storage = FileStoreConfiguration(file=os.path.dirname(__file__) + os.sep + "test_files" + os.sep + "person2.txt", fileformat="text", extension="txt", encoding="utf-8", delete_on_start=False)

        storage_engine = FileStorageEngine(file_store_config)

        storage_factory._storage_engines[StorageFactory.PERSON2] = storage_engine
        storage_factory._store_to_engine_map[StorageFactory.PERSON2] = storage_engine

        collection = Person2Collection()
        self.assertIsNotNone(collection)

        self.assertTrue(collection.load(storage_factory))

        self.assertEqual(collection.personalise_string("I was"), "he or she was")
        self.assertEqual(collection.personalise_string("hello he was over there"), "hello i was over there")

        self.assertTrue(collection.reload(storage_factory))

        self.assertEqual(collection.personalise_string("I was"), "he or she was")
        self.assertEqual(collection.personalise_string("hello he was over there"), "hello i was over there")

    def patch_load_collection(self, lookups_engine):
        raise Exception("Mock Exception")

    @patch("programy.mappings.person.Person2Collection._load_collection", patch_load_collection)
    def test_load_with_exception(self):
        storage_factory = StorageFactory()

        file_store_config = FileStorageConfiguration()
        file_store_config._person_storage = FileStoreConfiguration(file=os.path.dirname(__file__) + os.sep + "test_files" + os.sep + "person.txt", fileformat="text", extension="txt", encoding="utf-8", delete_on_start=False)

        storage_engine = FileStorageEngine(file_store_config)

        storage_factory._storage_engines[StorageFactory.PERSON] = storage_engine
        storage_factory._store_to_engine_map[StorageFactory.PERSON] = storage_engine

        collection = Person2Collection()
        self.assertIsNotNone(collection)

        self.assertFalse(collection.load(storage_factory))
