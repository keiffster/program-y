import unittest

import programytest.storage.engines as Engines
from programy.storage.stores.sql.config import SQLStorageConfiguration
from programy.storage.stores.sql.engine import SQLStorageEngine
from programy.storage.stores.sql.store.categories import SQLCategoryStore
from programytest.storage.asserts.store.assert_category import CategoryStoreAsserts


class SQLCategoryStoreTests(CategoryStoreAsserts):

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_initialise(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLCategoryStore(engine)
        self.assertEqual(store.storage_engine, engine)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_category_storage(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLCategoryStore(engine)
        self.assertEqual(store.storage_engine, engine)

        self.assert_category_storage(store)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_category_by_groupid_storage(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLCategoryStore(engine)
        self.assertEqual(store.storage_engine, engine)

        self.assert_category_by_groupid_storage(store)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_upload_from_file(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLCategoryStore(engine)
        self.assertEqual(store.storage_engine, engine)

        self.assert_upload_from_file(store)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_upload_from_directory(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLCategoryStore(engine)
        self.assertEqual(store.storage_engine, engine)

        self.assert_upload_from_directory(store)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_empty_named(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLCategoryStore(engine)
        self.assertEqual(store.storage_engine, engine)

        self.assert_empty_name(store)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_load(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLCategoryStore(engine)
        self.assertEqual(store.storage_engine, engine)

        self.assert_load(store)
