import unittest


class AccountLinkerAsserts(unittest.TestCase):
    
    def assert_generate_key(self, linkerservice):
        key = linkerservice._generate_key()
        self.assertIsNotNone(key)
        self.assertEqual(8, len(key))

        key = linkerservice._generate_key(size=12)
        self.assertIsNotNone(key)
        self.assertEqual(12, len(key))

    def assert_generate_expirary(self, linkerservice):
        expires = linkerservice._generate_expirary(lifetime=1)
        self.assertIsNotNone(expires)

    def assert_happy_path(self, linkerservice):
        primary_user = "testuser1"
        primary_client = "console"
        provided_key = "PASSWORD1"

        result = linkerservice.link_user_to_client(primary_user, primary_client)
        self.assertTrue(result)

        generated_key = linkerservice.generate_link(primary_user, provided_key)
        self.assertIsNotNone(generated_key)

        result = linkerservice.link_accounts(primary_user, provided_key, generated_key, "testuser2", "facebook")
        self.assertTrue(result)

        primary = linkerservice.primary_account("testuser2")
        self.assertTrue(primary)
        self.assertEqual(primary_user, primary)

    def assert_link_user_to_client_add_user_fails(self, linkerservice):
        primary_user = "testuser1"
        primary_client = "console"

        result = linkerservice.link_user_to_client(primary_user, primary_client)
        self.assertFalse(result)

    def assert_user_client_link_already_exists(self, linkerservice):
        primary_user = "testuser1"
        primary_client = "console"

        result = linkerservice.link_user_to_client(primary_user, primary_client)
        self.assertTrue(result)
        links = linkerservice.linked_accounts(primary_user)
        self.assertIsNotNone(links)
        self.assertEqual(1, len(links))
        self.assertEqual(primary_client, links[0])

        result = linkerservice.link_user_to_client(primary_user, primary_client)
        self.assertTrue(result)
        links = linkerservice.linked_accounts(primary_user)
        self.assertIsNotNone(links)
        self.assertEqual(1, len(links))
        self.assertEqual(primary_client, links[0])

    def assert_provided_key_not_matched(self, linkerservice):
        primary_user = "testuser1"
        primary_client = "console"
        provided_key = "PASSWORD1"
        secondary_user = "testuser2"
        secondary_client = "facebook"

        result = linkerservice.link_user_to_client(primary_user, primary_client)
        self.assertTrue(result)

        generated_key = linkerservice.generate_link(primary_user, provided_key)
        self.assertIsNotNone(generated_key)

        result = linkerservice.link_accounts(primary_user, "PASSWORD2", generated_key, secondary_user, secondary_client)
        self.assertFalse(result)

    def assert_generated_key_not_matched(self, linkerservice):
        primary_user = "testuser1"
        primary_client = "console"
        provided_key = "PASSWORD1"
        secondary_user = "testuser2"
        secondary_client = "facebook"

        result = linkerservice.link_user_to_client(primary_user, primary_client)
        self.assertTrue(result)

        generated_key = linkerservice.generate_link(primary_user, provided_key)
        self.assertIsNotNone(generated_key)

        result = linkerservice.link_accounts(primary_user, provided_key, generated_key+"X", secondary_user, secondary_client)
        self.assertFalse(result)

    def assert_generated_key_expired(self, linkerservice):
        primary_user = "testuser1"
        primary_client = "console"
        provided_key = "PASSWORD1"

        result = linkerservice.link_user_to_client(primary_user, primary_client)
        self.assertTrue(result)

        generated_key = linkerservice.generate_link(primary_user, provided_key, lifetime=0)
        self.assertIsNotNone(generated_key)

        result = linkerservice.link_accounts(primary_user, provided_key, generated_key, "testuser2", "facebook")
        self.assertFalse(result)

    def assert_lockout_after_max_retries(self, linkerservice):
        primary_user = "testuser1"
        primary_client = "console"
        provided_key = "PASSWORD1"
        secondary_user = "testuser2"
        secondary_client = "facebook"

        result = linkerservice.link_user_to_client(primary_user, primary_client)
        self.assertTrue(result)

        generated_key = linkerservice.generate_link(primary_user, provided_key)
        self.assertIsNotNone(generated_key)

        result = linkerservice.link_accounts(primary_user, provided_key, generated_key+"X", secondary_user, secondary_client)
        self.assertFalse(result)

        result = linkerservice.link_accounts(primary_user, provided_key, generated_key+"X", secondary_user, secondary_client)
        self.assertFalse(result)

        result = linkerservice.link_accounts(primary_user, provided_key, generated_key+"X", secondary_user, secondary_client)
        self.assertFalse(result)

        result = linkerservice.link_accounts(primary_user, provided_key, generated_key, secondary_user, secondary_client)
        self.assertFalse(result)

        reset = linkerservice.reset_link(primary_user)
        self.assertTrue(reset)

        result = linkerservice.link_accounts(primary_user, provided_key, generated_key, secondary_user, secondary_client)
        self.assertTrue(result)

    def assert_unlink_user_from_client(self, linkerservice):
        primary_user = "testuser1"
        primary_client = "console"
        provided_key = "PASSWORD1"
        secondary_user = "testuser2"
        secondary_client = "facebook"

        result = linkerservice.link_user_to_client(primary_user, primary_client)
        self.assertTrue(result)

        generated_key = linkerservice.generate_link(primary_user, provided_key)
        self.assertIsNotNone(generated_key)

        result = linkerservice.link_accounts(primary_user, provided_key, generated_key, secondary_user, secondary_client)
        self.assertTrue(result)

        result = linkerservice.unlink_user_from_client(primary_user, primary_client)
        self.assertTrue(result)

        result = linkerservice.link_accounts(primary_user, provided_key, generated_key, secondary_user, secondary_client)
        self.assertFalse(result)

    def assert_unlink_user_from_client_fails(self, linkerservice):
        primary_user = "testuser1"
        primary_client = "console"
        provided_key = "PASSWORD1"
        secondary_user = "testuser2"
        secondary_client = "facebook"

        result = linkerservice.link_user_to_client(primary_user, primary_client)
        self.assertTrue(result)

        generated_key = linkerservice.generate_link(primary_user, provided_key)
        self.assertIsNotNone(generated_key)

        result = linkerservice.link_accounts(primary_user, provided_key, generated_key, secondary_user, secondary_client)
        self.assertTrue(result)

        result = linkerservice.unlink_user_from_client(primary_user, primary_client)
        self.assertFalse(result)

    def assert_unlink_user_from_all_clients(self, linkerservice):
        primary_user = "testuser1"
        primary_client = "console"
        provided_key = "PASSWORD1"
        secondary_user1 = "testuser2"
        secondary_client1 = "facebook"
        secondary_user2 = "testuser3"
        secondary_client2 = "google"

        result = linkerservice.link_user_to_client(primary_user, primary_client)
        self.assertTrue(result)

        generated_key = linkerservice.generate_link(primary_user, provided_key)
        self.assertIsNotNone(generated_key)

        result = linkerservice.link_accounts(primary_user, provided_key, generated_key, secondary_user1, secondary_client1)
        self.assertTrue(result)

        result = linkerservice.link_accounts(primary_user, provided_key, generated_key, secondary_user2, secondary_client2)
        self.assertTrue(result)

        result = linkerservice.unlink_user_from_all_clients(primary_user)
        self.assertTrue(result)

    def assert_unlink_user_from_all_clients_fails(self, linkerservice):
        primary_user = "testuser1"
        primary_client = "console"
        provided_key = "PASSWORD1"
        secondary_user1 = "testuser2"
        secondary_client1 = "facebook"
        secondary_user2 = "testuser3"
        secondary_client2 = "google"

        result = linkerservice.link_user_to_client(primary_user, primary_client)
        self.assertTrue(result)

        generated_key = linkerservice.generate_link(primary_user, provided_key)
        self.assertIsNotNone(generated_key)

        result = linkerservice.link_accounts(primary_user, provided_key, generated_key, secondary_user1, secondary_client1)
        self.assertTrue(result)

        result = linkerservice.link_accounts(primary_user, provided_key, generated_key, secondary_user2, secondary_client2)
        self.assertTrue(result)

        result = linkerservice.unlink_user_from_all_clients(primary_user)
        self.assertFalse(result)

    def assert_generate_link(self, mgr):
        link = mgr.generate_link("testuser1", "PASSWORD1")
        self.assertIsNotNone(link)
        self.assertIsInstance(link, str)
        self.assertTrue(len(link) > 0)

    def assert_generate_link_create_link_fails(self, mgr):
        link = mgr.generate_link("testuser1", "PASSWORD1")
        self.assertIsNone(link)

    def assert_reset_link_get_link_fails(self, mgr):
        self.assertFalse(mgr.reset_link("testuser1"))

    def assert_link_accounts_success(self, mgr):
        primary_user = "testuser1"
        primary_client = "console"
        provided_key = "PASSWORD1"
        secondary_user1 = "testuser2"
        secondary_client1 = "facebook"

        result = mgr.link_user_to_client(primary_user, primary_client)
        self.assertTrue(result)

        generated_key = mgr.generate_link(primary_user, provided_key)
        self.assertIsNotNone(generated_key)

        result = mgr.link_accounts(primary_user, provided_key, generated_key, secondary_user1, secondary_client1)
        self.assertTrue(result)

    def assert_link_accounts_failure(self, mgr):
        primary_user = "testuser1"
        provided_key = "PASSWORD1"
        secondary_user1 = "testuser2"
        secondary_client1 = "facebook"

        generated_key = mgr.generate_link(primary_user, provided_key)
        self.assertIsNotNone(generated_key)

        result = mgr.link_accounts(primary_user, provided_key, generated_key, secondary_user1, secondary_client1)
        self.assertFalse(result)


