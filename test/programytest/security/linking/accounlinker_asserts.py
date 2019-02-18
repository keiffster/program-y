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
        self.assertEquals(primary_user, primary)

    def assert_user_client_link_already_exists(self, linkerservice):
        primary_user = "testuser1"
        primary_client = "console"

        result = linkerservice.link_user_to_client(primary_user, primary_client)
        self.assertTrue(result)
        links = linkerservice.linked_accounts(primary_user)
        self.assertIsNotNone(links)
        self.assertEquals(1, len(links))
        self.assertEquals(primary_client, links[0])

        result = linkerservice.link_user_to_client(primary_user, primary_client)
        self.assertTrue(result)
        links = linkerservice.linked_accounts(primary_user)
        self.assertIsNotNone(links)
        self.assertEquals(1, len(links))
        self.assertEquals(primary_client, links[0])

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
