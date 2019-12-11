import unittest
import programytest.storage.engines as Engines
from programy.storage.stores.nosql.redis.config import RedisStorageConfiguration
from programy.storage.stores.nosql.redis.engine import RedisStorageEngine
from programytest.storage.test_utils import StorageEngineTestUtils


class RedisStorageEngineTests(StorageEngineTestUtils):

    @unittest.skipIf(Engines.redis is False, Engines.redis_disabled)
    def test_init_with_configuration(self):
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

    @unittest.skipIf(Engines.redis is False, Engines.redis_disabled)
    def test_conversations_without_dropapp(self):
        config = RedisStorageConfiguration()
        config._drop_all_first = False
        engine = RedisStorageEngine(config)
        engine.initialise()
        self.conversation_asserts(storage_engine=engine)

    @unittest.skipIf(Engines.redis is False, Engines.redis_disabled)
    def test_initialise_no_password(self):
        config = RedisStorageConfiguration()
        config._password = None
        engine = RedisStorageEngine(config)
        engine.initialise()
        self.conversation_asserts(storage_engine=engine)

    @unittest.skipIf(Engines.redis is False, Engines.redis_disabled)
    def test_initialise_with_password(self):
        config = RedisStorageConfiguration()
        config._password = "password"
        engine = RedisStorageEngine(config)
        engine.initialise()
        self.conversation_asserts(storage_engine=engine)
