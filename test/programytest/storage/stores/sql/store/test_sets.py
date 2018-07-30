from programytest.storage.asserts.store.assert_sets import SetStoreAsserts
import os

from programy.storage.stores.sql.store.sets import SQLSetsStore
from programy.storage.stores.sql.engine import SQLStorageEngine
from programy.storage.stores.sql.config import SQLStorageConfiguration


class SQLSetsStoreTests(SetStoreAsserts):

    def test_initialise(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLSetsStore(engine)
        self.assertEquals(store.storage_engine, engine)

    def test_set_storage(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLSetsStore(engine)

        self.assert_set_storage(store)

    def test_upload_from_text(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLSetsStore(engine)

        self.assert_upload_from_text(store)

    def test_upload_from_text_file(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLSetsStore(engine)

        self.assert_upload_from_text_file(store, os.path.dirname(__file__) + os.sep + "data" + os.sep + "sets" + os.sep + "text" + os.sep + "testset.txt")

    def test_upload_text_files_from_directory_no_subdir(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLSetsStore(engine)

        self.assert_upload_text_files_from_directory_no_subdir(store, os.path.dirname(__file__)+os.sep+"data"+os.sep+"sets"+os.sep+"text")

    def test_upload_from_csv_file(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLSetsStore(engine)

        self.assert_upload_from_csv_file(store, os.path.dirname(__file__) + os.sep + "data" + os.sep + "sets" + os.sep + "csv" + os.sep + "testset.csv")

    def test_upload_csv_files_from_directory_with_subdir(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLSetsStore(engine)

        self.assert_upload_csv_files_from_directory_with_subdir(store, os.path.dirname(__file__) + os.sep + "data" + os.sep + "sets" + os.sep + "csv")

