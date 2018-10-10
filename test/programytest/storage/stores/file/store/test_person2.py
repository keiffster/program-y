from programytest.storage.asserts.store.assert_person2s import Person2sStoreAsserts
import os
import os.path
import re

from programy.storage.stores.file.store.lookups import FilePerson2Store
from programy.storage.stores.file.engine import FileStorageEngine
from programy.storage.stores.file.config import FileStorageConfiguration
from programy.mappings.person import PersonCollection
from programy.storage.stores.file.config import FileStoreConfiguration


class FilePerson2StoreTests(Person2sStoreAsserts):

    def test_initialise(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FilePerson2Store(engine)
        self.assertEqual(store.storage_engine, engine)

    def test_load_from_file(self):
        config = FileStorageConfiguration()
        config._person2_storage = FileStoreConfiguration(file=os.path.dirname(__file__) + os.sep + "data" + os.sep + "lookups" + os.sep + "text" + os.sep + "person2.txt", format="text", encoding="utf-8", delete_on_start=False)
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FilePerson2Store(engine)

        person2_collection = PersonCollection()
        
        store.load(person2_collection)

        self.assertEqual(person2_collection.person(" I WAS "), [re.compile('(^I WAS | I WAS | I WAS$)', re.IGNORECASE), ' HE OR SHE WAS '])
        self.assertEqual(person2_collection.personalise_string("I was there"), "he or she was there")
