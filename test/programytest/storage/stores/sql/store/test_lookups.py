import unittest
from unittest.mock import patch
import re
import programytest.storage.engines as Engines
from programy.storage.stores.sql.config import SQLStorageConfiguration
from programy.storage.stores.sql.engine import SQLStorageEngine
from programy.storage.stores.sql.store.lookups import SQLPersonStore
from programy.mappings.base import DoubleStringPatternSplitCollection


class TestCollection(DoubleStringPatternSplitCollection):

    def __init__(self):
        DoubleStringPatternSplitCollection.__init__(self)


class SQLPersonStoreTests(unittest.TestCase):

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_initialise(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLPersonStore(engine)
        self.assertEqual(store.storage_engine, engine)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_add_to_lookup_overwrite_false(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLPersonStore(engine)

        store.add_to_lookup("key1", "value1", overwrite_existing=False)
        store.add_to_lookup("key1", "value2", overwrite_existing=False)

        collection = TestCollection()

        store.load(collection)

        self.assertEquals(1, len(collection.pairs.keys()))
        self.assertTrue(collection.has_key("key1"))
        self.assertEqual([re.compile('(^key1|key1|key1$)', re.IGNORECASE), 'VALUE1'], collection.value("key1"))

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_load_no_collection(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLPersonStore(engine)

        collection = TestCollection()

        store.load(collection)

        self.assertEquals(0, len(collection.pairs.keys()))

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_add_to_lookup_overwrite_true(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLPersonStore(engine)
        store. empty()

        store.add_to_lookup("key1", "value1", overwrite_existing=True)
        store.add_to_lookup("key1", "value2", overwrite_existing=True)

        collection = TestCollection()

        store.load(collection)

        self.assertEquals(1, len(collection.pairs.keys()))
        self.assertTrue(collection.has_key("key1"))
        self.assertEqual([re.compile('(^key1|key1|key1$)', re.IGNORECASE), 'VALUE2'], collection.value("key1"))

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_load_all(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLPersonStore(engine)

        store.add_to_lookup("key1", "value1", overwrite_existing=True)

        collection = TestCollection()

        store.load_all(collection)

        self.assertEquals(1, len(collection.pairs.keys()))
        self.assertTrue(collection.has_key("key1"))
        self.assertEqual([re.compile('(^key1|key1|key1$)', re.IGNORECASE), 'VALUE1'], collection.value("key1"))

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_get_lookup_present(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLPersonStore(engine)
        store.empty()

        store.add_to_lookup("key1", "value1", overwrite_existing=True)

        collection = store.get_lookup()
        self.assertIsNotNone(collection )

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_get_lookup_not_present(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLPersonStore(engine)
        store.empty()

        collection = store.get_lookup()
        self.assertEquals({}, collection)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_process_line_verbose(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLPersonStore(engine)
        store.empty()

        store.process_line("test", ["field1", "field2"], verbose=True)
        store.process_line("test", ["field1", "field2"], verbose=False)

    def patch_read_lookups_from_file(self, filename, verbose):
        raise Exception("Mock Exception")

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    @patch("programy.storage.stores.sql.store.lookups.SQLLookupsStore._read_lookups_from_file", patch_read_lookups_from_file)
    def test_upload_from_file_add_document_false(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLPersonStore(engine)
        store.empty()

        count, success = store.upload_from_file("lookups.txtx")
        self.assertEqual(0, count)
        self.assertEqual(0, success)
