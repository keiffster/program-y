import unittest
from unittest.mock import patch

from programy.security.linking.extension import AccountLinkingExtension


class AccountLinkerExtensionAsserts(unittest.TestCase):

    def assert_no_words(self, context):

        extension = AccountLinkingExtension()
        self.assertIsNotNone(extension)

        self.assertEqual("ACCOUNT LINK FAILED UNKNOWN COMMAND", extension.execute(context, ""))

    def assert_unknown_command(self, context):

        extension = AccountLinkingExtension()
        self.assertIsNotNone(extension)

        self.assertEqual("ACCOUNT LINK FAILED UNKNOWN COMMAND", extension.execute(context, "UNKNOWN COMMAND"))
        self.assertEqual("ACCOUNT LINK FAILED UNKNOWN COMMAND", extension.execute(context, "LINK UNKNOWN"))

    def assert_primary_account_link_success(self, context):

        extension = AccountLinkingExtension()
        self.assertIsNotNone(extension)

        command = "LINK PRIMARY ACCOUNT TESTUSER CONSOLE PASSWORD123"

        result = extension.execute(context, command)
        self.assertIsNotNone(result)
        self.assertTrue(result.startswith("PRIMARY ACCOUNT LINKED"))
        words = result.split(" ")
        self.assertEqual(4, len(words))

    def assert_primary_account_link_no_service(self, context):
        extension = AccountLinkingExtension()
        self.assertIsNotNone(extension)

        command = "LINK PRIMARY ACCOUNT TESTUSER CONSOLE PASSWORD123"
        result = extension.execute(context, command)
        self.assertEquals("INVALID PRIMARY ACCOUNT COMMAND", result)

    def assert_primary_account_link_user_to_client_fails(self, context):
        extension = AccountLinkingExtension()
        self.assertIsNotNone(extension)

        command = "LINK PRIMARY ACCOUNT TESTUSER CONSOLE PASSWORD123"
        result = extension.execute(context, command)
        self.assertEquals("INVALID PRIMARY ACCOUNT COMMAND", result)

    def assert_primary_account_link_failures(self, context):

        extension = AccountLinkingExtension()
        self.assertIsNotNone(extension)

        self.assertEqual("INVALID PRIMARY ACCOUNT COMMAND", extension.execute(context, "LINK PRIMARY OTHER"))
        self.assertEqual("INVALID PRIMARY ACCOUNT COMMAND", extension.execute(context, "LINK PRIMARY ACCOUNT"))
        self.assertEqual("INVALID PRIMARY ACCOUNT COMMAND", extension.execute(context, "LINK PRIMARY ACCOUNT USERID"))
        self.assertEqual("INVALID PRIMARY ACCOUNT COMMAND", extension.execute(context, "LINK PRIMARY ACCOUNT USERID CLIENT"))

    def assert_secondary_account_link_success(self, context):

        extension = AccountLinkingExtension()
        self.assertIsNotNone(extension)

        command = "LINK PRIMARY ACCOUNT TESTUSER CONSOLE PASSWORD123"
        result = extension.execute(context, command)
        words = result.split(" ")
        self.assertEqual(4, len(words))

        command = "LINK SECONDARY ACCOUNT TESTUSER TESTUSER2 FACEBOOK PASSWORD123 %s"%words[3]

        result = extension.execute(context, command)
        self.assertIsNotNone(result)
        self.assertTrue(result.startswith("SECONDARY ACCOUNT LINKED"))

    def assert_secondary_account_link_failures(self, context):

        extension = AccountLinkingExtension()
        self.assertIsNotNone(extension)

        self.assertEqual("INVALID SECONDARY ACCOUNT COMMAND", extension.execute(context, "LINK SECONDARY OTHER"))
        self.assertEqual("INVALID SECONDARY ACCOUNT COMMAND", extension.execute(context, "LINK SECONDARY ACCOUNT"))
        self.assertEqual("INVALID SECONDARY ACCOUNT COMMAND", extension.execute(context, "LINK SECONDARY ACCOUNT PRIMARY_USER"))
        self.assertEqual("INVALID SECONDARY ACCOUNT COMMAND", extension.execute(context, "LINK SECONDARY ACCOUNT PRIMARY_USER SECONDARY_CLIENT"))
        self.assertEqual("INVALID SECONDARY ACCOUNT COMMAND", extension.execute(context, "LINK SECONDARY ACCOUNT PRIMARY_USER SECONDARY_CLIENT PRIMARY_USER"))
        self.assertEqual("INVALID SECONDARY ACCOUNT COMMAND", extension.execute(context, "LINK SECONDARY ACCOUNT PRIMARY_USER SECONDARY_CLIENT PRIMARY_USER"))
        self.assertEqual("INVALID SECONDARY ACCOUNT COMMAND", extension.execute(context, "LINK SECONDARY ACCOUNT PRIMARY_USER SECONDARY_CLIENT PRIMARY_USER GIVEN_TOKEN"))

    def assert_secondary_account_link_no_service(self, context):

        extension = AccountLinkingExtension()
        self.assertIsNotNone(extension)

        command = "LINK PRIMARY ACCOUNT TESTUSER CONSOLE PASSWORD123"
        result = extension.execute(context, command)
        words = result.split(" ")
        self.assertEqual(4, len(words))

        command = "LINK SECONDARY ACCOUNT TESTUSER TESTUSER2 FACEBOOK PASSWORD123 %s"%words[3]

        result = extension.execute(context, command)
        self.assertEquals("INVALID SECONDARY ACCOUNT COMMAND", result)

    def assert_account_linker_none(self, context):

        extension = AccountLinkingExtension()
        self.assertIsNotNone(extension)

        self.assertEqual("INVALID PRIMARY ACCOUNT COMMAND", extension.execute(context, "LINK PRIMARY ACCOUNT TESTUSER CONSOLE PASSWORD123"))
        self.assertEqual("INVALID SECONDARY ACCOUNT COMMAND", extension.execute(context, "LINK SECONDARY ACCOUNT TESTUSER TESTUSER2 FACEBOOK PASSWORD123 XYZ"))
