from programytest.storage.asserts.store.assert_variables import VariablesStoreAsserts

from programy.storage.stores.nosql.redis.store.variables import RedisVariableStore
from programy.storage.stores.nosql.redis.engine import RedisStorageEngine
from programy.storage.stores.nosql.redis.config import RedisStorageConfiguration


class RedisVariableStoreTests(VariablesStoreAsserts):

    def test_initialise(self):
        config = RedisStorageConfiguration()
        engine = RedisStorageEngine(config)
        engine.initialise()
        store = RedisVariableStore(engine)
        self.assertEquals(store.storage_engine, engine)

    def test_variables_storage(self):
        config = RedisStorageConfiguration()
        engine = RedisStorageEngine(config)
        engine.initialise()
        store = RedisVariableStore(engine)

        self.assert_variables_storage(store)

    def test_variable_storage(self):
        config = RedisStorageConfiguration()
        engine = RedisStorageEngine(config)
        engine.initialise()
        store = RedisVariableStore(engine)

        self.assert_variable_storage(store)

    def test_empty_variables(self):
        config = RedisStorageConfiguration()
        engine = RedisStorageEngine(config)
        engine.initialise()
        store = RedisVariableStore(engine)

        self.assert_empty_variables(store)
