import unittest
import os
import os.path

from programy.storage.stores.file.store.spelling import FileSpellingStore
from programy.storage.stores.file.engine import FileStorageEngine
from programy.storage.stores.file.config import FileStorageConfiguration
from programy.spelling.norvig import NorvigSpellingChecker
from programy.storage.stores.file.config import FileStoreConfiguration

class FileSpellingStoreTests(unittest.TestCase):

    def test_initialise(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileSpellingStore(engine)
        self.assertEqual(store.storage_engine, engine)

    def test_load_spelling(self):
        config = FileStorageConfiguration()
        config._spelling_storage =  FileStoreConfiguration(file=os.path.dirname(__file__) + os.sep + "data" + os.sep + "spelling" + os.sep + "corpus.txt", format="text", encoding="utf-8", delete_on_start=False)
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileSpellingStore(engine)

        store.empty()

        spelling_checker = NorvigSpellingChecker()
        store.load_spelling(spelling_checker)

        self.assertEqual("THESE ARE SOME WORDS", spelling_checker.correct("Thise ara sime wards"))