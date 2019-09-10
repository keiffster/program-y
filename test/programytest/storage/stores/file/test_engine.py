import unittest
import unittest.mock
import shutil
import os.path

from programy.storage.stores.file.engine import FileStorageEngine
from programy.storage.stores.file.config import FileStorageConfiguration

from programytest.storage.test_utils import StorageEngineTestUtils


class FileStorageEngineTests(StorageEngineTestUtils):

    def test_init_with_configuration(self):
        config = unittest.mock.Mock
        engine = FileStorageEngine(config)
        self.assertIsNotNone(engine)
        self.assertIsNotNone(engine.configuration)

    def test_properties(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        self.property_asserts(storage_engine=engine)

    def test_conversations(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        self.conversation_asserts(storage_engine=engine)

    def test_twitter(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        self.twitter_asserts(storage_engine=engine)
