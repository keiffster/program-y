from programytest.storage.asserts.store.assert_maps import MapStoreAsserts
import os
import os.path

from programy.storage.stores.sql.store.maps import SQLMapsStore
from programy.storage.stores.sql.engine import SQLStorageEngine
from programy.storage.stores.sql.config import SQLStorageConfiguration


class SQLMapsStoreTests(MapStoreAsserts):

    def test_initialise(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLMapsStore(engine)
        self.assertEquals(store.storage_engine, engine)

    def test_map_storage(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLMapsStore(engine)

        self.assert_map_storage(store)

    def test_upload_from_text(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLMapsStore(engine)

        self.assert_upload_from_text(store, 'sql')

    def test_upload_text_files_from_directory_no_subdir(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLMapsStore(engine)

        self.assert_upload_text_files_from_directory_no_subdir(store, os.path.dirname(__file__) + os.sep + "data" + os.sep + "maps" + os.sep + "text", 'sql')

    def test_upload_from_csv_file(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLMapsStore(engine)

        self.assert_upload_from_csv_file(store, os.path.dirname(__file__) + os.sep + "data" + os.sep + "maps" + os.sep + "csv" + os.sep + "testmap.csv", 'sql')

    def test_upload_csv_files_from_directory_with_subdir(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLMapsStore(engine)

        self.assert_upload_csv_files_from_directory_with_subdir(store, os.path.dirname(__file__)+os.sep+"data"+os.sep+"maps"+os.sep+"csv", 'sql')

