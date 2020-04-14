import os
import unittest
import unittest.mock

from programy.bot import Bot
from programy.clients.polling.twitter.client import TwitterBotClient
from programy.clients.polling.twitter.config import TwitterConfiguration
from programy.storage.config import FileStorageConfiguration
from programy.storage.factory import StorageFactory
from programy.storage.stores.file.config import FileStoreConfiguration
from programy.storage.stores.file.engine import FileStorageEngine
from programy.clients.render.text import TextRenderer
from programytest.clients.arguments import MockArgumentParser


class MockMessage(object):

    def __init__(self, id, sender_id, text):
        self.id = id
        self.sender_id = sender_id
        self.text = text


class MockTwitterApi(object):

    def __init__(self):
        self._mock_direct_messages = []
        self._destroyed_friendships = []
        self._messages_sent_to = []
        self._followers = []
        self._friends_ids = []
        self._statuses = []
        self._user = None
        self._status = None

    def direct_messages(self, since_id=-1):
        return self._mock_direct_messages

    def destroy_friendship(self, friend_id):
        self._destroyed_friendships.append(friend_id)

    def send_direct_message(self, id, text):
        self._messages_sent_to.append(id)

    def followers(self):
        return self._followers

    def friends_ids(self):
        return self._friends_ids

    def home_timeline(self, since_id=-1):
        return self._statuses

    def get_user(self, userid):
        return self._user

    def update_status(self, status):
        self._status = status


class MockBot(Bot):

    def __init__(self, config):
        Bot.__init__(self, config)
        self._answer = ""

    def ask_question(self, clientid: str, text: str, srai=False, responselogger=None):
        return self._answer


class MockTwitterBotClient(TwitterBotClient):

    def __init__(self, argument_parser=None):
        self._response = None
        TwitterBotClient.__init__(self, argument_parser)

    def _create_api(self, consumer_key, consumer_secret, access_token, access_token_secret):
        return MockTwitterApi()

    def load_license_keys(self):
        self._license_keys.add_key("TWITTER_USERNAME", "username")
        self._license_keys.add_key("TWITTER_CONSUMER_KEY", "consumer_key")
        self._license_keys.add_key("TWITTER_CONSUMER_SECRET", "consumer_secret")
        self._license_keys.add_key("TWITTER_ACCESS_TOKEN", "access_token")
        self._license_keys.add_key("TWITTER_ACCESS_TOKEN_SECRET", "access_secret")

    def ask_question(self, userid, question):
        return self._response


class TwitterBotClientTests(unittest.TestCase):

    def test_twitter_init(self):
        arguments = MockArgumentParser()
        client = MockTwitterBotClient(arguments)

        self.assertIsNotNone(client.get_client_configuration())
        self.assertIsInstance(client.get_client_configuration(), TwitterConfiguration)
        self.assertEqual("ProgramY AIML2.0 Twitter Client", client.get_description())

        self.assertEqual("username", client._username)
        self.assertEqual(8, client._username_len)

        self.assertEqual("consumer_key", client._consumer_key)
        self.assertEqual("consumer_secret", client._consumer_secret)
        self.assertEqual("access_token", client._access_token)
        self.assertEqual("access_secret", client._access_token_secret)

        self.assertFalse(client._render_callback())
        self.assertIsInstance(client.renderer, TextRenderer)


