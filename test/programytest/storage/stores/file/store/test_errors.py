import unittest
import os.path
import shutil

from programy.storage.stores.file.store.errors import FileErrorsStore
from programy.storage.stores.file.engine import FileStorageEngine
from programy.storage.stores.file.config import FileStorageConfiguration


class FileErrorsStoreTests(unittest.TestCase):

    def test_initialise(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileErrorsStore(engine)
        self.assertEqual(store.storage_engine, engine)

    def test_save_errors(self):
        config = FileStorageConfiguration()
        tmpdir = os.path.dirname(__file__) + os.sep + "errors"
        tmpfile = tmpdir + os.sep + "errors.txt"
        config.errors_storage._dirs = [tmpfile]
        config.errors_storage._has_single_file = True
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileErrorsStore(engine)

        path = store._get_dir_from_path(store._get_storage_path())
        if os.path.exists(path):
            shutil.rmtree(path)
        self.assertFalse(os.path.exists(path))

        errors = [["Error1", "aiml1.xml", "100", "200"]]
        store.save_errors(errors)

        self.assertTrue(os.path.exists(store._get_storage_path()))

        shutil.rmtree(tmpdir)
        self.assertFalse(os.path.exists(tmpdir))
