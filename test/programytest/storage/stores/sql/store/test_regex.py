import unittest
from unittest.mock import patch
import programytest.storage.engines as Engines
from programy.storage.stores.sql.config import SQLStorageConfiguration
from programy.storage.stores.sql.engine import SQLStorageEngine
from programy.storage.stores.sql.store.properties import SQLRegexStore
from programytest.storage.asserts.store.assert_regex import RegexStoreAsserts


class SQLRegexStoreTests(RegexStoreAsserts):

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_initialise(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLRegexStore(engine)
        self.assertEqual(store.storage_engine, engine)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_defaults_storage(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLRegexStore(engine)

        self.assert_regexes_storage(store)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_regex_storage(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLRegexStore(engine)

        self.assert_regex_storage(store)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_empty_regexes(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLRegexStore(engine)

        self.assert_empty_regexes(store)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_upload_from_file(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLRegexStore(engine)

        self.assert_upload_from_file(store)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_add_to_collection(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLRegexStore(engine)

        self.assert_add_to_collection(store)

    def patch_add_regex(self, name, value):
        raise Exception("Mock Exception")

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    @patch("programy.mappings.properties.RegexTemplatesCollection.add_regex", patch_add_regex)
    def test_add_to_collection_exception(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLRegexStore(engine)

        self.assert_add_to_collection_collection(store)
