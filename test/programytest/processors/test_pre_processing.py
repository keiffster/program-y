import os
import unittest
from programy.bot import Bot
from programy.config.bot.bot import BotConfiguration
from programy.context import ClientContext
from programy.processors.pre.demojize import DemojizePreProcessor
from programy.processors.pre.normalize import NormalizePreProcessor
from programy.processors.pre.removepunctuation import RemovePunctuationPreProcessor
from programy.processors.pre.toupper import ToUpperPreProcessor
from programytest.client import TestClient
from programy.storage.factory import StorageFactory
from programy.storage.stores.file.config import FileStorageConfiguration
from programy.storage.stores.file.config import FileStoreConfiguration
from programy.storage.stores.file.engine import FileStorageEngine
from programy.processors.processing import PreProcessorCollection


class PreProcessingTests(unittest.TestCase):

    def test_load(self):
        storage_factory = StorageFactory()

        file_store_config = FileStorageConfiguration()
        file_store_config._preprocessors_storage = FileStoreConfiguration(file=os.path.dirname(__file__) + os.sep + "test_files" + os.sep + "preprocessors.conf", fileformat="text", extension="txt", encoding="utf-8", delete_on_start=False)

        storage_engine = FileStorageEngine(file_store_config)

        storage_factory._storage_engines[StorageFactory.PREPROCESSORS] = storage_engine
        storage_factory._store_to_engine_map[StorageFactory.PREPROCESSORS] = storage_engine

        collection = PreProcessorCollection()
        self.assertIsNotNone(collection)

        self.assertTrue(collection.load(storage_factory))

    def test_pre_cleanup(self):
        self.client = TestClient()

        context = ClientContext(self.client, "testid")
        context.bot = Bot(config=BotConfiguration(), client=self.client)
        context.brain = context.bot.brain
        test_str = "This is my Location!"

        punctuation_processor = RemovePunctuationPreProcessor()
        test_str = punctuation_processor.process(context, test_str)
        self.assertEqual("This is my Location!", test_str)

        normalize_processor = NormalizePreProcessor()
        test_str = normalize_processor.process(context, test_str)
        self.assertEqual("This is my Location!", test_str)

        toupper_processor = ToUpperPreProcessor()
        test_str = toupper_processor.process(context, test_str)
        self.assertEqual("THIS IS MY LOCATION!", test_str)

        demojize_processpr = DemojizePreProcessor()
        test_str = demojize_processpr.process(context, test_str)
        self.assertEqual(test_str, test_str)