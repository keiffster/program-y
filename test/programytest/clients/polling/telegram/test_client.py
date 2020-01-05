import unittest.mock

from telegram.ext import CommandHandler
from telegram.ext import MessageHandler

from programy.clients.polling.telegram.client import TelegramBotClient
from programy.clients.polling.telegram.client import start, message, unknown
from programy.clients.polling.telegram.config import TelegramConfiguration
from programy.clients.render.text import TextRenderer
from programytest.clients.arguments import MockArgumentParser


class MockBot(object):

    def __init__(self):
        self.license_keys = {}
        self.answer = None

    def ask_question(self, userid, text, responselogger=None):
        return self.answer


class MockLicenseKeys(object):

    def __init__(self, keys=None):
        if keys is not None:
            self.keys = keys
        else:
            self.keys = {}

    def get_key(self, key):
        return self.keys[key]


class MockTelegramBot(object):

    def __init__(self):
        self._chat_id = None
        self._text = None

    def send_message(self, chat_id, text):
        self._chat_id = chat_id
        self._text = text


class MockDispatcher(object):

    def __init__(self):
        self._handlers = []

    def add_handler(self, handler):
        self._handlers.append(handler)


class MockUpdater(object):

    def __init__(self):
        self.dispatcher = MockDispatcher()
        self._ran = False
        self._stopped = False

    def start_polling(self):
        TelegramBotClient._running = False
        self._ran = True

    def stop(self):
        self._stopped = True


class MockMessage(object):

    def __init__(self, chat_id, text):
        self.chat_id = chat_id
        self.text = text


class MockUpdate(object):

    def __init__(self, message):
        self.message = message


class MockTelegramBotClient(TelegramBotClient):

    def __init__(self, argument_parser=None):
        self._response = None
        TelegramBotClient.__init__(self, argument_parser)

    def get_license_keys(self):
         self._telegram_token = "TELEGRAM_TOKEN"

    def create_updater(self, telegram_token):
        self._updater = MockUpdater()

    def ask_question(self, userid, question):
        return self._response

    def get_unknown_response(self, userid):
        return self._response

    def get_initial_question(self, update):
        return self._response


class TelegramBotClientTests(unittest.TestCase):

    def test_telegram_client_init(self):
        arguments = MockArgumentParser()
        client = MockTelegramBotClient(arguments)
        self.assertIsNotNone(client)
        self.assertIsInstance(client.get_client_configuration(), TelegramConfiguration)
        self.assertEqual(client.id, "telegram")
        self.assertEqual('ProgramY AIML2.0 Client', client.get_description())
        self.assertEqual("TELEGRAM_TOKEN", client._telegram_token)

        self.assertFalse(client._render_callback())
        self.assertIsInstance(client.renderer, TextRenderer)

    def test_register_handlers(self):
        arguments = MockArgumentParser()
        client = MockTelegramBotClient(arguments)
        self.assertIsNotNone(client)

        client.create_updater("TELEGRAM_TOKEN")

        client.register_handlers()

        self.assertEqual(3, len(client._updater.dispatcher._handlers))
        self.assertIsInstance(client._updater.dispatcher._handlers[0], CommandHandler)
        self.assertIsInstance(client._updater.dispatcher._handlers[1], MessageHandler)
        self.assertIsInstance(client._updater.dispatcher._handlers[2], MessageHandler)

    def test_start_no_client(self):
        TelegramBotClient.TELEGRAM_CLIENT = None
        mock_bot = unittest.mock.Mock()
        update = []
        with self.assertRaises(Exception):
            start(mock_bot, update)

    def test_start_with_client(self):
        arguments = MockArgumentParser()
        TelegramBotClient.TELEGRAM_CLIENT = MockTelegramBotClient(arguments)
        mock_bot = unittest.mock.Mock()
        update = []
        start(mock_bot, update)

    def test_client_start_no_initial_question(self):
        telegram_bot = MockTelegramBot()
        arguments = MockArgumentParser()
        client = MockTelegramBotClient(arguments)
        self.assertIsNotNone(client)

        client._response = None

        message = MockMessage("test123", None)
        update = MockUpdate(message)

        client.start(telegram_bot, update)

        self.assertIsNone(telegram_bot._text)

    def test_client_start(self):
        telegram_bot = MockTelegramBot()
        arguments = MockArgumentParser()
        client = MockTelegramBotClient(arguments)
        self.assertIsNotNone(client)

        client._response = "Initial Question"

        message = MockMessage("test123", None)
        update = MockUpdate(message)

        client.start(telegram_bot, update)

        self.assertEqual("test123", telegram_bot._chat_id)
        self.assertEqual("Initial Question", telegram_bot._text)

    def test_message_no_client(self):
        mock_bot = unittest.mock.Mock()
        update = []
        with self.assertRaises(Exception):
            message(mock_bot, update)

    def test_message_with_client(self):
        arguments = MockArgumentParser()
        TelegramBotClient.TELEGRAM_CLIENT = MockTelegramBotClient(arguments)
        mock_bot = unittest.mock.Mock()
        update = unittest.mock.Mock()
        update.message = unittest.mock.Mock()
        update.message.chat_id = 1
        update.message.text = "Hello"
        message(mock_bot, update)

    def test_client_message_no_response(self):
        telegram_bot = MockTelegramBot()
        arguments = MockArgumentParser()
        client = MockTelegramBotClient(arguments)
        self.assertIsNotNone(client)

        client._response = None

        message = MockMessage("test123", "Hello")
        update = MockUpdate(message)

        client.message(telegram_bot, update)

        self.assertIsNone(telegram_bot._text)

    def test_client_message(self):
        telegram_bot = MockTelegramBot()
        arguments = MockArgumentParser()
        client = MockTelegramBotClient(arguments)
        self.assertIsNotNone(client)

        client._response = "Hi there"

        message = MockMessage("test123", "Hello")
        update = MockUpdate(message)

        client.message(telegram_bot, update)

        self.assertEqual("test123", telegram_bot._chat_id)
        self.assertEqual("Hi there", telegram_bot._text)

    def test_unknown_no_client(self):
        TelegramBotClient.TELEGRAM_CLIENT = None
        mock_bot = unittest.mock.Mock()
        update = []
        with self.assertRaises(Exception):
            unknown(mock_bot, update)

    def test_unknown_with_client(self):
        arguments = MockArgumentParser()
        TelegramBotClient.TELEGRAM_CLIENT = MockTelegramBotClient(arguments)
        mock_bot = unittest.mock.Mock()
        update = unittest.mock.Mock()
        update.message = unittest.mock.Mock()
        update.message.chat_id = 1
        unknown(mock_bot, update)

    def test_client_unknown_no_response(self):
        telegram_bot = MockTelegramBot()
        arguments = MockArgumentParser()
        client = MockTelegramBotClient(arguments)
        self.assertIsNotNone(client)

        client._response = None

        message = MockMessage("test123", None)
        update = MockUpdate(message)

        client.message(telegram_bot, update)

        self.assertIsNone(telegram_bot._text)

    def test_client_unknown(self):
        telegram_bot = MockTelegramBot()
        arguments = MockArgumentParser()
        client = MockTelegramBotClient(arguments)
        self.assertIsNotNone(client)

        client._response = "Unknown Question"

        message = MockMessage("test123", None)
        update = MockUpdate(message)

        client.message(telegram_bot, update)

        self.assertEqual("test123", telegram_bot._chat_id)
        self.assertEqual("Unknown Question", telegram_bot._text)

    def test_poll_answer(self):
        telegram_bot = MockTelegramBot()
        arguments = MockArgumentParser()
        client = MockTelegramBotClient(arguments)
        self.assertIsNotNone(client)
        client.connect()

        self.assertFalse(client._updater._ran)

        client.poll_and_answer()

        self.assertTrue(client._updater._ran)
