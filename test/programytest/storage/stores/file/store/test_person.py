from programytest.storage.asserts.store.assert_persons import PersonssStoreAsserts
import os
import os.path
import re

from programy.storage.stores.file.store.lookups import FilePersonStore
from programy.storage.stores.file.engine import FileStorageEngine
from programy.storage.stores.file.config import FileStorageConfiguration
from programy.mappings.person import PersonCollection
from programy.storage.stores.file.config import FileStoreConfiguration


class FilePersonStoreTests(PersonssStoreAsserts):

    def test_initialise(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FilePersonStore(engine)
        self.assertEqual(store.storage_engine, engine)

    def test_load_from_file(self):
        config = FileStorageConfiguration()
        config._person_storage = FileStoreConfiguration(file=os.path.dirname(__file__) + os.sep + "data" + os.sep + "lookups" + os.sep + "text" + os.sep + "person.txt", format="text", encoding="utf-8", delete_on_start=False)
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FilePersonStore(engine)

        person_collection = PersonCollection()
        
        store.load(person_collection)

        self.assertEqual(person_collection.person(" WITH YOU "), [re.compile('(^WITH YOU | WITH YOU | WITH YOU$)', re.IGNORECASE), ' WITH ME2 '])
        self.assertEqual(person_collection.personalise_string("Is he with you"), "Is he with me2")
