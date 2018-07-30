from programytest.storage.asserts.store.assert_maps import MapStoreAsserts
import os
import os.path

from programy.storage.stores.nosql.mongo.store.maps import MongoMapStore
from programy.storage.stores.nosql.mongo.engine import MongoStorageEngine
from programy.storage.stores.nosql.mongo.config import MongoStorageConfiguration


class MongoMapStoreTests(MapStoreAsserts):

    def test_initialise(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoMapStore(engine)
        self.assertEquals(store.storage_engine, engine)

    def test_map_storage(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoMapStore(engine)

        self.assert_map_storage(store)

    def test_upload_from_text(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoMapStore(engine)

        self.assert_upload_from_text(store, 'mongo')

    def test_upload_text_files_from_directory_no_subdir(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoMapStore(engine)

        self.assert_upload_text_files_from_directory_no_subdir(store, os.path.dirname(__file__)+os.sep+"data"+os.sep+"maps"+os.sep+"text", 'mongo')

    def test_upload_from_csv_file(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoMapStore(engine)

        self.assert_upload_from_csv_file(store, os.path.dirname(__file__)+os.sep+"data"+os.sep+"maps"+os.sep+"csv"+os.sep+"testmap.csv", 'mongo')

    def test_upload_csv_files_from_directory_with_subdir(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoMapStore(engine)

        self.assert_upload_csv_files_from_directory_with_subdir(store, os.path.dirname(__file__)+os.sep+"data"+os.sep+"maps"+os.sep+"csv", 'mongo')
