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

    def test_get_bot_known(self):

        client = PropertiesAdminExtensionClient()
        client_context = client.create_client_context("testid")

        client_context.brain.properties.add_property("PROP1", "Value1")

        extension = PropertiesAdminExtension()
        self.assertIsNotNone(extension)

        result = extension.execute(client_context, "GET BOT PROP1")
        self.assertIsNotNone(result)
        self.assertEqual("Value1", result)

    def test_get_bot_unknown(self):

        client = PropertiesAdminExtensionClient()
        client_context = client.create_client_context("testid")

        extension = PropertiesAdminExtension()
        self.assertIsNotNone(extension)

        result = extension.execute(client_context, "GET BOT XXXXX")
        self.assertIsNotNone(result)
        self.assertEqual("unknown", result)

    def test_get_user_local_known(self):

        client = PropertiesAdminExtensionClient()
        client_context = client.create_client_context("testid")

        question = Question()
        conversation = client_context.bot.get_conversation(client_context)
        conversation.record_dialog(question)
        conversation.set_property("PROP1", "Value1")

        extension = PropertiesAdminExtension()
        self.assertIsNotNone(extension)

        result = extension.execute(client_context, "GET USER LOCAL PROP1")
        self.assertIsNotNone(result)
        self.assertEqual("Value1", result)

    def test_get_user_Local_unknown(self):

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

    def test_get_bot(self):

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
