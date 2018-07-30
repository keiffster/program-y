from programytest.storage.asserts.store.assert_rdfs import RDFStoreAsserts
import os
import os.path

from programy.storage.stores.nosql.mongo.store.rdfs import MongoRDFStore
from programy.storage.stores.nosql.mongo.engine import MongoStorageEngine
from programy.storage.stores.nosql.mongo.config import MongoStorageConfiguration


class MongoRDFStoreTests(RDFStoreAsserts):

    def test_initialise(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoRDFStore(engine)
        self.assertEquals(store.storage_engine, engine)


    def test_rdf_storage(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoRDFStore(engine)

        self.assert_rdf_storage(store)


    def test_upload_from_text(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoRDFStore(engine)

        self.assert_upload_from_text(store)

    def test_upload_from_text_file(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoRDFStore(engine)

        self.assert_upload_from_text_file(store, os.path.dirname(__file__) + os.sep + "data" + os.sep + "rdfs" + os.sep + "text" + os.sep + "activity.txt")

    def test_upload_text_files_from_directory_no_subdir(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoRDFStore(engine)

        self.assert_upload_text_files_from_directory_no_subdir(store, os.path.dirname(__file__) + os.sep + "data" + os.sep + "rdfs" + os.sep + "text")

    def test_upload_from_csv_file(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoRDFStore(engine)

        self.assert_upload_from_csv_file(store, os.path.dirname(__file__) + os.sep + "data" + os.sep + "rdfs" + os.sep + "csv" + os.sep + "activity.csv")

    def test_upload_csv_files_from_directory_with_subdir(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoRDFStore(engine)

        self.assert_upload_csv_files_from_directory_with_subdir(store, os.path.dirname(__file__) + os.sep + "data" + os.sep + "rdfs" + os.sep + "csv")
