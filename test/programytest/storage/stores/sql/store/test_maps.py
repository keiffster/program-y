import unittest
import programytest.storage.engines as Engines
from programy.storage.stores.sql.config import SQLStorageConfiguration
from programy.storage.stores.sql.engine import SQLStorageEngine
from programy.storage.stores.sql.store.maps import SQLMapsStore
from programytest.storage.asserts.store.assert_maps import MapStoreAsserts


class SQLMapsStoreTests(MapStoreAsserts):

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_initialise(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLMapsStore(engine)
        self.assertEqual(store.storage_engine, engine)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_map_storage(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLMapsStore(engine)

        self.assert_map_storage(store)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_upload_from_text(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLMapsStore(engine)

        self.assert_upload_from_text(store)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_upload_text_files_from_directory_no_subdir(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLMapsStore(engine)

        self.assert_upload_text_files_from_directory_no_subdir(store)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_upload_text_files_from_directory_with_subdir(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLMapsStore(engine)

        self.assert_upload_text_files_from_directory_with_subdir(store, "sql")

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_upload_from_csv_file(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLMapsStore(engine)

        self.assert_upload_from_csv_file(store)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_upload_csv_files_from_directory_with_subdir(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLMapsStore(engine)

        self.assert_upload_csv_files_from_directory_with_subdir(store, "sql")

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_empty_named(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLMapsStore(engine)

        self.assert_empty_named(store)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_add_to_map_overwrite_existing(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLMapsStore(engine)

        store.add_to_map("TESTMAP", "key1", "value1", overwrite_existing=True)
        store.add_to_map("TESTMAP", "key2", "value2", overwrite_existing=True)
        store.add_to_map("TESTMAP", "key2", "value3", overwrite_existing=True)

        self.assert_add_to_map_overwrite_existing(store)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_add_to_map_no_overwrite_existing(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLMapsStore(engine)

        self.assert_add_to_map_no_overwrite_existing(store)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_load_no_map_found(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLMapsStore(engine)

        self.assert_load_no_map_found(store)
