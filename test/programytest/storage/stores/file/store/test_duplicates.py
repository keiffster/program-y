import unittest
import os.path
import shutil

from programy.storage.stores.file.store.duplicates import FileDuplicatesStore
from programy.storage.stores.file.engine import FileStorageEngine
from programy.storage.stores.file.config import FileStorageConfiguration


class FileDuplicatesStoreTests(unittest.TestCase):

    def test_initialise(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileDuplicatesStore(engine)
        self.assertEquals(store.storage_engine, engine)

    def test_save_duplicates(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileDuplicatesStore(engine)

        path = store._get_dir_from_path(store._get_storage_path())
        if os.path.exists(path):
            shutil.rmtree(path)
        self.assertFalse(os.path.exists(path))

        duplicates = [["Duplicate1", "aiml1.xml", "100", "200"]]
        store.save_duplicates(duplicates)

        self.assertTrue(os.path.exists(store._get_storage_path()))

