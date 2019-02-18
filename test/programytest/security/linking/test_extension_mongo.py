import unittest
from programy.storage.stores.nosql.mongo.engine import MongoStorageEngine
from programy.storage.stores.nosql.mongo.config import MongoStorageConfiguration
from programy.security.linking.accountlinker import BasicAccountLinkerService

from programytest.client import TestClient
from programytest.security.linking.extension_asserts import AccountLinkerExtensionAsserts
import programytest.storage.engines as Engines


class MongoAccountLinkerExtensionTests(AccountLinkerExtensionAsserts):

    def setUp(self):
        config = MongoStorageConfiguration()
        self.storage_engine = MongoStorageEngine(config)
        self.storage_engine.initialise()

        client = TestClient()
        self.context = client.create_client_context("TESTUSER")
        self.context.brain._security._account_linker = BasicAccountLinkerService(self.storage_engine)

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_unknown_command(self):
        self.assert_unknown_command(self.context)

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_primary_account_link_success(self):
        self.assert_primary_account_link_success(self.context)

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_primary_account_link_failures(self):
        self.assert_primary_account_link_failures(self.context)

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_secondary_account_link_success(self):
        self.assert_secondary_account_link_success(self.context)

    @unittest.skipIf(Engines.mongo is False, Engines.mongo_disabled)
    def test_secondary_account_link_failures(self):
        self.assert_secondary_account_link_failures(self.context)
