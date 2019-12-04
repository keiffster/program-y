import os
import os.path
import re

from programy.mappings.gender import GenderCollection
from programy.storage.stores.file.config import FileStorageConfiguration
from programy.storage.stores.file.config import FileStoreConfiguration
from programy.storage.stores.file.engine import FileStorageEngine
from programy.storage.stores.file.store.lookups import FileGenderStore
from programytest.storage.asserts.store.assert_genders import GenderStoreAsserts


class FileGenderStoreTests(GenderStoreAsserts):

    def test_initialise(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileGenderStore(engine)
        self.assertEqual(store.storage_engine, engine)

    def test_storage_path(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileGenderStore(engine)

        self.assertEquals('/tmp/lookups/gender.txt', store._get_storage_path())
        self.assertIsInstance(store.get_storage(), FileStoreConfiguration)

    def test_load_from_file(self):
        config = FileStorageConfiguration()
        config._gender_storage = FileStoreConfiguration(file=os.path.dirname(__file__) + os.sep + "data" + os.sep + "lookups" + os.sep + "text" + os.sep + "gender.txt", fileformat="text", encoding="utf-8", delete_on_start=False)
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileGenderStore(engine)

        gender_collection = GenderCollection()
        
        store.load(gender_collection)

        self.assertEqual(gender_collection.gender(" WITH HIM "), [re.compile('(^WITH HIM | WITH HIM | WITH HIM$)', re.IGNORECASE), ' WITH HER '])
        self.assertEqual(gender_collection.genderise_string("This is with him "), "This is with her")
