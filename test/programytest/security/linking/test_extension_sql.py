import unittest
from unittest.mock import patch
import programytest.storage.engines as Engines
from programy.security.linking.accountlinker import BasicAccountLinkerService
from programy.storage.stores.sql.config import SQLStorageConfiguration
from programy.storage.stores.sql.engine import SQLStorageEngine
from programytest.client import TestClient
from programytest.security.linking.extension_asserts import AccountLinkerExtensionAsserts


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

    def patch_get_account_linker_service(self, context):
        return None

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    @patch('programy.security.linking.extension.AccountLinkingExtension.get_account_linker_service', patch_get_account_linker_service)
    def test_primary_account_link_no_service(self):
        self.assert_primary_account_link_no_service(self.context)

    def patch_link_user_to_client(self, userid, account_name):
        return False

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    @patch('programy.security.linking.accountlinker.BasicAccountLinkerService.link_user_to_client', patch_link_user_to_client)
    def test_primary_account_link_link_user_to_client_fails(self):
        self.assert_primary_account_link_user_to_client_fails(self.context)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_primary_account_link_failures(self):
        self.assert_primary_account_link_failures(self.context)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_secondary_account_link_success(self):
        self.assert_secondary_account_link_success(self.context)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_secondary_account_link_failures(self):
        self.assert_secondary_account_link_failures(self.context)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    @patch('programy.security.linking.extension.AccountLinkingExtension.get_account_linker_service', patch_get_account_linker_service)
    def test_secondary_account_link_no_service(self):
        self.assert_secondary_account_link_no_service(self.context)

