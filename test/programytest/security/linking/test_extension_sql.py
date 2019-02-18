import unittest
from programy.storage.stores.sql.engine import SQLStorageEngine
from programy.storage.stores.sql.config import SQLStorageConfiguration
from programy.security.linking.accountlinker import BasicAccountLinkerService

from programytest.client import TestClient
from programytest.security.linking.extension_asserts import AccountLinkerExtensionAsserts
import programytest.storage.engines as Engines


class SQLAccountLinkerExtensionTests(AccountLinkerExtensionAsserts):

    def setUp(self):
        config = SQLStorageConfiguration()
        storage_engine = SQLStorageEngine(config)
        storage_engine.initialise()

        client = TestClient()
        self.context = client.create_client_context("TESTUSER")
        self.context.brain._security._account_linker = BasicAccountLinkerService(storage_engine)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_unknown_command(self):
        self.assert_unknown_command(self.context)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_primary_account_link_success(self):
        self.assert_primary_account_link_success(self.context)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_primary_account_link_failures(self):
        self.assert_primary_account_link_failures(self.context)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_secondary_account_link_success(self):
        self.assert_secondary_account_link_success(self.context)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_secondary_account_link_failures(self):
        self.assert_secondary_account_link_failures(self.context)
