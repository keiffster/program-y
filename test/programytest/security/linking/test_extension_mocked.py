from unittest.mock import patch

from programy.security.linking.accountlinker import BasicAccountLinkerService
from programytest.client import TestClient
from programytest.security.linking.extension_asserts import AccountLinkerExtensionAsserts
from programytest.security.linking.test_accountlinker_mocked import MockStorageEngine


class MockedAccountLinkerExtensionTests(AccountLinkerExtensionAsserts):

    def setUp(self):
        storage_engine = MockStorageEngine()

        client = TestClient()
        self.context = client.create_client_context("TESTUSER")
        self.context.brain._security._account_linker = BasicAccountLinkerService(storage_engine)

    def test_no_words(self):
        self.assert_no_words(self.context)

    def test_unknown_command(self):
        self.assert_unknown_command(self.context)

    def test_primary_account_link_success(self):
        self.assert_primary_account_link_success(self.context)

    def patch_get_account_linker_service(self, context):
        return None

    @patch('programy.security.linking.extension.AccountLinkingExtension.get_account_linker_service', patch_get_account_linker_service)
    def test_primary_account_link_no_service(self):
        self.assert_primary_account_link_no_service(self.context)

    def patch_link_user_to_client(self, userid, account_name):
        return False

    @patch('programy.security.linking.accountlinker.BasicAccountLinkerService.link_user_to_client', patch_link_user_to_client)
    def test_primary_account_link_link_user_to_client_fails(self):
        self.assert_primary_account_link_user_to_client_fails(self.context)

    def test_primary_account_link_failures(self):
        self.assert_primary_account_link_failures(self.context)

    def test_secondary_account_link_success(self):
        self.assert_secondary_account_link_success(self.context)

    def test_secondary_account_link_failures(self):
        self.assert_secondary_account_link_failures(self.context)

    @patch('programy.security.linking.extension.AccountLinkingExtension.get_account_linker_service', patch_get_account_linker_service)
    def test_secondary_account_link_no_service(self):
        self.assert_secondary_account_link_no_service(self.context)

    def patch_generate_link(self, userid, provided_key):
        return None

    @patch('programy.security.linking.accountlinker.BasicAccountLinkerService.generate_link', patch_generate_link)
    def test_account_linker_not_present(self):
        self.assert_account_linker_none(self.context)
