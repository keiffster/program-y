from programytest.storage.asserts.store.assert_denormals import DenormalStoreAsserts
import os
import os.path
import re

from programy.storage.stores.file.store.lookups import FileDenormalStore
from programy.storage.stores.file.engine import FileStorageEngine
from programy.storage.stores.file.config import FileStorageConfiguration
from programy.mappings.denormal import DenormalCollection
from programy.storage.stores.file.config import FileStoreConfiguration


class FileDenormalStoreTests(DenormalStoreAsserts):

    def test_initialise(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileDenormalStore(engine)
        self.assertEqual(store.storage_engine, engine)

    def test_load_from_file(self):
        config = FileStorageConfiguration()
        config._denormal_storage = FileStoreConfiguration(file=os.path.dirname(__file__) + os.sep + "data" + os.sep + "lookups" + os.sep + "text" + os.sep + "denormal.txt", format="text", encoding="utf-8", delete_on_start=False)
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileDenormalStore(engine)

        denormal_collection = DenormalCollection()
        
        store.load(denormal_collection)

        self.assertEqual(denormal_collection.denormalise(" DOT COM "), [re.compile('(^DOT COM | DOT COM | DOT COM$)', re.IGNORECASE), '.COM '])
        self.assertEqual(denormal_collection.denormalise_string("keith dot com"), "keith.com")
