import os
import os.path
import unittest

from programy.processors.processing import ProcessorCollection
from programy.storage.stores.file.config import FileStorageConfiguration
from programy.storage.stores.file.config import FileStoreConfiguration
from programy.storage.stores.file.engine import FileStorageEngine
from programy.storage.stores.file.store.processors import FilePostQuestionProcessorsStore


class FilePostQuestionProcessorsStoreTests(unittest.TestCase):

    def test_initialise(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FilePostQuestionProcessorsStore(engine)
        self.assertEqual(store.storage_engine, engine)

    def test_storage_path(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FilePostQuestionProcessorsStore(engine)

        self.assertEquals('/tmp/processing/postquestionprocessors.conf', store._get_storage_path())
        self.assertIsInstance(store.get_storage(), FileStoreConfiguration)

    def test_load_postprocessors(self):
        config = FileStorageConfiguration()
        config._postquestionprocessors_storage = FileStoreConfiguration(file=os.path.dirname(__file__) + os.sep + "data" + os.sep + "processors" + os.sep + "postquestionprocessors.conf", fileformat="text", encoding="utf-8", delete_on_start=False)
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FilePostQuestionProcessorsStore(engine)

        collection = ProcessorCollection()
        store.load(collection)

        self.assertEqual(0, len(collection.processors))
