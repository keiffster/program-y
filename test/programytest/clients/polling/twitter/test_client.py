import unittest
import unittest.mock
import os

from programy.clients.polling.twitter.client import TwitterBotClient
from programy.clients.polling.twitter.config import TwitterConfiguration
from programy.bot import Bot
from programytest.clients.arguments import MockArgumentParser
from programy.storage.config import FileStorageConfiguration
from programy.storage.stores.file.config import FileStoreConfiguration
from programy.storage.stores.file.store.twitter import FileTwitterStore
from programy.storage.stores.file.engine import FileStorageEngine
from programy.storage.factory import StorageFactory


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

    #############################################################################################
    # Direct Messages

    def test_get_direct_messages_no_previous(self):
        arguments = MockArgumentParser()
        client = MockTwitterBotClient(arguments)
        self.assertIsNotNone(client)
        self.assertTrue(client.connect())

        client._api._mock_direct_messages = [MockMessage(1, 1, "Message1")]

        messages = client._get_direct_messages(-1)
        self.assertEqual(1, len(messages))

    def test_get_direct_messages_previous(self):
        arguments = MockArgumentParser()
        client = MockTwitterBotClient(arguments)
        self.assertIsNotNone(client)
        self.assertTrue(client.connect())

        client._api._mock_direct_messages = [MockMessage(31, 1, "Message1")]

        messages = client._get_direct_messages(30)
        self.assertEqual(1, len(messages))

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

        self.assertEqual(1, len(client._api._destroyed_friendships))
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

        self.assertEqual(1, len(client._api._messages_sent_to))
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

        self.assertEqual(2, len(client._api._destroyed_friendships))
        self.assertTrue(bool(3 in client._api._destroyed_friendships))
        self.assertTrue(bool(4 in client._api._destroyed_friendships))
        self.assertEqual(1, len(client._api._messages_sent_to))
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

        self.assertEqual("Hello", client._get_question_from_text("@keiffster Hello"))
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

        #TODO this writes to local storage rather than /tmp
        file_store_config = FileStorageConfiguration()
        file_store_config._twitter_storage = FileStoreConfiguration(file=os.path.dirname(__file__) + os.sep + "test_files" + os.sep + "gender.txt", format="text", extension="txt", encoding="utf-8", delete_on_start=False)

        storage_engine = FileStorageEngine(file_store_config)

        client.storage_factory._storage_engines[StorageFactory.TWITTER] = storage_engine
        client.storage_factory._store_to_engine_map[StorageFactory.TWITTER] = storage_engine

        client._store_last_message_ids('666', '667')

        ids = client._get_last_message_ids()
        self.assertEqual(ids[0], '666')
        self.assertEqual(ids[1], '667')

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

