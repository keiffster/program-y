import unittest

from programy.storage.stores.nosql.redis.config import RedisStorageConfiguration
from programy.storage.stores.nosql.redis.engine import RedisStorageEngine
from programy.storage.stores.nosql.redis.store.conversations import RedisConversationStore


class RedisStoreTests(unittest.TestCase):

    def test_operations(self):
        config = RedisStorageConfiguration()
        engine = RedisStorageEngine(config)
        engine.initialise()
        store = RedisConversationStore(engine)

        store.save('TESTKEY', "Hello world")
        self.assertEquals('Hello world', store.get('TESTKEY'))
        store.delete('TESTKEY')
        self.assertEquals(None, store.get('TESTKEY'))

