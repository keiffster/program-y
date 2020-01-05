import unittest
from unittest.mock import patch

import programytest.storage.engines as Engines
from programy.security.linking.accountlinker import BasicAccountLinkerService
from programy.storage.stores.sql.config import SQLStorageConfiguration
from programy.storage.stores.sql.engine import SQLStorageEngine
from programy.storage.stores.sql.dao.link import Link
from programytest.security.linking.accounlinker_asserts import AccountLinkerAsserts


class SQLAccountLinkerServiceTests(AccountLinkerAsserts):

    def setUp(self):
        config = SQLStorageConfiguration()
        self.storage_engine = SQLStorageEngine(config)
        self.storage_engine.initialise()

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_init(self):
        mgr = BasicAccountLinkerService(self.storage_engine)
        self.assertIsNotNone(mgr)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_generate_key(self):
        mgr = BasicAccountLinkerService(self.storage_engine)
        self.assert_generate_key(mgr)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_generate_expirary(self):
        mgr = BasicAccountLinkerService(self.storage_engine)
        self.assert_generate_expirary(mgr)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_happy_path(self):
        mgr = BasicAccountLinkerService(self.storage_engine)
        self.assert_happy_path(mgr)

    def patch_add_user(self, userid, clientid):
        return None

    @patch('programy.storage.stores.sql.store.users.SQLUserStore.add_user', patch_add_user)
    def test_link_user_to_client_add_user_fails(self):
        mgr = BasicAccountLinkerService(self.storage_engine)
        self.assert_link_user_to_client_add_user_fails(mgr)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_user_client_link_already_exists(self):
        mgr = BasicAccountLinkerService(self.storage_engine)
        self.assert_user_client_link_already_exists(mgr)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_provided_key_not_matched(self):
        mgr = BasicAccountLinkerService(self.storage_engine)
        self.assert_provided_key_not_matched(mgr)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_generated_key_not_matched(self):
        mgr = BasicAccountLinkerService(self.storage_engine)
        self.assert_generated_key_not_matched(mgr)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_generated_key_expired(self):
        mgr = BasicAccountLinkerService(self.storage_engine)
        self.assert_generated_key_expired(mgr)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_lockout_after_max_retries(self):
        mgr = BasicAccountLinkerService(self.storage_engine)
        self.assert_lockout_after_max_retries(mgr)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_unlink_user_from_client(self):
        mgr = BasicAccountLinkerService(self.storage_engine)
        self.assert_unlink_user_from_client(mgr)

    def patch_remove_user(self, userid, clientid):
        return False

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    @patch('programy.storage.stores.sql.store.users.SQLUserStore.remove_user', patch_remove_user)
    def test_unlink_user_from_client_remove_user_fails1(self):
        mgr = BasicAccountLinkerService(self.storage_engine)
        self.assert_unlink_user_from_client_fails(mgr)

    def patch_remove_link(self, userid):
        return False

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    @patch('programy.storage.stores.sql.store.links.SQLLinkStore.remove_link', patch_remove_link)
    def test_unlink_user_from_client_remove_user_fails2(self):
        mgr = BasicAccountLinkerService(self.storage_engine)
        self.assert_unlink_user_from_client_fails(mgr)

    def patch_unlink_accounts(self, userid):
        return False

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    @patch('programy.storage.stores.sql.store.linkedaccounts.SQLLinkedAccountStore.unlink_accounts', patch_unlink_accounts)
    def test_unlink_user_from_client_remove_user_fails3(self):
        mgr = BasicAccountLinkerService(self.storage_engine)
        self.assert_unlink_user_from_client_fails(mgr)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_unlink_user_from_all_clients(self):
        mgr = BasicAccountLinkerService(self.storage_engine)
        self.assert_unlink_user_from_all_clients(mgr)

    def patch_remove_user_from_all_clients(self, userid):
        return False

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    @patch('programy.storage.stores.sql.store.users.SQLUserStore.remove_user_from_all_clients',patch_remove_user_from_all_clients)
    def test_unlink_user_from_all_clients_remove_user_from_all_clients_fails(self):
        mgr = BasicAccountLinkerService(self.storage_engine)
        self.assert_unlink_user_from_all_clients_fails(mgr)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    @patch('programy.storage.stores.sql.store.links.SQLLinkStore.remove_link', patch_remove_link)
    def test_unlink_user_from_all_clients_remove_link_fails(self):
        mgr = BasicAccountLinkerService(self.storage_engine)
        self.assert_unlink_user_from_all_clients_fails(mgr)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    @patch('programy.storage.stores.sql.store.linkedaccounts.SQLLinkedAccountStore.unlink_accounts', patch_unlink_accounts)
    def test_unlink_user_from_all_clients_unlink_accounts_fails(self):
        mgr = BasicAccountLinkerService(self.storage_engine)
        self.assert_unlink_user_from_all_clients_fails(mgr)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_generate_link(self):
        mgr = BasicAccountLinkerService(self.storage_engine)
        self.assert_generate_link(mgr)

    def patch_create_link(self, userid, provided_key, generated_key, expires):
        return None

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    @patch('programy.storage.stores.sql.store.links.SQLLinkStore.create_link', patch_create_link)
    def test_generate_link_create_link_fails(self):
        mgr = BasicAccountLinkerService(self.storage_engine)
        self.assert_generate_link_create_link_fails(mgr)

    def patch_get_link(self, userid):
        return None

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    @patch('programy.storage.stores.sql.store.links.SQLLinkStore.get_link', patch_get_link)
    def test_reset_link_get_link_fails(self):
        mgr = BasicAccountLinkerService(self.storage_engine)
        self.assert_reset_link_get_link_fails(mgr)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_link_accounts(self):
        mgr = BasicAccountLinkerService(self.storage_engine)
        self.assert_link_accounts_success(mgr)

    def patch_get_link(self, userid):
        link = Link()
        link.expired = True
        return link

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    @patch('programy.storage.stores.sql.store.links.SQLLinkStore.get_link', patch_get_link)
    def test_link_accounts_link_expired(self):
        mgr = BasicAccountLinkerService(self.storage_engine)
        self.assert_link_accounts_failure(mgr)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    @patch('programy.storage.stores.sql.store.users.SQLUserStore.add_user', patch_add_user)
    def test_link_accounts_add_user_fails(self):
        mgr = BasicAccountLinkerService(self.storage_engine)
        self.assert_link_accounts_failure(mgr)

    def patch_link_accounts(self, userid, linked_userid):
        return None

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    @patch('programy.storage.stores.sql.store.linkedaccounts.SQLLinkedAccountStore.link_accounts', patch_link_accounts)
    def test_link_accounts_link_accounts_fails(self):
        mgr = BasicAccountLinkerService(self.storage_engine)
        self.assert_link_accounts_failure(mgr)
