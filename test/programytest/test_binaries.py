import os
import os.path
import unittest

from programy.binaries import BinariesManager
from programy.config.brain.binaries import BrainBinariesConfiguration
from programy.storage.factory import StorageFactory
from programy.storage.stores.file.config import FileStorageConfiguration
from programy.storage.stores.file.config import FileStoreConfiguration
from programy.storage.stores.file.engine import FileStorageEngine
from programytest.client import TestClient


class MockBinariesManager(BinariesManager):

    def __init__(self, binaries_configuration, except_on_load=False, except_on_save=False):
        BinariesManager.__init__(self, binaries_configuration)
        self._except_on_load = except_on_load
        self._except_on_save = except_on_save

    def _load_from_storage(self, storage_factory):
        if self._except_on_load is True:
            raise Exception("Mock Error")
        else:
            return super(MockBinariesManager, self)._load_from_storage(storage_factory)

    def _save_to_storage(self, storage_factory, aiml_parser):
        if self._except_on_save is True:
            raise Exception("Mock Error")
        else:
            super(MockBinariesManager, self)._save_to_storage(storage_factory, aiml_parser)


class BinariesTests(unittest.TestCase):

    def test_init_with_config(self):
        config = BrainBinariesConfiguration()
        manager = BinariesManager(config)
        self.assertIsNotNone(manager)
        self.assertEquals(config, manager._configuration)

    def test_init_without_config(self):
        with self.assertRaises(Exception):
            manager = BinariesManager(None)

    def test_save_then_load(self):

        tmpdir = FileStorageConfiguration.get_temp_dir()

        fullpath = tmpdir + os.sep + "braintree/braintree.bin"

        if os.path.exists(fullpath):
            os.remove(fullpath)

        config = FileStorageConfiguration()
        config._binaries_storage = FileStoreConfiguration(file=fullpath, fileformat="binary", encoding="utf-8",
                                                          delete_on_start=False)

        factory = StorageFactory()

        storage_engine = FileStorageEngine(config)

        factory._storage_engines[StorageFactory.BINARIES] = storage_engine
        factory._store_to_engine_map[StorageFactory.BINARIES] = storage_engine

        storage_engine.initialise()

        config = BrainBinariesConfiguration()
        manager = BinariesManager(config)
        self.assertIsNotNone(manager)

        test_client = TestClient()
        client_context = test_client.create_client_context("test1")

        self.assertTrue(manager.save_binary(factory, client_context.bot.brain.aiml_parser))

        self.assertTrue(os.path.exists(fullpath))

        aiml_parser2 = manager.load_binary(factory)
        self.assertIsNotNone(aiml_parser2)

        if os.path.exists(fullpath):
            os.remove(fullpath)

    def test_save_then_load_no_config(self):

        config = FileStorageConfiguration()
        factory = StorageFactory()
        storage_engine = FileStorageEngine(config)
        storage_engine.initialise()

        config = BrainBinariesConfiguration()
        manager = BinariesManager(config)
        self.assertIsNotNone(manager)

        test_client = TestClient()
        client_context = test_client.create_client_context("test1")

        self.assertFalse(manager.save_binary(factory, client_context.bot.brain.aiml_parser))

        self.assertIsNone(manager.load_binary(factory))

    def test_save_with_exception(self):

        config = BrainBinariesConfiguration()
        manager = MockBinariesManager(config, except_on_save=True)
        self.assertIsNotNone(manager)

        config = FileStorageConfiguration()
        factory = StorageFactory()
        storage_engine = FileStorageEngine(config)
        storage_engine.initialise()

        test_client = TestClient()
        client_context = test_client.create_client_context("test1")

        self.assertFalse(manager.save_binary(factory, client_context.bot.brain.aiml_parser))

    def test_load_with_exception(self):

        config = BrainBinariesConfiguration()
        manager = MockBinariesManager(config, except_on_load=True)
        self.assertIsNotNone(manager)

        config = FileStorageConfiguration()
        factory = StorageFactory()
        storage_engine = FileStorageEngine(config)
        storage_engine.initialise()

        test_client = TestClient()

        self.assertIsNone(manager.load_binary(factory))
