import unittest

from programy.security.linking.extension import AccountLinkingExtension


class AccountLinkerExtensionAsserts(unittest.TestCase):

    def assert_unknown_command(self, context):

        extension = AccountLinkingExtension()
        self.assertIsNotNone(extension)

        self.assertEquals("ACCOUNT LINK FAILED UNKNOWN COMMAND", extension.execute(context, "UNKNOWN COMMAND"))
        self.assertEquals("ACCOUNT LINK FAILED UNKNOWN COMMAND", extension.execute(context, "LINK UNKNOWN"))

    def assert_primary_account_link_success(self, context):

        extension = AccountLinkingExtension()
        self.assertIsNotNone(extension)

        command = "LINK PRIMARY ACCOUNT TESTUSER CONSOLE PASSWORD123"

        result = extension.execute(context, command)
        self.assertIsNotNone(result)
        self.assertTrue(result.startswith("PRIMARY ACCOUNT LINKED"))
        words = result.split(" ")
        self.assertEqual(4, len(words))

    def assert_primary_account_link_failures(self, context):

        extension = AccountLinkingExtension()
        self.assertIsNotNone(extension)

        self.assertEquals("INVALID PRIMARY ACCOUNT COMMAND", extension.execute(context, "LINK PRIMARY ACCOUNT"))
        self.assertEquals("INVALID PRIMARY ACCOUNT COMMAND", extension.execute(context, "LINK PRIMARY ACCOUNT USERID"))
        self.assertEquals("INVALID PRIMARY ACCOUNT COMMAND", extension.execute(context, "LINK PRIMARY ACCOUNT USERID CLIENT"))

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

        self.assertEquals("INVALID SECONDARY ACCOUNT COMMAND", extension.execute(context, "LINK SECONDARY ACCOUNT"))
        self.assertEquals("INVALID SECONDARY ACCOUNT COMMAND", extension.execute(context, "LINK SECONDARY ACCOUNT PRIMARY_USER"))
        self.assertEquals("INVALID SECONDARY ACCOUNT COMMAND", extension.execute(context, "LINK SECONDARY ACCOUNT PRIMARY_USER SECONDARY_CLIENT"))
        self.assertEquals("INVALID SECONDARY ACCOUNT COMMAND", extension.execute(context, "LINK SECONDARY ACCOUNT PRIMARY_USER SECONDARY_CLIENT PRIMARY_USER"))
        self.assertEquals("INVALID SECONDARY ACCOUNT COMMAND", extension.execute(context, "LINK SECONDARY ACCOUNT PRIMARY_USER SECONDARY_CLIENT PRIMARY_USER"))
        self.assertEquals("INVALID SECONDARY ACCOUNT COMMAND", extension.execute(context, "LINK SECONDARY ACCOUNT PRIMARY_USER SECONDARY_CLIENT PRIMARY_USER GIVEN_TOKEN"))
