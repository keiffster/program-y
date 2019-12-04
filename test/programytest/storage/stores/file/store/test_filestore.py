import os
import os.path
import shutil
import unittest
from unittest.mock import patch
from programy.storage.stores.file.config import FileStorageConfiguration
from programy.storage.stores.file.engine import FileStorageEngine
from programy.storage.stores.file.store.filestore import FileStore


class MockFileStore(FileStore):

    def __init__(self, engine):
        FileStore.__init__(self, engine)
        self._temp_folder = "/tmp/filestoretemp"

    def _get_storage_path(self):
        return self._temp_folder


class FileStoreTests(unittest.TestCase):

    def test_initialise(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        store = FileStore(engine)
        self.assertEqual(store.storage_engine, engine)

    def test_file_path_operations(self):
        self.assertEqual("/temp", FileStore._get_dir_from_path("/temp/files.txt"))
        self.assertEqual("/temp/files", FileStore._get_dir_from_path("/temp/files/files.txt"))
        self.assertEqual("./temp", FileStore._get_dir_from_path("./temp/files.txt"))
        self.assertEqual(".", FileStore._get_dir_from_path("./files.txt"))
        self.assertEqual("", FileStore._get_dir_from_path("files.txt"))

    def test_ensure_dir_exists(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        store = MockFileStore(engine)

        if os.path.exists(store._get_storage_path()):
            shutil.rmtree(store._get_storage_path())
        self.assertFalse(os.path.exists(store._get_storage_path()))

        store._ensure_dir_exists(store._get_storage_path())

        self.assertTrue(os.path.exists(store._get_storage_path()))

    def test_drop(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        store = MockFileStore(engine)

        if os.path.exists(store._get_storage_path()):
            shutil.rmtree(store._get_storage_path())

        os.mkdir(store._get_storage_path())
        os.mkdir(store._get_storage_path() + os.sep + "subdir1")
        store.drop()

        self.assertFalse(os.path.exists(store._get_storage_path()))

    def test_drop_no_dir(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        store = MockFileStore(engine)

        if os.path.exists(store._get_storage_path()):
            shutil.rmtree(store._get_storage_path())

        store.drop()

        self.assertFalse(os.path.exists(store._get_storage_path()))

    def patch_drop_folder(self, folder):
        raise Exception("Mock Exception")

    @patch('programy.storage.stores.file.store.filestore.FileStore._drop_folder', patch_drop_folder)
    def test_drop_exception(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        store = MockFileStore(engine)

        if os.path.exists(store._get_storage_path()):
            shutil.rmtree(store._get_storage_path())

        store.drop()

        self.assertFalse(os.path.exists(store._get_storage_path()))
