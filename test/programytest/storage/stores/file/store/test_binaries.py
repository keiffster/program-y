import unittest
import os.path
import shutil

from programy.storage.stores.file.store.binaries import FileBinariesStore
from programy.storage.stores.file.engine import FileStorageEngine
from programy.storage.stores.file.config import FileStorageConfiguration


class PretendAimlParser(object):

    def __init__(self, name):
        self._name = name


class FileBinariesStoreTests(unittest.TestCase):

    def test_initialise(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileBinariesStore(engine)
        self.assertEquals(store.storage_engine, engine)

    def test_save_load_binaries(self):
        config = FileStorageConfiguration()
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

        self.assertEquals(aiml_parser2._name, "pretend1")

