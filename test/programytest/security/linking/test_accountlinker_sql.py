import unittest
from programy.storage.stores.sql.engine import SQLStorageEngine
from programy.storage.stores.sql.config import SQLStorageConfiguration
from programy.security.linking.accountlinker import BasicAccountLinkerService

from programytest.security.linking.accounlinker_asserts import AccountLinkerAsserts
import programytest.storage.engines as Engines


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
