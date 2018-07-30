from programytest.storage.asserts.store.assert_variables import VariablesStoreAsserts

from programy.storage.stores.file.store.variables import FileVariablesStore
from programy.storage.stores.file.engine import FileStorageEngine
from programy.storage.stores.file.config import FileStorageConfiguration


class FileVariablesStoreTests(VariablesStoreAsserts):

    def test_initialise(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileVariablesStore(engine)
        self.assertEquals(store.storage_engine, engine)

    def test_variables_storage(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileVariablesStore(engine)

        self.assert_variables_storage(store)

    def test_variable_storage(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileVariablesStore(engine)

        self.assert_variable_storage(store)

    def test_empty_variables(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileVariablesStore(engine)

        self.assert_empty_variables(store)