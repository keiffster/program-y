import unittest
import unittest.mock
import os

from programy.clients.twitter import TwitterBotClient
from programy.config.sections.client.twitter import TwitterConfiguration

from programytest.clients.arguments import MockArgumentParser

class MockBot(object):

    def __init__(self):
        self.license_keys = {}
        self.answer = None

    def ask_question(self, userid, text):
        return self.answer

class MockMessage(object):

    def __init__(self, id, sender_id, text):
        self.id = id
        self.sender_id = sender_id
        self.text = text

class MockTwitterApi(object):

    def __init__(self):
        self._mock_direct_messages = []

    def direct_messages(self, since_id=-1):
        return self._mock_direct_messages

    def send_direct_message(self, userid, text):
        self.userid = userid
        self.text = text

class MockTwitterBotClient(TwitterBotClient):

    def __init__(self, argument_parser=None):
        TwitterBotClient.__init__(self, argument_parser)

    def create_api(self, consumer_key, consumer_secret, access_token, access_token_secret):
        return MockTwitterApi()

class MockLicenseKeys(object):

    def __init__(self, keys=None):
        if keys is not None:
            self.keys = keys
        else:
            self.keys = {}

    def get_key(self, key):
        return self.keys[key]

class TwitterBotClientTests(unittest.TestCase):

    def test_twitter_client(self):
        arguments = MockArgumentParser()
        client = TwitterBotClient(arguments)
        self.assertIsNotNone(client)

        self.assertIsNotNone(client.get_client_configuration())
        self.assertIsInstance(client.get_client_configuration(), TwitterConfiguration)

        client.set_environment()
        self.assertEquals("Twitter", client.bot.brain.properties.property("env"))

    def test_twitter_get_username(self):
        arguments = MockArgumentParser()
        client = TwitterBotClient(arguments)
        self.assertIsNotNone(client)

        bot = MockBot()
        bot.license_keys = MockLicenseKeys({"TWITTER_USERNAME": "Username"})

        client.get_username(bot)
        self.assertEquals("Username", client._username)
        self.assertEquals(8, client._username_len)

    def test_twitter_get_consumer_secrets(self):
        arguments = MockArgumentParser()
        client = TwitterBotClient(arguments)
        self.assertIsNotNone(client)

        bot = MockBot()
        bot.license_keys = MockLicenseKeys({"TWITTER_CONSUMER_KEY": "Key", "TWITTER_CONSUMER_SECRET": "Secret"})

        consumer_key, consumer_secret = client.get_consumer_secrets(bot)
        self.assertIsNotNone(consumer_key)
        self.assertEquals("Key", consumer_key)
        self.assertIsNotNone(consumer_secret)
        self.assertEquals("Secret", consumer_secret)

    def test_twitter_get_access_secrets(self):
        arguments = MockArgumentParser()
        client = TwitterBotClient(arguments)
        self.assertIsNotNone(client)

        bot = MockBot()
        bot.license_keys = MockLicenseKeys({"TWITTER_ACCESS_TOKEN": "Access", "TWITTER_ACCESS_TOKEN_SECRET": "Secret"})

        access_token, access_token_secret = client.get_access_secrets(bot)
        self.assertIsNotNone(access_token)
        self.assertEquals("Access", access_token)
        self.assertIsNotNone(access_token_secret)
        self.assertEquals("Secret", access_token_secret)

    def test_twitter_initialise(self):
        arguments = MockArgumentParser()
        client = MockTwitterBotClient(arguments)
        self.assertIsNotNone(client)

        client.bot = MockBot()
        client.bot.license_keys = MockLicenseKeys({"TWITTER_USERNAME": "Username",
                                            "TWITTER_CONSUMER_KEY": "Key", "TWITTER_CONSUMER_SECRET": "Secret",
                                            "TWITTER_ACCESS_TOKEN": "Access", "TWITTER_ACCESS_TOKEN_SECRET": "Secret"
                                            })
        client.initialise()
        self.assertIsNotNone(client._api)

    #############################################################################################
    # Direct Messages

    def test_get_direct_messages_no_previous(self):
        arguments = MockArgumentParser()
        client = MockTwitterBotClient(arguments)
        self.assertIsNotNone(client)

        client.bot = MockBot()
        client.bot.license_keys = MockLicenseKeys({"TWITTER_USERNAME": "Username",
                                            "TWITTER_CONSUMER_KEY": "Key", "TWITTER_CONSUMER_SECRET": "Secret",
                                            "TWITTER_ACCESS_TOKEN": "Access", "TWITTER_ACCESS_TOKEN_SECRET": "Secret"
                                            })
        client.initialise()

        client._api._mock_direct_messages = [MockMessage(1, "Message1", 1)]

        messages = client.get_direct_messages(-1)
        self.assertEquals(1, len(messages))

    def test_get_direct_messages_previous(self):
        arguments = MockArgumentParser()
        client = MockTwitterBotClient(arguments)
        self.assertIsNotNone(client)

        client.bot = MockBot()
        client.bot.license_keys = MockLicenseKeys({"TWITTER_USERNAME": "Username",
                                            "TWITTER_CONSUMER_KEY": "Key", "TWITTER_CONSUMER_SECRET": "Secret",
                                            "TWITTER_ACCESS_TOKEN": "Access", "TWITTER_ACCESS_TOKEN_SECRET": "Secret"
                                            })
        client.initialise()

        client._api._mock_direct_messages = [MockMessage(31, "Message1", 1)]

        messages = client.get_direct_messages(30)
        self.assertEquals(1, len(messages))

    def test_process_direct_message_question(self):
        arguments = MockArgumentParser()
        client = MockTwitterBotClient(arguments)
        self.assertIsNotNone(client)

        client.bot = MockBot()
        client.bot.license_keys = MockLicenseKeys({"TWITTER_USERNAME": "Username",
                                            "TWITTER_CONSUMER_KEY": "Key", "TWITTER_CONSUMER_SECRET": "Secret",
                                            "TWITTER_ACCESS_TOKEN": "Access", "TWITTER_ACCESS_TOKEN_SECRET": "Secret"
                                            })
        client.initialise()

        client.bot.answer = "Hiya"
        client.process_direct_message_question("userid1", "Hello")

        self.assertEqual("userid1", client._api.userid)
        self.assertEqual("Hiya", client._api.text)

    def test_process_direct_messages(self):

        arguments = MockArgumentParser()
        client = MockTwitterBotClient(arguments)
        self.assertIsNotNone(client)

        client.bot = MockBot()
        client.bot.license_keys = MockLicenseKeys({"TWITTER_USERNAME": "Username",
                                            "TWITTER_CONSUMER_KEY": "Key", "TWITTER_CONSUMER_SECRET": "Secret",
                                            "TWITTER_ACCESS_TOKEN": "Access", "TWITTER_ACCESS_TOKEN_SECRET": "Secret"
                                            })
        client.initialise()

        client.bot.answer = "Hiya"
        client._api._mock_direct_messages = [MockMessage(31, "Message1", 1)]

        last_message_id = client.process_direct_messages(-1)
        self.assertEqual(31, last_message_id)

    #############################################################################################
    # Followers

    #def unfollow_non_followers(self, friends, followers_ids):
    #def follow_new_followers(self, followers, friends):
    #def process_followers(self):

    #############################################################################################
    # Status (Tweets)

    #def get_statuses(self, last_status_id):
    #def process_statuses(self, last_status_id):
    #def get_question_from_text(self, text):
    #def process_status_question(self, userid, text):

    #############################################################################################
    # Message ID Storage

    def test_message_ids_save_load(self):
        arguments = MockArgumentParser()
        client = TwitterBotClient(arguments)
        self.assertIsNotNone(client)

        client.configuration.client_configuration._storage = 'file'
        client.configuration.client_configuration._storage_location = "/tmp/twitter.txt"

        if os.path.exists(client.configuration.client_configuration.storage_location):
            os.remove(client.configuration.client_configuration.storage_location)
        self.assertFalse(os.path.exists(client.configuration.client_configuration.storage_location))

        client.store_last_message_ids(666, 667)

        self.assertTrue(os.path.exists(client.configuration.client_configuration.storage_location))

        ids = client.get_last_message_ids()
        self.assertEquals(ids[0], 666)
        self.assertEquals(ids[1], 667)

    #############################################################################################
    # Execution

    #def use_polling(self):

    def test_twitter_user_streaming(self):
        arguments = MockArgumentParser()
        client = TwitterBotClient(arguments)
        self.assertIsNotNone(client)

        with self.assertRaises(Exception):
            client.use_streaming()

    #def run(self):
