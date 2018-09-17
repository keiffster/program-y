import unittest
import os
import os.path

from programy.storage.stores.file.store.processors import FilePostProcessorsStore
from programy.storage.stores.file.engine import FileStorageEngine
from programy.storage.stores.file.config import FileStorageConfiguration
from programy.processors.processing import ProcessorCollection
from programy.storage.stores.file.config import FileStoreConfiguration


class FilePostProcessorsStoreTests(unittest.TestCase):

    def test_initialise(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FilePostProcessorsStore(engine)
        self.assertEqual(store.storage_engine, engine)

    def test_load_postprocessors(self):
        config = FileStorageConfiguration()
        config._postprocessors_storage = FileStoreConfiguration(file=os.path.dirname(__file__) + os.sep + "data" + os.sep + "processors" + os.sep + "postprocessors.conf", format="text", encoding="utf-8", delete_on_start=False)
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FilePostProcessorsStore(engine)

        collection = ProcessorCollection()
        store.load(collection)

        self.assertEqual(5, len(collection.processors))
