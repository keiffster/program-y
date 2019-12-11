import unittest
from unittest.mock import patch
import programytest.storage.engines as Engines
from programy.storage.stores.sql.config import SQLStorageConfiguration
from programy.storage.stores.sql.engine import SQLStorageEngine
from programy.storage.stores.sql.store.spelling import SQLSpellingStore
from programytest.storage.asserts.store.assert_spelling import SpellingStoreAsserts


class SQLSpellingStoreTests(SpellingStoreAsserts):

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_initialise(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLSpellingStore(engine)
        self.assertEqual(store.storage_engine, engine)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_upload_from_file(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLSpellingStore(engine)

        self.assert_upload_from_file(store, verbose=False)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_upload_from_file_verbose(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLSpellingStore(engine)

        self.assert_upload_from_file(store, verbose=True)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_upload_from_file_verbose_no_corpus(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLSpellingStore(engine)

        self.assert_upload_from_file_no_corpus(store, verbose=False)

    def patch_read_corpus_from_file(self, filename, verbose):
        raise Exception("Mock Exception")

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    @patch("programy.storage.stores.sql.store.spelling.SQLSpellingStore._read_corpus_from_file",
           patch_read_corpus_from_file)
    def test_upload_from_file_exception(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLSpellingStore(engine)

        self.assert_upload_from_file_exception(store, verbose=False)