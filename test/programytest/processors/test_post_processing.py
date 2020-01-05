import unittest
import re
import os
from programy.bot import Bot
from programy.config.bot.bot import BotConfiguration
from programy.context import ClientContext
from programy.processors.post.denormalize import DenormalizePostProcessor
from programy.processors.post.emojize import EmojizePostProcessor
from programy.processors.post.formatnumbers import FormatNumbersPostProcessor
from programy.processors.post.formatpunctuation import FormatPunctuationProcessor
from programy.processors.post.multispaces import RemoveMultiSpacePostProcessor
from programytest.client import TestClient
from programy.storage.factory import StorageFactory
from programy.storage.stores.file.config import FileStorageConfiguration
from programy.storage.stores.file.config import FileStoreConfiguration
from programy.storage.stores.file.engine import FileStorageEngine
from programy.processors.processing import PostProcessorCollection


class PostProcessingTests(unittest.TestCase):

    def test_load(self):
        storage_factory = StorageFactory()

        file_store_config = FileStorageConfiguration()
        file_store_config._postprocessors_storage = FileStoreConfiguration(file=os.path.dirname(__file__) + os.sep + "test_files" + os.sep + "postprocessors.conf", fileformat="text", extension="txt", encoding="utf-8", delete_on_start=False)

        storage_engine = FileStorageEngine(file_store_config)

        storage_factory._storage_engines[StorageFactory.POSTPROCESSORS] = storage_engine
        storage_factory._store_to_engine_map[StorageFactory.POSTPROCESSORS] = storage_engine

        collection = PostProcessorCollection()
        self.assertIsNotNone(collection)

        self.assertTrue(collection.load(storage_factory))

    def post_process(self, output_str):
        self.client = TestClient()

        context = ClientContext(self.client, "testid")
   
        context.bot = Bot(config=BotConfiguration(), client=self.client)
        context.brain = context.bot.brain
        context.bot.brain.denormals.add_to_lookup(" DOT COM ", [re.compile('(^DOT COM | DOT COM | DOT COM$)', re.IGNORECASE), '.COM '])
        context.bot.brain.denormals.add_to_lookup(" ATSIGN ",[re.compile('(^ATSIGN | ATSIGN | ATSIGN$)', re.IGNORECASE), '@'])

        denormalize = DenormalizePostProcessor()
        punctuation = FormatPunctuationProcessor()
        numbers = FormatNumbersPostProcessor()
        multispaces = RemoveMultiSpacePostProcessor()
        emojize = EmojizePostProcessor()

        output_str = denormalize.process(context, output_str)
        output_str = punctuation.process(context, output_str)
        output_str = numbers.process(context, output_str)
        output_str = multispaces.process(context, output_str)
        output_str = emojize.process(context, output_str)

        return output_str

    def test_post_cleanup(self):

        result = self.post_process("Hello World")
        self.assertIsNotNone(result)
        self.assertEqual("Hello World", result)

        result = self.post_process("Hello World . This is It! ")
        self.assertIsNotNone(result)
        self.assertEqual("Hello World. This is It!", result)

        result = self.post_process("Is the result 23 . 45 ?")
        self.assertIsNotNone(result)
        self.assertEqual("Is the result 23.45?", result)

        result = self.post_process("My email address is ybot atsign programy dot com")
        self.assertIsNotNone(result)
        self.assertEqual("My email address is ybot@programy.com", result)

        result = self.post_process("He said ' Hello World '.")
        self.assertIsNotNone(result)
        self.assertEqual("He said 'Hello World'.", result)

