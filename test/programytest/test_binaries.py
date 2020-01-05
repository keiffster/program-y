import os
import os.path
import unittest
from unittest.mock import patch
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

    def create_storage_factory(self, fullpath):
        config = FileStorageConfiguration()
        config._binaries_storage = FileStoreConfiguration(file=fullpath, fileformat="binary", encoding="utf-8",
                                                          delete_on_start=False)

        factory = StorageFactory()

        storage_engine = FileStorageEngine(config)

        factory._storage_engines[StorageFactory.BINARIES] = storage_engine
        factory._store_to_engine_map[StorageFactory.BINARIES] = storage_engine

        storage_engine.initialise()

        return factory

    def test_save_then_load(self):

        tmpdir = FileStorageConfiguration.get_temp_dir()

        fullpath = tmpdir + os.sep + "braintree/braintree.bin"

        if os.path.exists(fullpath):
            os.remove(fullpath)

        factory = self.create_storage_factory(fullpath)

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

    def patch_save_to_storage(self, storage_factory, aiml_parser):
        raise Exception("Mock Exception")

    @patch("programy.binaries.BinariesManager._save_to_storage", patch_save_to_storage)
    def test_save_with_exception(self):

        config = BrainBinariesConfiguration()
        manager = BinariesManager(config)
        self.assertIsNotNone(manager)

        tmpdir = FileStorageConfiguration.get_temp_dir()

        fullpath = tmpdir + os.sep + "braintree/braintree.bin"

        if os.path.exists(fullpath):
            os.remove(fullpath)

        factory = self.create_storage_factory(fullpath)

        test_client = TestClient()
        client_context = test_client.create_client_context("test1")

        self.assertFalse(manager.save_binary(factory, client_context.bot.brain.aiml_parser))

    def patch_load_from_storage(self, storage_factory):
        raise Exception("Mock Exception")

    @patch("programy.binaries.BinariesManager._load_from_storage", patch_load_from_storage)
    def test_load_with_exception_and_raise(self):

        config = BrainBinariesConfiguration()
        config._load_aiml_on_binary_fail = False
        manager = BinariesManager(config)
        self.assertIsNotNone(manager)

        tmpdir = FileStorageConfiguration.get_temp_dir()

        fullpath = tmpdir + os.sep + "braintree/braintree.bin"

        if os.path.exists(fullpath):
            os.remove(fullpath)

        factory = self.create_storage_factory(fullpath)

        with self.assertRaises(Exception):
            manager.load_binary(factory)

    @patch("programy.binaries.BinariesManager._load_from_storage", patch_load_from_storage)
    def test_load_with_exception_and_not_raise(self):

        config = BrainBinariesConfiguration()
        config._load_aiml_on_binary_fail = True
        manager = BinariesManager(config)
        self.assertIsNotNone(manager)

        tmpdir = FileStorageConfiguration.get_temp_dir()

        fullpath = tmpdir + os.sep + "braintree/braintree.bin"

        if os.path.exists(fullpath):
            os.remove(fullpath)

        factory = self.create_storage_factory(fullpath)

        self.assertIsNone(manager.load_binary(factory))
