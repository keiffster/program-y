import unittest

from programy.dialog.question import Question
from programy.extensions.admin.properties import PropertiesAdminExtension
from programytest.client import TestClient


class PropertiesAdminExtensionClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(PropertiesAdminExtensionClient, self).load_configuration(arguments)


class PropertiesAdminExtensionTests(unittest.TestCase):

    def test_unknown_properties_command(self):
        client = PropertiesAdminExtensionClient()
        client_context = client.create_client_context("testid")

        extension = PropertiesAdminExtension()
        self.assertIsNotNone(extension)

        self.assertEquals("Unknown properties command [XXXX]", extension.execute(client_context, "XXXX"))

    def test_unknown_gets_command(self):
        client = PropertiesAdminExtensionClient()
        client_context = client.create_client_context("testid")

        extension = PropertiesAdminExtension()
        self.assertIsNotNone(extension)

        self.assertEquals("Unknown GET command [XXXX]", extension.execute(client_context, "GET XXXX"))

    def test_get_bot_incomplete(self):

        client = PropertiesAdminExtensionClient()
        client_context = client.create_client_context("testid")

        client_context.brain.properties.add_property("PROP1", "Value1")

        extension = PropertiesAdminExtension()
        self.assertIsNotNone(extension)

        result = extension.execute(client_context, "GET BOT")
        self.assertEqual("Missing variable name for GET BOT", result)

    def test_get_bot_known(self):

        client = PropertiesAdminExtensionClient()
        client_context = client.create_client_context("testid")

        client_context.brain.properties.add_property("PROP1", "Value1")

        extension = PropertiesAdminExtension()
        self.assertIsNotNone(extension)

        result = extension.execute(client_context, "GET BOT PROP1")
        self.assertEqual("Value1", result)

    def test_get_bot_unknown(self):

        client = PropertiesAdminExtensionClient()
        client_context = client.create_client_context("testid")

        extension = PropertiesAdminExtension()
        self.assertIsNotNone(extension)

        result = extension.execute(client_context, "GET BOT XXXXX")
        self.assertIsNotNone(result)
        self.assertEqual("unknown", result)

    def test_get_user_incomplete(self):

        client = PropertiesAdminExtensionClient()
        client_context = client.create_client_context("testid")

        question = Question()
        conversation = client_context.bot.get_conversation(client_context)
        conversation.record_dialog(question)
        conversation.set_property("PROP1", "Value1")

        extension = PropertiesAdminExtension()
        self.assertIsNotNone(extension)

        result = extension.execute(client_context, "GET USER")
        self.assertIsNotNone(result)
        self.assertEqual("Invalid syntax for GET USER, LOCAL or GLOBAL", result)

    def test_get_user_other(self):

        client = PropertiesAdminExtensionClient()
        client_context = client.create_client_context("testid")

        question = Question()
        conversation = client_context.bot.get_conversation(client_context)
        conversation.record_dialog(question)
        conversation.set_property("PROP1", "Value1")

        extension = PropertiesAdminExtension()
        self.assertIsNotNone(extension)

        result = extension.execute(client_context, "GET USER XXXX")
        self.assertIsNotNone(result)
        self.assertEqual("Invalid GET USER var type [XXXX]", result)

    def test_get_user_local_missing(self):

        client = PropertiesAdminExtensionClient()
        client_context = client.create_client_context("testid")

        question = Question()
        conversation = client_context.bot.get_conversation(client_context)
        conversation.record_dialog(question)
        conversation.set_property("PROP1", "Value1")

        extension = PropertiesAdminExtension()
        self.assertIsNotNone(extension)

        result = extension.execute(client_context, "GET USER LOCAL")
        self.assertIsNotNone(result)
        self.assertEqual("Missing variable name for GET USER", result)

    def test_get_user_global_missing(self):

        client = PropertiesAdminExtensionClient()
        client_context = client.create_client_context("testid")

        question = Question()
        conversation = client_context.bot.get_conversation(client_context)
        conversation.record_dialog(question)
        conversation.set_property("PROP1", "Value1")

        extension = PropertiesAdminExtension()
        self.assertIsNotNone(extension)

        result = extension.execute(client_context, "GET USER GLOBAL")
        self.assertIsNotNone(result)
        self.assertEqual("Missing variable name for GET USER", result)

    def test_get_user_local_known(self):

        client = PropertiesAdminExtensionClient()
        client_context = client.create_client_context("testid")

        question = Question()
        question.set_property("PROP1", "Value1")
        conversation = client_context.bot.get_conversation(client_context)
        conversation.record_dialog(question)

        extension = PropertiesAdminExtension()
        self.assertIsNotNone(extension)

        result = extension.execute(client_context, "GET USER LOCAL PROP1")
        self.assertIsNotNone(result)
        self.assertEqual("Value1", result)

    def test_get_user_local_unknown(self):

        client = PropertiesAdminExtensionClient()
        client_context = client.create_client_context("testid")

        extension = PropertiesAdminExtension()
        self.assertIsNotNone(extension)

        result = extension.execute(client_context, "GET USER LOCAL XXX")
        self.assertIsNotNone(result)
        self.assertEqual("unknown", result)

    def test_get_user_global_known(self):

        client = PropertiesAdminExtensionClient()
        client_context = client.create_client_context("testid")

        client_context.bot.get_conversation(client_context).set_property("PROP1", "Value1")

        extension = PropertiesAdminExtension()
        self.assertIsNotNone(extension)

        result = extension.execute(client_context, "GET USER GLOBAL PROP1")
        self.assertIsNotNone(result)
        self.assertEqual("Value1", result)

    def test_get_user_global_unknown(self):

        client = PropertiesAdminExtensionClient()
        client_context = client.create_client_context("testid")

        extension = PropertiesAdminExtension()
        self.assertIsNotNone(extension)

        result = extension.execute(client_context, "GET USER GLOBAL XXX")
        self.assertIsNotNone(result)
        self.assertEqual("unknown", result)

    def test_get_bot_props(self):

        client = PropertiesAdminExtensionClient()
        client_context = client.create_client_context("testid")

        client_context.brain.properties.add_property("key1", "val1")
        client_context.brain.properties.add_property("key2", "val2")

        extension = PropertiesAdminExtension()
        self.assertIsNotNone(extension)

        client_context.bot.get_conversation(client_context)

        result = extension.execute(client_context, "BOT")
        self.assertIsNotNone(result)
        self.assertEqual("Properties:<br /><ul><li>key1 = val1</li><li>key2 = val2</li></ul><br />", result)

    def test_get_bot_no_props(self):

        client = PropertiesAdminExtensionClient()
        client_context = client.create_client_context("testid")

        extension = PropertiesAdminExtension()
        self.assertIsNotNone(extension)

        client_context.bot.get_conversation(client_context)

        result = extension.execute(client_context, "BOT")
        self.assertIsNotNone(result)
        self.assertEqual("Properties:<br /><ul></ul><br />", result)

    def test_get_user(self):

        client = PropertiesAdminExtensionClient()
        client_context = client.create_client_context("testid")

        extension = PropertiesAdminExtension()
        self.assertIsNotNone(extension)

        client_context.bot.get_conversation(client_context)

        result = extension.execute(client_context, "USER")
        self.assertIsNotNone(result)
        self.assertEqual("Properties:<br /><ul><li>topic = *</li></ul><br />", result)

    def test_get_user_no_converstion(self):

        client = PropertiesAdminExtensionClient()
        client_context = client.create_client_context("testid")

        extension = PropertiesAdminExtension()
        self.assertIsNotNone(extension)

        result = extension.execute(client_context, "USER")
        self.assertIsNotNone(result)
        self.assertEqual("No conversation currently available", result)
