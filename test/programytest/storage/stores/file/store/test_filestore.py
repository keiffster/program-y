import unittest
import os
import os.path
import shutil

from programy.storage.stores.file.store.filestore import FileStore
from programy.storage.stores.file.engine import FileStorageEngine
from programy.storage.stores.file.config import FileStorageConfiguration


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
        self.assertEquals(store.storage_engine, engine)

    def test_file_path_operations(self):
        self.assertEquals("/temp", FileStore._get_dir_from_path("/temp/files.txt"))
        self.assertEquals("/temp/files", FileStore._get_dir_from_path("/temp/files/files.txt"))
        self.assertEquals("./temp", FileStore._get_dir_from_path("./temp/files.txt"))
        self.assertEquals(".", FileStore._get_dir_from_path("./files.txt"))
        self.assertEquals("", FileStore._get_dir_from_path("files.txt"))

    def test_ensure_dir_exists(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        store = MockFileStore(engine)

        if os.path.exists(store._get_storage_path()):
            shutil.rmtree(store._get_storage_path())
        self.assertFalse(os.path.exists(store._get_storage_path()))

        store._ensure_dir_exists(store._get_storage_path())

        self.assertTrue(os.path.exists(store._get_storage_path()))
