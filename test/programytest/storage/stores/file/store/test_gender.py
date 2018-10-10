from programytest.storage.asserts.store.assert_genders import GenderStoreAsserts
import os
import os.path
import re

from programy.storage.stores.file.store.lookups import FileGenderStore
from programy.storage.stores.file.engine import FileStorageEngine
from programy.storage.stores.file.config import FileStorageConfiguration
from programy.mappings.gender import GenderCollection
from programy.storage.stores.file.config import FileStoreConfiguration


class FileGenderStoreTests(GenderStoreAsserts):

    def test_initialise(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileGenderStore(engine)
        self.assertEqual(store.storage_engine, engine)

    def test_load_from_file(self):
        config = FileStorageConfiguration()
        config._gender_storage = FileStoreConfiguration(file=os.path.dirname(__file__) + os.sep + "data" + os.sep + "lookups" + os.sep + "text" + os.sep + "gender.txt", format="text", encoding="utf-8", delete_on_start=False)
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileGenderStore(engine)

        gender_collection = GenderCollection()
        
        store.load(gender_collection)

        self.assertEqual(gender_collection.gender(" WITH HIM "), [re.compile('(^WITH HIM | WITH HIM | WITH HIM$)', re.IGNORECASE), ' WITH HER '])
        self.assertEqual(gender_collection.genderise_string("This is with him "), "This is with her")
