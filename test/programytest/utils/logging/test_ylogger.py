import logging
import unittest

from programy.bot import Bot
from programy.brain import Brain
from programy.config.bot.bot import BotConfiguration
from programy.config.brain.brain import BrainConfiguration
from programy.context import ClientContext
from programy.utils.console.console import outputLog
from programy.utils.logging.ylogger import YLogger
from programytest.client import TestClient


class YLoggerTests(unittest.TestCase):

    def test_ylogger_initialise(self):
        client_context = ClientContext(TestClient(), "testid")
        YLogger.reset_snapshot()

        snapshot = YLogger.snapshot()

        self.assertIsNotNone(snapshot)
        self.assertEqual(str(snapshot), "Critical(0) Fatal(0) Error(0) Exception(0) Warning(0) Info(0), Debug(0)")

    def test_ylogger_critical(self):
        client_context = ClientContext(TestClient(), "testid")
        YLogger.reset_snapshot()

        YLogger.critical(client_context, "Test Message")
        snapshot = YLogger.snapshot()
        self.assertIsNotNone(snapshot)
        self.assertEqual(str(snapshot), "Critical(1) Fatal(0) Error(0) Exception(0) Warning(0) Info(0), Debug(0)")

    def test_ylogger_fatal(self):
        client_context = ClientContext(TestClient(), "testid")
        YLogger.reset_snapshot()

        YLogger.fatal(client_context, "Test Message")
        snapshot = YLogger.snapshot()
        self.assertIsNotNone(snapshot)
        self.assertEqual(str(snapshot), "Critical(0) Fatal(1) Error(0) Exception(0) Warning(0) Info(0), Debug(0)")

    def test_ylogger_error(self):
        client_context = ClientContext(TestClient(), "testid")
        YLogger.reset_snapshot()

        YLogger.error(client_context, "Test Message")
        snapshot = YLogger.snapshot()
        self.assertIsNotNone(snapshot)
        self.assertEqual(str(snapshot), "Critical(0) Fatal(0) Error(1) Exception(0) Warning(0) Info(0), Debug(0)")

    def test_ylogger_exception(self):
        client_context = ClientContext(TestClient(), "testid")
        YLogger.reset_snapshot()

        YLogger.exception(client_context, "Test Message", Exception("Test error"))
        snapshot = YLogger.snapshot()
        self.assertIsNotNone(snapshot)
        self.assertEqual(str(snapshot), "Critical(0) Fatal(0) Error(0) Exception(1) Warning(0) Info(0), Debug(0)")

    def test_ylogger_exception_nostack(self):
        client_context = ClientContext(TestClient(), "testid")
        YLogger.reset_snapshot()

        YLogger.exception_nostack(client_context, "Test Message", Exception("Test error"))
        snapshot = YLogger.snapshot()
        self.assertIsNotNone(snapshot)
        self.assertEqual(str(snapshot), "Critical(0) Fatal(0) Error(0) Exception(1) Warning(0) Info(0), Debug(0)")

    def test_ylogger_warning(self):
        client_context = ClientContext(TestClient(), "testid")
        YLogger.reset_snapshot()

        YLogger.warning(client_context, "Test Message")
        snapshot = YLogger.snapshot()
        self.assertIsNotNone(snapshot)
        self.assertEqual(str(snapshot), "Critical(0) Fatal(0) Error(0) Exception(0) Warning(1) Info(0), Debug(0)")

    def test_ylogger_info(self):
        client_context = ClientContext(TestClient(), "testid")
        YLogger.reset_snapshot()

        YLogger.info(client_context, "Test Message")
        snapshot = YLogger.snapshot()
        self.assertIsNotNone(snapshot)
        self.assertEqual(str(snapshot), "Critical(0) Fatal(0) Error(0) Exception(0) Warning(0) Info(1), Debug(0)")

    def test_ylogger_debug(self):
        client_context = ClientContext(TestClient(), "testid")
        YLogger.reset_snapshot()

        YLogger.debug(client_context, "Test Message")
        snapshot = YLogger.snapshot()
        self.assertIsNotNone(snapshot)
        self.assertEqual(str(snapshot), "Critical(0) Fatal(0) Error(0) Exception(0) Warning(0) Info(0), Debug(1)")

    def test_format_message_with_client(self):
        client = TestClient()

        msg = YLogger.format_message(client, "Test Message")
        self.assertIsNotNone(msg)
        self.assertEqual("[testclient] - Test Message", msg)

    def test_format_message_with_client_and_bot(self):
        client = TestClient()

        config = BotConfiguration()
        config._section_name = "testbot"
        bot = Bot(config, client)

        msg = YLogger.format_message(bot, "Test Message")
        self.assertIsNotNone(msg)
        self.assertEqual("[testclient] [testbot] - Test Message", msg)

    def test_format_message_with_bot(self):
        config = BotConfiguration()
        config._section_name = "testbot"
        client = TestClient()
        bot = Bot(config, client)

        msg = YLogger.format_message(bot, "Test Message")
        self.assertIsNotNone(msg)
        self.assertEqual("[testclient] [testbot] - Test Message", msg)

    def test_format_message_with_client_and_bot_and_brain(self):
        client = TestClient()

        bot_config = BotConfiguration()
        bot_config._section_name = "testbot"
        bot = Bot(bot_config, client)

        brain_config = BrainConfiguration()
        brain_config._section_name = "testbrain"
        brain = Brain(bot, brain_config)

        msg = YLogger.format_message(brain, "Test Message")
        self.assertIsNotNone(msg)
        self.assertEqual("[testclient] [testbot] [testbrain] - Test Message", msg)

    def test_format_message_with_client_and_bot_and_brain(self):
        brain_config = BrainConfiguration()
        client = TestClient()
        context = client.create_client_context("testid")

        brain_config._section_name = "testbrain"
        brain = Brain(context.bot, brain_config)

        msg = YLogger.format_message(brain, "Test Message")
        self.assertIsNotNone(msg)
        self.assertEqual("[testclient] [bot] [testbrain] - Test Message", msg)

    def test_format_message_with_client_context(self):

        client = TestClient()

        bot_config = BotConfiguration()
        bot_config._section_name = "testbot"
        bot = Bot(bot_config, client)

        brain_config = BrainConfiguration()
        brain_config._section_name = "testbrain"
        brain = Brain(bot, brain_config)

        client_context = ClientContext(client, "testuser")
        client_context._bot = bot
        client_context._brain = brain

        msg = YLogger.format_message(client_context, "Test Message")
        self.assertIsNotNone(msg)
        self.assertEqual("[testclient] [testbot] [testbrain] [testuser] - Test Message", msg)

    def test_is_ylogger_method(self):
        self.assertFalse(YLogger.is_ylogger_method(print))
        self.assertFalse(YLogger.is_ylogger_method(outputLog))
        self.assertTrue(YLogger.is_ylogger_method(YLogger.debug))
