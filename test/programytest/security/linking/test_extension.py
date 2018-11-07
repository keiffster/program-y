import unittest

from programy.security.linking.extension import AccountLinkingExtension

from programytest.client import TestClient


class AccountLinkerExtensionTests(unittest.TestCase):

    def setUp(self):
        client = TestClient()
        self.context = client.create_client_context("TESTUSER")

    def test_unknown_command(self):

        extension = AccountLinkingExtension()
        self.assertIsNotNone(extension)

        self.assertEquals("ACCOUNT LINK FAILED UNKNOWN COMMAND", extension.execute(self.context, "UNKNOWN COMMAND"))
        self.assertEquals("ACCOUNT LINK FAILED UNKNOWN COMMAND", extension.execute(self.context, "LINK UNKNOWN"))

    def test_primary_account_link_success(self):

        extension = AccountLinkingExtension()
        self.assertIsNotNone(extension)

        command = "LINK PRIMARY ACCOUNT TESTUSER CONSOLE PASSWORD123"

        result = extension.execute(self.context, command)
        self.assertIsNotNone(result)
        self.assertTrue(result.startswith("PRIMARY ACCOUNT LINKED"))

    def test_primary_account_link_failures(self):

        extension = AccountLinkingExtension()
        self.assertIsNotNone(extension)

        self.assertEquals("INVALID PRIMARY ACCOUNT COMMAND", extension.execute(self.context, "LINK PRIMARY ACCOUNT"))
        self.assertEquals("INVALID PRIMARY ACCOUNT COMMAND", extension.execute(self.context, "LINK PRIMARY ACCOUNT USERID"))
        self.assertEquals("INVALID PRIMARY ACCOUNT COMMAND", extension.execute(self.context, "LINK PRIMARY ACCOUNT USERID CLIENT"))

    def test_secondary_account_link_success(self):

        extension = AccountLinkingExtension()
        self.assertIsNotNone(extension)

        command = "LINK SECONDARY ACCOUNT TESTUSER CONSOLE TESTUSER2 FACEBOOK PASSWORD123 HHHHHHH"

        result = extension.execute(self.context, command)
        self.assertIsNotNone(result)
        self.assertTrue(result.startswith("SECONDARY ACCOUNT LINKED"))

    def test_secondary_account_link_failures(self):

        extension = AccountLinkingExtension()
        self.assertIsNotNone(extension)

        self.assertEquals("INVALID SECONDARY ACCOUNT COMMAND", extension.execute(self.context, "LINK SECONDARY ACCOUNT"))
        self.assertEquals("INVALID SECONDARY ACCOUNT COMMAND", extension.execute(self.context, "LINK SECONDARY ACCOUNT SECONDARY_USER"))
        self.assertEquals("INVALID SECONDARY ACCOUNT COMMAND", extension.execute(self.context, "LINK SECONDARY ACCOUNT SECONDARY_USER SECONDARY_CLIENT"))
        self.assertEquals("INVALID SECONDARY ACCOUNT COMMAND", extension.execute(self.context, "LINK SECONDARY ACCOUNT SECONDARY_USER SECONDARY_CLIENT PRIMARY_USER"))
        self.assertEquals("INVALID SECONDARY ACCOUNT COMMAND", extension.execute(self.context, "LINK SECONDARY ACCOUNT SECONDARY_USER SECONDARY_CLIENT PRIMARY_USER PRIMARY_CLIENT"))
        self.assertEquals("INVALID SECONDARY ACCOUNT COMMAND", extension.execute(self.context, "LINK SECONDARY ACCOUNT SECONDARY_USER SECONDARY_CLIENT PRIMARY_USER PRIMARY_CLIENT GIVEN_TOKEN"))
