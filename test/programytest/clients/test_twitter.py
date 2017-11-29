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

    def ask_question(self, userid, text, responselogger=None):
        return self.answer

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

class MockTwitterBotClient(TwitterBotClient):

    def __init__(self, argument_parser=None):
        TwitterBotClient.__init__(self, argument_parser)
        self._use_polling_real = True
        self._polled = False

    def _create_api(self, consumer_key, consumer_secret, access_token, access_token_secret):
        return MockTwitterApi()

    def _use_polling(self):
        if self._use_polling_real:
            super(MockTwitterBotClient, self).use_polling(self)
        else:
            self._polled = True

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

        client._get_username(bot)
        self.assertEquals("Username", client._username)
        self.assertEquals(8, client._username_len)

    def test_twitter_get_consumer_secrets(self):
        arguments = MockArgumentParser()
        client = TwitterBotClient(arguments)
        self.assertIsNotNone(client)

        bot = MockBot()
        bot.license_keys = MockLicenseKeys({"TWITTER_CONSUMER_KEY": "Key", "TWITTER_CONSUMER_SECRET": "Secret"})

        consumer_key, consumer_secret = client._get_consumer_secrets(bot)
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

        access_token, access_token_secret = client._get_access_secrets(bot)
        self.assertIsNotNone(access_token)
        self.assertEquals("Access", access_token)
        self.assertIsNotNone(access_token_secret)
        self.assertEquals("Secret", access_token_secret)

    def test_twitter_initialise(self):
        arguments = MockArgumentParser()
        client = MockTwitterBotClient(arguments)
        self.assertIsNotNone(client)

        client._bot = MockBot()
        client.bot.license_keys = MockLicenseKeys({"TWITTER_USERNAME": "Username",
                                            "TWITTER_CONSUMER_KEY": "Key", "TWITTER_CONSUMER_SECRET": "Secret",
                                            "TWITTER_ACCESS_TOKEN": "Access", "TWITTER_ACCESS_TOKEN_SECRET": "Secret"
                                            })
        client._initialise()
        self.assertIsNotNone(client._api)

    #############################################################################################
    # Direct Messages

    def test_get_direct_messages_no_previous(self):
        arguments = MockArgumentParser()
        client = MockTwitterBotClient(arguments)
        self.assertIsNotNone(client)

        client._bot = MockBot()
        client.bot.license_keys = MockLicenseKeys({"TWITTER_USERNAME": "Username",
                                            "TWITTER_CONSUMER_KEY": "Key", "TWITTER_CONSUMER_SECRET": "Secret",
                                            "TWITTER_ACCESS_TOKEN": "Access", "TWITTER_ACCESS_TOKEN_SECRET": "Secret"
                                            })
        client._initialise()

        client._api._mock_direct_messages = [MockMessage(1, "Message1", 1)]

        messages = client._get_direct_messages(-1)
        self.assertEquals(1, len(messages))

    def test_get_direct_messages_previous(self):
        arguments = MockArgumentParser()
        client = MockTwitterBotClient(arguments)
        self.assertIsNotNone(client)

        client._bot = MockBot()
        client.bot.license_keys = MockLicenseKeys({"TWITTER_USERNAME": "Username",
                                            "TWITTER_CONSUMER_KEY": "Key", "TWITTER_CONSUMER_SECRET": "Secret",
                                            "TWITTER_ACCESS_TOKEN": "Access", "TWITTER_ACCESS_TOKEN_SECRET": "Secret"
                                            })
        client._initialise()

        client._api._mock_direct_messages = [MockMessage(31, "Message1", 1)]

        messages = client._get_direct_messages(30)
        self.assertEquals(1, len(messages))

    def test_process_direct_message_question(self):
        arguments = MockArgumentParser()
        client = MockTwitterBotClient(arguments)
        self.assertIsNotNone(client)

        client._bot = MockBot()
        client.bot.license_keys = MockLicenseKeys({"TWITTER_USERNAME": "Username",
                                            "TWITTER_CONSUMER_KEY": "Key", "TWITTER_CONSUMER_SECRET": "Secret",
                                            "TWITTER_ACCESS_TOKEN": "Access", "TWITTER_ACCESS_TOKEN_SECRET": "Secret"
                                            })
        client._initialise()

        client.bot.answer = "Hiya"
        client._process_direct_message_question("userid1", "Hello")

        self.assertEqual(1, len(client._api._messages_sent_to))
        self.assertTrue(bool("userid1" in client._api._messages_sent_to))

    def test_process_direct_messages(self):
        arguments = MockArgumentParser()
        client = MockTwitterBotClient(arguments)
        self.assertIsNotNone(client)

        client._bot = MockBot()
        client.bot.license_keys = MockLicenseKeys({"TWITTER_USERNAME": "Username",
                                            "TWITTER_CONSUMER_KEY": "Key", "TWITTER_CONSUMER_SECRET": "Secret",
                                            "TWITTER_ACCESS_TOKEN": "Access", "TWITTER_ACCESS_TOKEN_SECRET": "Secret"
                                            })
        client._initialise()

        client.bot.answer = "Hiya"
        client._api._mock_direct_messages = [MockMessage(31, "Message1", 1)]

        last_message_id = client._process_direct_messages(-1)
        self.assertEqual(31, last_message_id)

    #############################################################################################
    # Followers

    def test_unfollow_non_followers(self):
        arguments = MockArgumentParser()
        client = MockTwitterBotClient(arguments)
        self.assertIsNotNone(client)

        client._bot = MockBot()
        client.bot.license_keys = MockLicenseKeys({"TWITTER_USERNAME": "Username",
                                            "TWITTER_CONSUMER_KEY": "Key", "TWITTER_CONSUMER_SECRET": "Secret",
                                            "TWITTER_ACCESS_TOKEN": "Access", "TWITTER_ACCESS_TOKEN_SECRET": "Secret"
                                            })
        client._initialise()

        friends = [1, 2, 3, 4]
        followers_ids = [1, 2, 4]

        client._unfollow_non_followers(friends, followers_ids)

        self.assertEquals(1, len(client._api._destroyed_friendships))
        self.assertTrue(bool(3 in client._api._destroyed_friendships))

    def test_follow_new_followers(self):
        arguments = MockArgumentParser()
        client = MockTwitterBotClient(arguments)
        self.assertIsNotNone(client)

        client._bot = MockBot()
        client.bot.license_keys = MockLicenseKeys({"TWITTER_USERNAME": "Username",
                                            "TWITTER_CONSUMER_KEY": "Key", "TWITTER_CONSUMER_SECRET": "Secret",
                                            "TWITTER_ACCESS_TOKEN": "Access", "TWITTER_ACCESS_TOKEN_SECRET": "Secret"
                                            })
        client._initialise()

        follower1 = unittest.mock.Mock()
        follower1.follow.return_value = None
        follower1.id = 3

        followers = [follower1]
        friends = [1, 2, 4]

        client._follow_new_followers(followers, friends)

        self.assertEquals(1, len(client._api._messages_sent_to))
        self.assertTrue(bool(3 in client._api._messages_sent_to))

    def test_process_followers(self):
        arguments = MockArgumentParser()
        client = MockTwitterBotClient(arguments)
        self.assertIsNotNone(client)

        client._bot = MockBot()
        client.bot.license_keys = MockLicenseKeys({"TWITTER_USERNAME": "Username",
                                            "TWITTER_CONSUMER_KEY": "Key", "TWITTER_CONSUMER_SECRET": "Secret",
                                            "TWITTER_ACCESS_TOKEN": "Access", "TWITTER_ACCESS_TOKEN_SECRET": "Secret"
                                            })
        client._initialise()

        follower1 = unittest.mock.Mock()
        follower1.follow.return_value = None
        follower1.id = 1

        follower2 = unittest.mock.Mock()
        follower2.follow.return_value = None
        follower2.id = 2

        client._api._followers = [follower1, follower2]
        client._api._friends_ids = [2, 3, 4]

        client._process_followers()

        self.assertEquals(2, len(client._api._destroyed_friendships))
        self.assertTrue(bool(3 in client._api._destroyed_friendships))
        self.assertTrue(bool(4 in client._api._destroyed_friendships))
        self.assertEquals(1, len(client._api._messages_sent_to))
        self.assertTrue(bool(1 in client._api._messages_sent_to))

    #############################################################################################
    # Status (Tweets)

    def test_get_statuses_no(self):
        arguments = MockArgumentParser()
        client = MockTwitterBotClient(arguments)
        self.assertIsNotNone(client)

        client._bot = MockBot()
        client.bot.license_keys = MockLicenseKeys({"TWITTER_USERNAME": "Username",
                                                   "TWITTER_CONSUMER_KEY": "Key", "TWITTER_CONSUMER_SECRET": "Secret",
                                                   "TWITTER_ACCESS_TOKEN": "Access", "TWITTER_ACCESS_TOKEN_SECRET": "Secret"
                                                   })
        client._initialise()

        client._api._statuses = []

        statuses = client._get_statuses(-1)
        self.assertIsNotNone(statuses)

    def test_get_statuses_no(self):
        arguments = MockArgumentParser()
        client = MockTwitterBotClient(arguments)
        self.assertIsNotNone(client)

        client._bot = MockBot()
        client.bot.license_keys = MockLicenseKeys({"TWITTER_USERNAME": "Username",
                                                   "TWITTER_CONSUMER_KEY": "Key", "TWITTER_CONSUMER_SECRET": "Secret",
                                                   "TWITTER_ACCESS_TOKEN": "Access",
                                                   "TWITTER_ACCESS_TOKEN_SECRET": "Secret"
                                                   })
        client._initialise()

        client._api._statuses = []

        statuses = client._get_statuses(666)
        self.assertIsNotNone(statuses)

    def test_get_question_from_text(self):
        arguments = MockArgumentParser()
        client = MockTwitterBotClient(arguments)
        self.assertIsNotNone(client)

        client._username = "keiffster"
        client._username_len = 9

        self.assertEquals("Hello", client._get_question_from_text("@keiffster Hello"))
        self.assertIsNone(client._get_question_from_text("keiffster Hello"))
        self.assertIsNone(client._get_question_from_text("Hello"))

    def test_process_status_question(self):
        arguments = MockArgumentParser()
        client = MockTwitterBotClient(arguments)
        self.assertIsNotNone(client)

        client._bot = MockBot()
        client.bot.license_keys = MockLicenseKeys({"TWITTER_USERNAME": "Username",
                                                   "TWITTER_CONSUMER_KEY": "Key", "TWITTER_CONSUMER_SECRET": "Secret",
                                                   "TWITTER_ACCESS_TOKEN": "Access",
                                                   "TWITTER_ACCESS_TOKEN_SECRET": "Secret"
                                                   })
        client._initialise()
        client.bot.answer = "Hiya"
        client._username = "keiffster"
        client._username_len = 9

        client._api._user = unittest.mock.Mock()
        client._api._user.screen_name = "BigFred"

        client._process_status_question("userid1", "@keiffster Hello")

        self.assertIsNotNone(client._api._status)
        self.assertEqual("@BigFred Hiya", client._api._status)

    def test_process_statuses(self):
        arguments = MockArgumentParser()
        client = MockTwitterBotClient(arguments)
        self.assertIsNotNone(client)

        client._bot = MockBot()
        client.bot.license_keys = MockLicenseKeys({"TWITTER_USERNAME": "Username",
                                                   "TWITTER_CONSUMER_KEY": "Key", "TWITTER_CONSUMER_SECRET": "Secret",
                                                   "TWITTER_ACCESS_TOKEN": "Access", "TWITTER_ACCESS_TOKEN_SECRET": "Secret"
                                                   })
        client._initialise()
        client.bot.answer = "Hiya"
        client._username = "Keiffster"
        client._username_len = 9

        client._api._user = unittest.mock.Mock()
        client._api._user.screen_name = "BigFred"

        status1 = unittest.mock.Mock()
        status1.id = 1
        status1.author = unittest.mock.Mock()
        status1.author.screen_name = "keiffster"
        status1.user = unittest.mock.Mock()
        status1.user.id = 66
        status1.text = "@Keiffster Hello"

        status2 = unittest.mock.Mock()
        status2.id = 2
        status2.author = unittest.mock.Mock()
        status2.author.screen_name = "BigFred"
        status2.user = unittest.mock.Mock()
        status2.user.id = 68
        status2.text = "@Keiffster Hello"

        client._api._statuses = [status1, status2]

        client._process_statuses(-1)

        self.assertIsNotNone(client._api._status)
        self.assertEqual("@BigFred Hiya", client._api._status)

    #############################################################################################
    # Message ID Storage

    def test_message_ids_save_load(self):
        arguments = MockArgumentParser()
        client = TwitterBotClient(arguments)
        self.assertIsNotNone(client)

        client.configuration.client_configuration._storage = 'file'
        if os.name == 'posix':
            client.configuration.client_configuration._storage_location = "/tmp/twitter.txt"
        else:
            client.configuration.client_configuration._storage_location = "C:\Windows\Temp/twitter.txt"

        if os.path.exists(client.configuration.client_configuration.storage_location):
            os.remove(client.configuration.client_configuration.storage_location)
        self.assertFalse(os.path.exists(client.configuration.client_configuration.storage_location))

        client._store_last_message_ids(666, 667)

        self.assertTrue(os.path.exists(client.configuration.client_configuration.storage_location))

        ids = client._get_last_message_ids()
        self.assertEquals(ids[0], 666)
        self.assertEquals(ids[1], 667)

    #############################################################################################
    # Execution

    def test_twitter_user_streaming(self):
        arguments = MockArgumentParser()
        client = TwitterBotClient(arguments)
        self.assertIsNotNone(client)

        with self.assertRaises(Exception):
            client._use_streaming()

    def test_poll(self):
        arguments = MockArgumentParser()
        client = MockTwitterBotClient(arguments)
        self.assertIsNotNone(client)

        client._bot = MockBot()
        client.bot.license_keys = MockLicenseKeys({"TWITTER_USERNAME": "Username",
                                                   "TWITTER_CONSUMER_KEY": "Key", "TWITTER_CONSUMER_SECRET": "Secret",
                                                   "TWITTER_ACCESS_TOKEN": "Access", "TWITTER_ACCESS_TOKEN_SECRET": "Secret"
                                                   })
        client._initialise()
        client.bot.answer = "Hiya"
        client._username = "Keiffster"
        client._username_len = 9

        client.configuration.client_configuration._use_direct_message = True
        client.configuration.client_configuration._auto_follow = True
        client.configuration.client_configuration._use_status = True
        client.configuration.client_configuration._polling_interval = 0

        client._poll( -1, -1)

    def test_run_with_streaming(self):
        arguments = MockArgumentParser()
        client = MockTwitterBotClient(arguments)
        self.assertIsNotNone(client)

        client._bot = MockBot()
        client.bot.license_keys = MockLicenseKeys({"TWITTER_USERNAME": "Username",
                                                   "TWITTER_CONSUMER_KEY": "Key", "TWITTER_CONSUMER_SECRET": "Secret",
                                                   "TWITTER_ACCESS_TOKEN": "Access", "TWITTER_ACCESS_TOKEN_SECRET": "Secret"
                                                   })

        client.configuration.client_configuration._streaming = True
        client.configuration.client_configuration._polling = False

        with self.assertRaises(Exception):
            client._run()

    def test_run_with_polling(self):
        arguments = MockArgumentParser()
        client = MockTwitterBotClient(arguments)
        self.assertIsNotNone(client)

        client._bot = MockBot()
        client.bot.license_keys = MockLicenseKeys({"TWITTER_USERNAME": "Username",
                                                   "TWITTER_CONSUMER_KEY": "Key", "TWITTER_CONSUMER_SECRET": "Secret",
                                                   "TWITTER_ACCESS_TOKEN": "Access", "TWITTER_ACCESS_TOKEN_SECRET": "Secret"
                                                   })

        client.configuration.client_configuration._streaming = False
        client.configuration.client_configuration._polling = True

        client._use_polling_real = False
        client.run()
        self.assertTrue(client._polled)