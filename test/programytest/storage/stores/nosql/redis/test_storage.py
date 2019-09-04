import unittest

from programy.storage.stores.nosql.redis.engine import RedisStorageEngine
from programy.storage.stores.nosql.redis.config import RedisStorageConfiguration

from programytest.storage.test_utils import StorageEngineTestUtils
import programytest.storage.engines as Engines


class RedisStorageEngineTests(StorageEngineTestUtils):

    @unittest.skipIf(Engines.redis is False, Engines.redis_disabled)
    def test_init_with_configuration(self):
        print(Engines.redis)
        config = RedisStorageConfiguration()
        engine = RedisStorageEngine(config)
        self.assertIsNotNone(engine)
        self.assertIsNotNone(engine.configuration)

    @unittest.skipIf(Engines.redis is False, Engines.redis_disabled)
    def test_conversations(self):
        config = RedisStorageConfiguration()
        engine = RedisStorageEngine(config)
        engine.initialise()
        self.conversation_asserts(storage_engine=engine)
