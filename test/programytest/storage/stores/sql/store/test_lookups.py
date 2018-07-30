from programytest.storage.asserts.store.assert_lookups import LookupStoreAsserts
import os
import os.path

from programy.storage.stores.sql.store.lookups import SQLLookupsStore
from programy.storage.stores.sql.engine import SQLStorageEngine
from programy.storage.stores.sql.config import SQLStorageConfiguration


class SQLLookupsStoreTests(LookupStoreAsserts):

    def test_initialise(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLLookupsStore(engine)
        self.assertEquals(store.storage_engine, engine)

    def test_lookup_storage(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLLookupsStore(engine)

        self.assert_lookup_storage(store)

    def test_upload_from_text(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLLookupsStore(engine)

        self.assert_upload_from_text(store)

    def test_upload_from_text_file(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLLookupsStore(engine)

        self.assert_upload_from_text_file(store, os.path.dirname(__file__)+os.sep+"data"+os.sep+"lookups"+os.sep+"text"+os.sep+"gender.txt")

    def test_upload_csv_file(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLLookupsStore(engine)

        self.assert_upload_csv_file(store, os.path.dirname(__file__)+os.sep+"data"+os.sep+"lookups"+os.sep+"csv"+os.sep+"gender.csv")
