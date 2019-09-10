import unittest
import os
import os.path

from programy.storage.stores.file.store.processors import FilePostQuestionProcessorsStore
from programy.storage.stores.file.engine import FileStorageEngine
from programy.storage.stores.file.config import FileStorageConfiguration
from programy.processors.processing import ProcessorCollection
from programy.storage.stores.file.config import FileStoreConfiguration


class FilePostQuestionProcessorsStoreTests(unittest.TestCase):

    def test_initialise(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FilePostQuestionProcessorsStore(engine)
        self.assertEqual(store.storage_engine, engine)

    def test_load_postprocessors(self):
        config = FileStorageConfiguration()
        config._postprocessors_storage = FileStoreConfiguration(file=os.path.dirname(__file__) + os.sep + "data" + os.sep + "processors" + os.sep + "postquestionprocessors.conf", format="text", encoding="utf-8", delete_on_start=False)
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FilePostQuestionProcessorsStore(engine)

        collection = ProcessorCollection()
        store.load(collection)

        self.assertEqual(0, len(collection.processors))
