import unittest
from unittest.mock import patch
import programytest.storage.engines as Engines
from programy.storage.stores.sql.config import SQLStorageConfiguration
from programy.storage.stores.sql.engine import SQLStorageEngine
from programy.storage.stores.sql.store.properties import SQLPropertyStore
from programytest.storage.asserts.store.assert_properties import PropertyStoreAsserts


class SQLPropertyStoreTests(PropertyStoreAsserts):

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_initialise(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLPropertyStore(engine)
        self.assertEqual(store.storage_engine, engine)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_split_into_fields(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLPropertyStore(engine)

        self.assertEquals(None, store.split_into_fields(""))
        self.assertEquals(None, store.split_into_fields("X"))
        self.assertEquals(['X', 'Y'], store.split_into_fields('"X","Y"'))
        self.assertEquals(['X', 'Y'], store.split_into_fields('"X","Y","Z"'))

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_properties_storage(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLPropertyStore(engine)

        self.assert_properties_storage(store)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_property_storage(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLPropertyStore(engine)

        self.assert_property_storage(store)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_duplicate_properties_storage(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLPropertyStore(engine)

        self.assert_duplicate_property_storage(store)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_empty_properties(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLPropertyStore(engine)

        self.assert_empty_properties(store)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_upload_from_file(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLPropertyStore(engine)

        self.assert_upload_from_file(store)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_upload_from_file_verbose(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLPropertyStore(engine)

        self.assert_upload_from_file_verbose(store)

    def patch_read_lines_from_file(self, filename, verbose):
        raise Exception("Mock Exception")

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    @patch("programy.storage.stores.sql.store.properties.SQLPropertyStore._read_lines_from_file", patch_read_lines_from_file)
    def test_upload_from_file_with_exception(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLPropertyStore(engine)

        self.assert_upload_from_file_exception(store)
