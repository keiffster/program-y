import os
import os.path
import unittest
from unittest.mock import patch
from programy.spelling.norvig import NorvigSpellingChecker
from programy.storage.stores.file.config import FileStorageConfiguration
from programy.storage.stores.file.config import FileStoreConfiguration
from programy.storage.stores.file.engine import FileStorageEngine
from programy.storage.stores.file.store.spelling import FileSpellingStore


class FileSpellingStoreTests(unittest.TestCase):

    def test_initialise(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileSpellingStore(engine)
        self.assertEqual(store.storage_engine, engine)

    def test_storage_path(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileSpellingStore(engine)

        self.assertEquals('/tmp/spelling/corpus.txt', store._get_storage_path())
        self.assertIsInstance(store.get_storage(), FileStoreConfiguration)

    def test_load_spelling(self):
        config = FileStorageConfiguration()
        config._spelling_storage =  FileStoreConfiguration(file=os.path.dirname(__file__) + os.sep + "data" + os.sep + "spelling" + os.sep + "corpus.txt", fileformat="text", encoding="utf-8", delete_on_start=False)
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileSpellingStore(engine)

        spelling_checker = NorvigSpellingChecker()
        self.assertTrue(store.load_spelling(spelling_checker))

        self.assertEqual("THESE ARE SOME WORDS", spelling_checker.correct("Thise ara sime wards"))

    def patch_load_corpus_from_file(self, filename, encoding, spell_checker):
        raise Exception ("Mock Exception")

    @patch ("programy.storage.stores.file.store.spelling.FileSpellingStore._load_corpus_from_file", patch_load_corpus_from_file)
    def test_load_spelling_with_exception(self):
        config = FileStorageConfiguration()
        config._spelling_storage =  FileStoreConfiguration(file=os.path.dirname(__file__) + os.sep + "data" + os.sep + "spelling" + os.sep + "corpus.txt", fileformat="text", encoding="utf-8", delete_on_start=False)
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileSpellingStore(engine)

        spelling_checker = NorvigSpellingChecker()
        self.assertFalse(store.load_spelling(spelling_checker))
