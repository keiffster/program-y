import unittest
from unittest.mock import patch
import programytest.storage.engines as Engines
from programy.storage.stores.nosql.mongo.config import MongoStorageConfiguration
from programy.storage.stores.nosql.mongo.engine import MongoStorageEngine
from programy.storage.stores.nosql.mongo.store.spelling import MongoSpellingStore
from programytest.storage.asserts.store.assert_spelling import SpellingStoreAsserts


class MongoSpellingStoreTests(SpellingStoreAsserts):

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_initialise(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoSpellingStore(engine)
        self.assertEqual(store.storage_engine, engine)
        
    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_upload_from_file(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoSpellingStore(engine)

        self.assert_upload_from_file(store, verbose=False)

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_upload_from_file_verbose(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoSpellingStore(engine)

        self.assert_upload_from_file(store, verbose=True)

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_upload_from_file_verbose_no_corpus(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoSpellingStore(engine)

        self.assert_upload_from_file_no_corpus(store, verbose=False)

    def patch_read_corpus_from_file(self, filename, verbose):
        raise Exception("Mock Exception")

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    @patch("programy.storage.stores.nosql.mongo.store.spelling.MongoSpellingStore._read_corpus_from_file", patch_read_corpus_from_file)
    def test_upload_from_file_exception(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoSpellingStore(engine)

        self.assert_upload_from_file_exception(store, verbose=False)

    def patch_add_document(self, document):
        return False

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    @patch("programy.storage.stores.nosql.mongo.store.mongostore.MongoStore.add_document", patch_add_document)
    def test_upload_from_file_add_document_false(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoSpellingStore(engine)

        self.assert_upload_from_file_exception(store, verbose=False)
