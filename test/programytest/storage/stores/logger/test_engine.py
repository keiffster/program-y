import unittest
import unittest.mock

from programy.storage.stores.logger.engine import LoggerStorageEngine
from programy.storage.stores.logger.config import LoggerStorageConfiguration

from programytest.storage.test_utils import StorageEngineTestUtils

class LoggerStorageEngineTests(StorageEngineTestUtils):

    def test_init_with_configuration(self):
        config = unittest.mock.Mock
        engine = LoggerStorageEngine(config)
        self.assertIsNotNone(engine)
        self.assertIsNotNone(engine.configuration)

    def test_conversations(self):
        config = LoggerStorageConfiguration()
        engine = LoggerStorageEngine(config)
        engine.initialise()
        self.conversation_asserts(storage_engine=engine, visit=False)
