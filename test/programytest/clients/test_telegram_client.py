import unittest
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler

from programy.clients.telegram_client import TelegramBotClient
from programy.config.sections.client.telegram_client import TelegramConfiguration

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
        self._ran = False
        self._stopped = False

    def start_polling(self):
        TelegramBotClient._running = False
        self._ran = True

    def stop(self):
        self._stopped = True


class TelegramBotClientTests(unittest.TestCase):

    def test_telegram_bot_client_init(self):
        arguments = MockArgumentParser()
        bot_client = TelegramBotClient(arguments)
        self.assertIsNotNone(bot_client)
        self.assertEquals(bot_client.clientid, "telegram")
        self.assertIsInstance(bot_client.get_client_configuration(), TelegramConfiguration)

    def test_get_token(self):
        mock_keys = MockLicenseKeys({"TELEGRAM_TOKEN": "TEST123"})
        self.assertEquals("TEST123", TelegramBotClient.get_token(mock_keys))

    def test_register_handlers(self):
        dispatcher = MockDispatcher()
        TelegramBotClient.register_handlers(dispatcher)
        self.assertEquals(3, len(dispatcher._handlers))
        self.assertIsInstance(dispatcher._handlers[0], CommandHandler)
        self.assertIsInstance(dispatcher._handlers[1], MessageHandler)
        self.assertIsInstance(dispatcher._handlers[2], MessageHandler)

    def test_poll_and_process(self):
        updater = MockUpdater()
        TelegramBotClient.poll_and_process(updater)
        self.assertTrue(updater._ran)

