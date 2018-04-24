import unittest
import unittest.mock
import os

from programy.clients.polling.twitter.client import TwitterBotClient
from programy.clients.polling.twitter.config import TwitterConfiguration
from programy.bot import Bot
from programy.config.bot.bot import BotConfiguration
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
        self.assertEquals("ProgramY AIML2.0 Twitter Client", client.get_description())

        self.assertEquals("username", client._username)
        self.assertEquals(8, client._username_len)

        self.assertEquals("consumer_key", client._consumer_key)
        self.assertEquals("consumer_secret", client._consumer_secret)
        self.assertEquals("access_token", client._access_token)
        self.assertEquals("access_secret", client._access_token_secret)

    #############################################################################################
    # Direct Messages

    def test_get_direct_messages_no_previous(self):
        arguments = MockArgumentParser()
        client = MockTwitterBotClient(arguments)
        self.assertIsNotNone(client)
        self.assertTrue(client.connect())

        client._api._mock_direct_messages = [MockMessage(1, 1, "Message1")]

        messages = client._get_direct_messages(-1)
        self.assertEquals(1, len(messages))

    def test_get_direct_messages_previous(self):
        arguments = MockArgumentParser()
        client = MockTwitterBotClient(arguments)
        self.assertIsNotNone(client)
        self.assertTrue(client.connect())

        client._api._mock_direct_messages = [MockMessage(31, 1, "Message1")]

        messages = client._get_direct_messages(30)
        self.assertEquals(1, len(messages))

    def test_process_direct_message_question(self):
        arguments = MockArgumentParser()
        client = MockTwitterBotClient(arguments)
        self.assertIsNotNone(client)
        self.assertTrue(client.connect())

        client._process_direct_message_question("userid1", "Hello")

        self.assertEqual(1, len(client._api._messages_sent_to))
        self.assertTrue(bool("userid1" in client._api._messages_sent_to))

    def test_process_direct_messages(self):
        arguments = MockArgumentParser()
        client = MockTwitterBotClient(arguments)
        self.assertIsNotNone(client)
        self.assertTrue(client.connect())

        client._api._mock_direct_messages = [MockMessage(31, 1, "Message1")]

        last_message_id = client._process_direct_messages(-1)
        self.assertEqual(31, last_message_id)

    #############################################################################################
    # Followers

    def test_unfollow_non_followers(self):
        arguments = MockArgumentParser()
        client = MockTwitterBotClient(arguments)
        self.assertIsNotNone(client)
        self.assertTrue(client.connect())

        friends = [1, 2, 3, 4]
        followers_ids = [1, 2, 4]

        client._unfollow_non_followers(friends, followers_ids)

        self.assertEquals(1, len(client._api._destroyed_friendships))
        self.assertTrue(bool(3 in client._api._destroyed_friendships))

    def test_follow_new_followers(self):
        arguments = MockArgumentParser()
        client = MockTwitterBotClient(arguments)
        self.assertIsNotNone(client)
        self.assertTrue(client.connect())

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
        self.assertTrue(client.connect())

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

    def test_get_statuses_wrong_number(self):
        arguments = MockArgumentParser()
        client = MockTwitterBotClient(arguments)
        self.assertIsNotNone(client)
        self.assertTrue(client.connect())

        client._api._statuses = []

        statuses = client._get_statuses(-1)
        self.assertIsNotNone(statuses)

    def test_get_statuses_excessive_number(self):
        arguments = MockArgumentParser()
        client = MockTwitterBotClient(arguments)
        self.assertIsNotNone(client)
        self.assertTrue(client.connect())

        client._api._statuses = []

        statuses = client._get_statuses(666)
        self.assertIsNotNone(statuses)

    def test_get_question_from_text(self):
        arguments = MockArgumentParser()
        client = MockTwitterBotClient(arguments)
        self.assertIsNotNone(client)
        self.assertTrue(client.connect())

        client._username = "keiffster"
        client._username_len = 9

        self.assertEquals("Hello", client._get_question_from_text("@keiffster Hello"))
        self.assertIsNone(client._get_question_from_text("keiffster Hello"))
        self.assertIsNone(client._get_question_from_text("Hello"))

    def test_process_status_question(self):
        arguments = MockArgumentParser()
        client = MockTwitterBotClient(arguments)
        self.assertIsNotNone(client)
        self.assertTrue(client.connect())

        client._response = "Hiya"

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
        self.assertTrue(client.connect())

        client._response = "Hiya"

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
        client = MockTwitterBotClient(arguments)
        self.assertIsNotNone(client)
        self.assertTrue(client.connect())

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

    def test_poll(self):
        arguments = MockArgumentParser()
        client = MockTwitterBotClient(arguments)
        self.assertIsNotNone(client)
        self.assertTrue(client.connect())

        client._username = "Keiffster"
        client._username_len = 9

        client.configuration.client_configuration._use_direct_message = True
        client.configuration.client_configuration._auto_follow = True
        client.configuration.client_configuration._use_status = True
        client.configuration.client_configuration._polling_interval = 0

        client._poll( -1, -1)

