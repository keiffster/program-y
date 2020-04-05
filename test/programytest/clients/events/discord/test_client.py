import unittest

from programy.clients.events.discord.client import DiscordBotClient
from programy.clients.events.discord.client import DiscordClient
from programy.clients.events.discord.config import DiscordConfiguration
from programy.clients.render.text import TextRenderer
from programytest.clients.arguments import MockArgumentParser


class MockDiscordBotClient(DiscordBotClient):

    def __init__(self, discord_client: DiscordClient, argument_parser=None):
        DiscordBotClient.__init__(self, discord_client, argument_parser)

    def get_discord_user(self):
        return 1234567890

    def get_license_keys(self):
        return 'XYZ'

    def ask_question(self, client_context, question):
        return "Hello there."

class MockAuthor():

    def __init__(self, id):
        self.id = id


class MockDiscordClient():

    def __init__(self, user=MockAuthor("testid")):
        self.user = user

    def __eq__(self, other):
        return other.id == self.user.id


class MockMessage():

    def __init__(self, author, content):
        self.author = author
        self.content = content


class DiscordBotClientTests(unittest.TestCase):

    def test_init(self):
        arguments = MockArgumentParser()

        client = MockDiscordBotClient(MockDiscordClient(), arguments)
        self.assertIsNotNone(client)
        self.assertIsNotNone(client.arguments)
        self.assertEqual(client.id, "Discord")
        self.assertEqual('ProgramY AIML2.0 Client', client.get_description())
        self.assertIsInstance(client.get_client_configuration(), DiscordConfiguration)

        self.assertFalse(client._render_callback())
        self.assertIsInstance(client.renderer, TextRenderer)

    def test_on_ready(self):
        arguments = MockArgumentParser()

        client = MockDiscordBotClient(MockDiscordClient(), arguments)
        self.assertIsNotNone(client)

        response = client.on_ready()
        self.assertTrue(response)

    def test_on_message(self):
        arguments = MockArgumentParser()

        client = MockDiscordBotClient(MockDiscordClient(), arguments)
        self.assertIsNotNone(client)

        response = client.on_message(MockMessage(MockAuthor(1234567891), "hello"))
        self.assertIsNotNone(response)

    def test_on_message_same_user(self):
        arguments = MockArgumentParser()

        user = MockAuthor(1234567890)

        client = MockDiscordBotClient(MockDiscordClient(user=user), arguments)
        self.assertIsNotNone(client)

        response = client.on_message(MockMessage(user, "hello"))
        self.assertEqual('Hello there.', response)
