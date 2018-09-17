import unittest
import os.path
import shutil

from programy.storage.stores.file.store.binaries import FileBinariesStore
from programy.storage.stores.file.engine import FileStorageEngine
from programy.storage.stores.file.config import FileStorageConfiguration
import shutil

class PretendAimlParser(object):

    def __init__(self, name):
        self._name = name


class FileBinariesStoreTests(unittest.TestCase):

    def test_initialise(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileBinariesStore(engine)
        self.assertEqual(store.storage_engine, engine)

    def test_save_load_binaries(self):
        config = FileStorageConfiguration()
        tmpdir = os.path.dirname(__file__) + os.sep + "braintree"
        tmpfile = tmpdir + os.sep + "braintree.bin"
        config.binaries_storage._dirs = [tmpfile]
        config.binaries_storage._has_single_file = True
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileBinariesStore(engine)

        aiml_parser = PretendAimlParser("pretend1")

        path = store._get_dir_from_path(store._get_storage_path())
        if os.path.exists(path):
            shutil.rmtree(path)
        self.assertFalse(os.path.exists(path))

        store.save_binary(aiml_parser)

        self.assertTrue(os.path.exists(store._get_storage_path()))

        aiml_parser2 = store.load_binary()
        self.assertIsNotNone(aiml_parser2)

        self.assertEqual(aiml_parser2._name, "pretend1")

        shutil.rmtree(tmpdir)
        self.assertFalse(os.path.exists(tmpdir))