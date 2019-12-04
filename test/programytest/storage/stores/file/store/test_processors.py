import os
import os.path
import unittest
from unittest.mock import patch
from programy.processors.processing import ProcessorCollection
from programy.storage.stores.file.config import FileStorageConfiguration
from programy.storage.stores.file.engine import FileStorageEngine
from programy.storage.stores.file.store.processors import FileProcessorsStore


class FileProcessorsStoreStoreTests(unittest.TestCase):

    def test_initialise(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileProcessorsStore(engine)
        self.assertEqual(store.storage_engine, engine)

    def test_load_file_contents(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileProcessorsStore(engine)

        collection = ProcessorCollection()
        count = store._load_file_contents(collection, os.path.dirname(__file__) + os.sep + "data" + os.sep + "processors" + os.sep + "preprocessors.conf")
        self.assertEquals(2, count)

    def test_process_line(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileProcessorsStore(engine)
        collection = ProcessorCollection()

        self.assertEquals(0, store._process_line("", collection, 0))
        self.assertEquals(0, store._process_line("#programy.processors.post.denormalize.DenormalizePostProcessor", collection, 0))
        self.assertEquals(1, store._process_line("programy.processors.post.denormalize.DenormalizePostProcessor", collection, 0))

    @staticmethod
    def patch_instantiate_class(class_string):
        raise Exception("Mock Exception")

    @patch("programy.utils.classes.loader.ClassLoader.instantiate_class", patch_instantiate_class)
    def test_process_line_with_exception(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileProcessorsStore(engine)

        collection = ProcessorCollection()
        count = store._process_line("XXXXXX", collection, 0)
        self.assertEquals(0, count)

