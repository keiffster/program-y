import os.path
import shutil
import unittest
from unittest.mock import patch
from programy.storage.stores.file.config import FileStorageConfiguration
from programy.storage.stores.file.engine import FileStorageEngine
from programy.storage.stores.file.store.duplicates import FileDuplicatesStore
from programy.storage.stores.file.store.config import FileStoreConfiguration


class FileDuplicatesStoreTests(unittest.TestCase):

    def test_initialise(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileDuplicatesStore(engine)
        self.assertEqual(store.storage_engine, engine)

    def test_storage_path(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileDuplicatesStore(engine)

        self.assertEquals('/tmp/debug/duplicates.txt', store._get_storage_path())
        self.assertIsInstance(store.get_storage(), FileStoreConfiguration)

    def test_save_duplicates(self):
        config = FileStorageConfiguration()
        tmpdir = os.path.dirname(__file__) + os.sep + "duplicates"
        tmpfile = tmpdir + os.sep + "duplicates.txt"
        config.duplicates_storage._dirs = [tmpfile]
        config.duplicates_storage._has_single_file = True
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

        shutil.rmtree(tmpdir)
        self.assertFalse(os.path.exists(tmpdir))

    def patch_write_duplicates_to_file(self, filename, duplicates):
        raise Exception("Mock Exception")

    @patch ('programy.storage.stores.file.store.duplicates.FileDuplicatesStore._write_duplicates_to_file', patch_write_duplicates_to_file)
    def test_save_duplicates(self):
        config = FileStorageConfiguration()
        tmpdir = os.path.dirname(__file__) + os.sep + "duplicates"
        tmpfile = tmpdir + os.sep + "duplicates.txt"
        config.duplicates_storage._dirs = [tmpfile]
        config.duplicates_storage._has_single_file = True
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileDuplicatesStore(engine)

        path = store._get_dir_from_path(store._get_storage_path())
        if os.path.exists(path):
            shutil.rmtree(path)
        self.assertFalse(os.path.exists(path))

        duplicates = [["Duplicate1", "aiml1.xml", "100", "200"]]
        store.save_duplicates(duplicates)

        self.assertFalse(os.path.exists(store._get_storage_path()))

    def test_empty(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileDuplicatesStore(engine)

        if os.path.exists(store._get_storage_path()) is False:
            os.mkdir(store._get_storage_path())

        store.empty()

        self.assertFalse(os.path.exists(store._get_storage_path()))

    def test_empty_no_dir(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileDuplicatesStore(engine)

        if os.path.exists(store._get_storage_path()) is True:
            shutil.rmtree(store._get_storage_path())

        store.empty()

        self.assertFalse(os.path.exists(store._get_storage_path()))
