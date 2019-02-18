import unittest

from programy.storage.stores.nosql.mongo.engine import MongoStorageEngine
from programy.storage.stores.nosql.mongo.config import MongoStorageConfiguration

from programytest.storage.test_utils import StorageEngineTestUtils
import programytest.storage.engines as Engines


class MongoStorageEngineTests(StorageEngineTestUtils):

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_init_with_configuration(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        self.assertIsNotNone(engine)
        self.assertIsNotNone(engine.configuration)

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_users(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        self.user_asserts(storage_engine=engine)

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_linked_accounts(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        self.linked_account_asserts(storage_engine=engine)

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_links(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        self.link_asserts(storage_engine=engine)

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_properties(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        self.property_asserts(storage_engine=engine)

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_conversations(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        self.conversation_asserts(storage_engine=engine)

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_categories(self):
        config = MongoStorageConfiguration()
        engine = MongoStorageEngine(config)
        engine.initialise()
        self.category_asserts(storage_engine=engine)
