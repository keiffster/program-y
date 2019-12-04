import os
import os.path
import re

from programy.mappings.person import PersonCollection
from programy.storage.stores.file.config import FileStorageConfiguration
from programy.storage.stores.file.config import FileStoreConfiguration
from programy.storage.stores.file.engine import FileStorageEngine
from programy.storage.stores.file.store.lookups import FilePerson2Store
from programytest.storage.asserts.store.assert_person2s import Person2sStoreAsserts


class FilePerson2StoreTests(Person2sStoreAsserts):

    def test_initialise(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FilePerson2Store(engine)
        self.assertEqual(store.storage_engine, engine)

    def test_storage_path(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FilePerson2Store(engine)

        self.assertEquals('/tmp/lookups/person2.txt', store._get_storage_path())
        self.assertIsInstance(store.get_storage(), FileStoreConfiguration)

    def test_load_from_file(self):
        config = FileStorageConfiguration()
        config._person2_storage = FileStoreConfiguration(file=os.path.dirname(__file__) + os.sep + "data" + os.sep + "lookups" + os.sep + "text" + os.sep + "person2.txt", fileformat="text", encoding="utf-8", delete_on_start=False)
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FilePerson2Store(engine)

        person2_collection = PersonCollection()
        
        store.load(person2_collection)

        self.assertEqual(person2_collection.person(" I WAS "), [re.compile('(^I WAS | I WAS | I WAS$)', re.IGNORECASE), ' HE OR SHE WAS '])
        self.assertEqual(person2_collection.personalise_string("I was there"), "he or she was there")
