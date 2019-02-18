import unittest

from programytest.storage.asserts.store.assert_variables import VariablesStoreAsserts

from programy.storage.stores.nosql.redis.store.variables import RedisVariableStore
from programy.storage.stores.nosql.redis.engine import RedisStorageEngine
from programy.storage.stores.nosql.redis.config import RedisStorageConfiguration

import programytest.storage.engines as Engines


class RedisVariableStoreTests(VariablesStoreAsserts):

    @unittest.skipIf(Engines.redis is False, Engines.redis_disabled)
    def test_initialise(self):
        config = RedisStorageConfiguration()
        engine = RedisStorageEngine(config)
        engine.initialise()
        store = RedisVariableStore(engine)
        self.assertEqual(store.storage_engine, engine)

    @unittest.skipIf(Engines.redis is False, Engines.redis_disabled)
    def test_variables_storage(self):
        config = RedisStorageConfiguration()
        engine = RedisStorageEngine(config)
        engine.initialise()
        store = RedisVariableStore(engine)

        self.assert_variables_storage(store)

    @unittest.skipIf(Engines.redis is False, Engines.redis_disabled)
    def test_variable_storage(self):
        config = RedisStorageConfiguration()
        engine = RedisStorageEngine(config)
        engine.initialise()
        store = RedisVariableStore(engine)

        self.assert_variable_storage(store)

    @unittest.skipIf(Engines.redis is False, Engines.redis_disabled)
    def test_empty_variables(self):
        config = RedisStorageConfiguration()
        engine = RedisStorageEngine(config)
        engine.initialise()
        store = RedisVariableStore(engine)

        self.assert_empty_variables(store)
