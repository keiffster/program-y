from programy.storage.stores.nosql.redis.engine import RedisStorageEngine
from programy.storage.stores.nosql.redis.config import RedisStorageConfiguration

from programytest.storage.test_utils import StorageEngineTestUtils

class RedisStorageEngineTests(StorageEngineTestUtils):

    def test_init_with_configuration(self):
        config = RedisStorageConfiguration()
        engine = RedisStorageEngine(config)
        self.assertIsNotNone(engine)
        self.assertIsNotNone(engine.configuration)

    def test_properties(self):
        config = RedisStorageConfiguration()
        engine = RedisStorageEngine(config)
        engine.initialise()
        # TODO Fix this
        #self.property_asserts(storage_engine=engine)
