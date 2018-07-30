from programytest.storage.asserts.store.assert_variables import VariablesStoreAsserts

from programy.storage.stores.nosql.mongo.store.variables import MongoVariableStore
from programy.storage.stores.nosql.mongo.engine import MongoStorageEngine
from programy.storage.stores.nosql.mongo.config import MongoStorageConfiguration


class MongoVariableStoreTests(VariablesStoreAsserts):

    def test_initialise(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoVariableStore(engine)
        self.assertEquals(store.storage_engine, engine)

    def test_variables_storage(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoVariableStore(engine)

        self.assert_variables_storage(store)

    def test_variable_storage(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoVariableStore(engine)

        self.assert_variable_storage(store)

    def test_empty_variables(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = MongoVariableStore(engine)

        self.assert_empty_variables(store)
