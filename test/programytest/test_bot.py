import unittest.mock

from programy.brain import Brain
from programy.bot import BrainFactory
from programy.bot import Bot
from programy.config.bot.bot import BotConfiguration
from programy.config.programy import ProgramyConfiguration
from programy.clients.events.console.config import ConsoleConfiguration
from programy.context import ClientContext

from programytest.client import TestClient


class MockBrain(Brain):

    def __init__(self, bot, configuration):
        Brain.__init__(self, bot, configuration)
        self._response = ""

    def ask_question(self, clientid, sentence, srai=False):
        return self._response


class MockBot(Bot):

    def __init__(self, config: BotConfiguration, client):
        Bot.__init__(self, config, client)

    def loads_brains(self, bot):
        self._brains["mock"] = MockBrain(self, self.configuration.configurations[0])


class BrainFactoryTests(unittest.TestCase):

    def test_empty_config_init(self):
        configuration = BotConfiguration()
        configuration._bot_selector = "programy.clients.client.DefaultBrainSelector"

        client = TestClient()
        bot = Bot(configuration, client)

        factory = BrainFactory(bot)
        self.assertIsNotNone(factory)

        brain = factory.select_brain()
        self.assertIsNotNone(brain)
        self.assertIsInstance(brain, Brain)


class BotTests(unittest.TestCase):

    def setUp(self):
        client = TestClient()
        self._client_context = client.create_client_context("testid")

    def test_bot_init_blank(self):
        
        client = TestClient()
        bot = Bot(BotConfiguration(), client)

        self.assertIsNotNone(bot.brain)

        self.assertEqual("bot", bot.ylogger_type())
        self.assertIsNone(bot.spell_checker)
        self.assertIsNotNone(bot.sentence_splitter)
        self.assertIsNotNone(bot.sentence_joiner)
        self.assertIsNotNone(bot.conversations)
        self.assertIsNotNone(bot.default_response)
        self.assertIsNotNone(bot.exit_response)
        self.assertIsNotNone(bot.initial_question)
        self.assertTrue(bot.override_properties)
        self.assertIsNotNone(bot.get_version_string)

    def test_bot_init_with_config(self):
        
        bot_config = BotConfiguration()
        bot_config._bot_root              = BotConfiguration.DEFAULT_ROOT
        bot_config._default_response      = BotConfiguration.DEFAULT_RESPONSE
        bot_config._exit_response         = BotConfiguration.DEFAULT_EXIT_RESPONSE
        bot_config._initial_question      = BotConfiguration.DEFAULT_INITIAL_QUESTION
        bot_config._empty_string          = BotConfiguration.DEFAULT_EMPTY_STRING
        bot_config._override_properties   = BotConfiguration.DEFAULT_OVERRIDE_PREDICATES
        bot_config._max_question_recursion = 1000
        bot_config._max_question_timeout   = 60
        bot_config._max_search_depth       = 100
        bot_config._max_search_timeout     = 60

        client = TestClient()
        bot = Bot(bot_config, client)

        self.assertIsNotNone(bot.brain)
        self.assertIsNone(bot.spell_checker)
        self.assertIsNotNone(bot.sentence_splitter)
        self.assertIsNotNone(bot.sentence_joiner)
        self.assertIsNotNone(bot.conversations)
        self.assertIsNotNone(bot.default_response)
        self.assertIsNotNone(bot.exit_response)
        self.assertIsNotNone(bot.initial_question)
        self.assertTrue(bot.override_properties)
        self.assertIsNotNone(bot.get_version_string)

    def test_bot_old_version(self):
        bot_config = BotConfiguration()

        client = TestClient()
        bot = Bot(bot_config, client)

        self._client_context.brain.properties.add_property("name", 'bot'),
        self._client_context.brain.properties.add_property("version", "1.9.3"),
        self._client_context.brain.properties.add_property("birthdate", "1st January 2019")

        version = bot.get_version_string(self._client_context)

        self.assertIsNotNone(version)
        self.assertEqual("bot, v1.9.3, initiated 1st January 2019", version)

    def test_bot_new_version(self):
        bot_config = BotConfiguration()

        client = TestClient()
        bot = Bot(bot_config, client)

        self._client_context.brain.properties.add_property("name", 'bot'),
        self._client_context.brain.properties.add_property("app_version", "1.9.3"),
        self._client_context.brain.properties.add_property("grammar_version", "37"),
        self._client_context.brain.properties.add_property("birthdate", "1st January 2019")

        version = bot.get_version_string(self._client_context)

        self.assertIsNotNone(version)
        self.assertEqual("bot, App: v1.9.3 Grammar v37, initiated 1st January 2019", version)

    def test_bot_init_no_spellchecker_configuration(self):
        bot_config = BotConfiguration()
        bot_config._spelling = None
        client = TestClient()
        bot = Bot(bot_config, client)

        self.assertIsNotNone(bot)
        self.assertIsNone(bot.spell_checker)

    def test_bot_init_no_spellchecker(self):
        bot_config = BotConfiguration()
        bot_config.spelling._classname = None
        client = TestClient()
        bot = Bot(bot_config, client)

        self.assertIsNotNone(bot)
        self.assertIsNone(bot.spell_checker)

    def test_bot_init_with_invalid_spellchecker(self):
        bot_config = BotConfiguration()
        bot_config.spelling._classname = "programy.spelling.checker.SpellingCheckerX"
        client = TestClient()
        bot = Bot(bot_config, client)

        self.assertIsNotNone(bot)
        self.assertIsNone(bot.spell_checker)

    def test_bot_init_with_valid_spellchecker(self):
        bot_config = BotConfiguration()
        bot_config.spelling._classname = "programy.spelling.textblob_spelling.TextBlobSpellingChecker"
        client = TestClient()
        bot = Bot(bot_config, client)

        self.assertIsNotNone(bot)
        self.assertIsNotNone(bot.spell_checker)

    def test_bot_init_no_splitter_configuration(self):
        bot_config = BotConfiguration()
        bot_config._splitter = None
        client = TestClient()
        bot = Bot(bot_config, client)

        self.assertIsNotNone(bot)
        self.assertIsNone(bot.sentence_splitter)

    def test_bot_init_no_splitterr(self):
        bot_config = BotConfiguration()
        bot_config.splitter._classname = None
        client = TestClient()
        bot = Bot(bot_config, client)

        self.assertIsNotNone(bot)
        self.assertIsNone(bot.sentence_splitter)

    def test_bot_init_with_invalid_splitterr(self):
        bot_config = BotConfiguration()
        bot_config.splitter._classname = "programy.spelling.checker.SpellingCheckerX"
        client = TestClient()
        bot = Bot(bot_config, client)

        self.assertIsNotNone(bot)
        self.assertIsNone(bot.sentence_splitter)

    def test_bot_init_with_valid_splitterr(self):
        bot_config = BotConfiguration()
        bot_config.splitter._classname = "programy.dialog.splitter.splitter.SentenceSplitter"
        client = TestClient()
        bot = Bot(bot_config, client)

        self.assertIsNotNone(bot)
        self.assertIsNotNone(bot.sentence_splitter)

    def test_bot_init_no_joiner_configuration(self):
        bot_config = BotConfiguration()
        bot_config._joiner = None
        client = TestClient()
        bot = Bot(bot_config, client)

        self.assertIsNotNone(bot)
        self.assertIsNone(bot.sentence_joiner)

    def test_bot_init_no_joinerr(self):
        bot_config = BotConfiguration()
        bot_config.joiner._classname = None
        client = TestClient()
        bot = Bot(bot_config, client)

        self.assertIsNotNone(bot)
        self.assertIsNone(bot.sentence_joiner)

    def test_bot_init_with_invalid_joinerr(self):
        bot_config = BotConfiguration()
        bot_config.joiner._classname = "programy.spelling.checker.SpellingCheckerX"
        client = TestClient()
        bot = Bot(bot_config, client)

        self.assertIsNotNone(bot)
        self.assertIsNone(bot.sentence_joiner)

    def test_bot_init_with_valid_joinerr(self):
        bot_config = BotConfiguration()
        bot_config.joiner._classname = "programy.dialog.joiner.joiner.SentenceJoiner"
        client = TestClient()
        bot = Bot(bot_config, client)

        self.assertIsNotNone(bot)
        self.assertIsNotNone(bot.sentence_joiner)

    def test_bot_init_no_translator_configuration(self):
        bot_config = BotConfiguration()
        bot_config._from_translator = None
        bot_config._to_translator = None
        client = TestClient()
        bot = Bot(bot_config, client)

        self.assertIsNotNone(bot)
        self.assertIsNone(bot.from_translator)
        self.assertIsNone(bot.to_translator)

    def test_bot_init_no_translatorr(self):
        bot_config = BotConfiguration()
        bot_config.from_translator._classname = None
        bot_config.to_translator._classname = None
        client = TestClient()
        bot = Bot(bot_config, client)

        self.assertIsNotNone(bot)
        self.assertIsNone(bot.from_translator)
        self.assertIsNone(bot.to_translator)

    def test_bot_init_with_invalid_translatorr(self):
        bot_config = BotConfiguration()
        bot_config.from_translator._classname = "programy.spelling.checker.SpellingCheckerX"
        bot_config.to_translator._classname = "programy.spelling.checker.SpellingCheckerX"
        client = TestClient()
        bot = Bot(bot_config, client)

        self.assertIsNotNone(bot)
        self.assertIsNone(bot.from_translator)
        self.assertIsNone(bot.to_translator)

    def test_bot_init_with_valid_translatorr(self):
        bot_config = BotConfiguration()
        bot_config.from_translator._classname = "programy.nlp.translate.textblob_translator.TextBlobTranslator"
        bot_config.to_translator._classname = "programy.nlp.translate.textblob_translator.TextBlobTranslator"
        client = TestClient()
        bot = Bot(bot_config, client)

        self.assertIsNotNone(bot)
        self.assertIsNotNone(bot.from_translator)
        self.assertIsNotNone(bot.to_translator)

    def test_bot_init_no_sentiment_analyser_configuration(self):
        bot_config = BotConfiguration()
        bot_config._sentiment = None
        client = TestClient()
        bot = Bot(bot_config, client)

        self.assertIsNotNone(bot)
        self.assertIsNone(bot.sentiment_analyser)

    def test_bot_init_no_sentiment_analyserr(self):
        bot_config = BotConfiguration()
        bot_config.sentiment_analyser._classname = None
        client = TestClient()
        bot = Bot(bot_config, client)

        self.assertIsNotNone(bot)
        self.assertIsNone(bot.sentiment_analyser)

    def test_bot_init_with_invalid_sentiment_analyserr(self):
        bot_config = BotConfiguration()
        bot_config.sentiment_analyser._classname = "programy.spelling.checker.SpellingCheckerX"
        client = TestClient()
        bot = Bot(bot_config, client)

        self.assertIsNotNone(bot)
        self.assertIsNone(bot.sentiment_analyser)

    def test_bot_init_with_valid_sentiment_analyserr(self):
        bot_config = BotConfiguration()
        bot_config.sentiment_analyser._classname = "programy.nlp.sentiment.textblob_sentiment.TextBlobSentimentAnalyser"
        client = TestClient()
        bot = Bot(bot_config, client)

        self.assertIsNotNone(bot)
        self.assertIsNotNone(bot.sentiment_analyser)

    def test_bot_init_default_brain(self):
        client = TestClient()
        bot = Bot(BotConfiguration(), client)
        self.assertIsNotNone(bot)
        self.assertIsNotNone(bot.brain)

    def test_bot_init_supplied_brain(self):
        client = TestClient()
        bot = Bot(BotConfiguration(), client)
        self.assertIsNotNone(bot)
        self.assertIsNotNone(bot.brain)

    def test_bot_defaultresponses(self):
        client = TestClient()
        bot = Bot(BotConfiguration(), client)
        self.assertIsNotNone(bot)

        self.assertEqual(bot.default_response, "")
        self.assertEqual(bot.exit_response, "Bye!")

    def test_bot_with_config(self):
        configuration = ProgramyConfiguration(ConsoleConfiguration())
        self.assertIsNotNone(configuration)
        self.assertIsNotNone(configuration.client_configuration.configurations[0])
        self.assertIsNotNone(configuration.client_configuration.configurations[0].configurations[0])

        configuration.client_configuration.configurations[0].prompt = ":"
        configuration.client_configuration.configurations[0].default_response = "No answer for that"
        configuration.client_configuration.configurations[0].exit_response = "See ya!"

        client = TestClient()
        bot = Bot(configuration.client_configuration.configurations[0], client)
        self.assertIsNotNone(bot)

        self.assertEqual(bot.default_response, "No answer for that")
        self.assertEqual(bot.exit_response, "See ya!")

    def test_bot_with_conversation(self):
        client = TestClient()
        bot = Bot(BotConfiguration(), client)
        self.assertIsNotNone(bot)

        self.assertFalse(bot.has_conversation(self._client_context))

        response = bot.ask_question(self._client_context, "hello")
        self.assertIsNotNone(response)
        self.assertTrue(bot.has_conversation(self._client_context))

        response = bot.ask_question(self._client_context, "hello")
        self.assertIsNotNone(response)
        self.assertTrue(bot.has_conversation(self._client_context))

        client_context2 = ClientContext(TestClient(), "testid2")
        client_context2._bot = bot
        client_context2._brain = self._client_context.bot.brain

        response = bot.ask_question(client_context2, "hello")
        self.assertIsNotNone(response)
        self.assertTrue(bot.has_conversation(client_context2))

    def test_bot_chat_loop(self):

        client = TestClient()
        bot = Bot(BotConfiguration(), client)
        self.assertIsNotNone(bot)
        self.assertIsInstance(bot, Bot)
        bot.configuration._default_response = "Sorry, I don't have an answer for that right now"

        response = bot.ask_question(self._client_context, "hello")
        self.assertIsNotNone(response)
        self.assertEqual(response, "Sorry, I don't have an answer for that right now.")

        response = bot.ask_question(self._client_context, "hello again")
        self.assertIsNotNone(response)
        self.assertEqual(response, "Sorry, I don't have an answer for that right now.")

        response = bot.ask_question(self._client_context, "goodbye")
        self.assertIsNotNone(response)
        self.assertEqual(response, "Sorry, I don't have an answer for that right now.")

        conversation = bot.get_conversation(self._client_context)
        self.assertIsNotNone(conversation)

        self.assertEqual(conversation.previous_nth_question(2).sentence(0).text(self._client_context), "hello")
        self.assertEqual(conversation.previous_nth_question(2).sentence(0).response, "Sorry, I don't have an answer for that right now")

        self.assertEqual(conversation.previous_nth_question(1).sentence(0).text(self._client_context), "hello again")
        self.assertEqual(conversation.previous_nth_question(1).sentence(0).response, "Sorry, I don't have an answer for that right now")

        self.assertEqual(conversation.previous_nth_question(0).sentence(0).text(self._client_context), "goodbye")
        self.assertEqual(conversation.previous_nth_question(0).sentence(0).response, "Sorry, I don't have an answer for that right now")

    def test_max_recusion(self):

        client = TestClient()
        bot = Bot(BotConfiguration(), client)
        self.assertIsNotNone(bot)
        bot.configuration._default_response = "Sorry, I don't have an answer for that right now"
        bot.configuration._max_question_recursion = 0

        with self.assertRaises(Exception):
            bot.ask_question(self._client_context, "hello")

    def test_get_default_response_empty_string(self):

        bot_config = BotConfiguration()
        self.assertIsNotNone(bot_config)

        client = TestClient()
        bot = Bot(bot_config, client)
        self.assertIsNotNone(bot)

        self.assertEqual("", bot.get_default_response(self._client_context))

    def test_get_default_response_default_response_only(self):

        bot_config = BotConfiguration()
        self.assertIsNotNone(bot_config)

        bot_config.default_response = "Default response!"

        client = TestClient()
        bot = Bot(bot_config, client)
        self.assertIsNotNone(bot)

        self.assertEqual("Default response!", bot.get_default_response(self._client_context))

    def test_get_default_response_default_response_srai_no_match(self):

        bot_config = BotConfiguration()
        self.assertIsNotNone(bot_config)

        bot_config.default_response_srai = "YDEFAULTRESPONSE"
        bot_config.default_response = "Default response!"

        client = TestClient()
        bot = Bot(bot_config, client)
        self.assertIsNotNone(bot)

        self.assertEqual("Default response!", bot.get_default_response(self._client_context))

    def test_get_default_response_default_response_srai_match(self):

        bot_config = BotConfiguration()
        self.assertIsNotNone(bot_config)

        bot_config.default_response_srai = "YDEFAULTRESPONSE"
        bot_config.default_response = "Default response!"

        client = TestClient()
        bot = MockBot(bot_config, client)
        self.assertIsNotNone(bot)

        client_context2 = ClientContext(TestClient(), "testid2")
        client_context2._bot = bot
        client_context2._brain = MockBrain(bot, bot.configuration.configurations[0])
        client_context2._brain._response = "Y DEFAULT RESPONSE"

        response = bot.get_default_response(client_context2)
        self.assertIsNotNone(response)
        self.assertEqual("Y DEFAULT RESPONSE", response)

    def test_get_default_response_no_srai(self):

        bot_config = BotConfiguration()
        bot_config._default_response_srai = None
        bot_config._default_response = "Test This"
        self.assertIsNotNone(bot_config)

        client = TestClient()
        bot = Bot(bot_config, client)
        self.assertIsNotNone(bot)

        self.assertEqual("Test This", bot.get_default_response(self._client_context))

    def test_get_initial_question_empty_string(self):

        bot_config = BotConfiguration()
        self.assertIsNotNone(bot_config)

        client = TestClient()
        bot = Bot(bot_config, client)
        self.assertIsNotNone(bot)

        self.assertEqual("Hello", bot.get_initial_question(self._client_context))

    def test_get_initial_question_initial_question_only(self):

        bot_config = BotConfiguration()
        self.assertIsNotNone(bot_config)

        bot_config.initial_question = "Default response!"

        client = TestClient()
        bot = Bot(bot_config, client)
        self.assertIsNotNone(bot)

        self.assertEqual("Default response!", bot.get_initial_question(self._client_context))

    def test_get_initial_question_initial_question_srai_no_match(self):

        bot_config = BotConfiguration()
        self.assertIsNotNone(bot_config)

        bot_config.initial_question_srai = "YDEFAULTRESPONSE"
        bot_config.initial_question = "Default response!"

        client = TestClient()
        bot = Bot(bot_config, client)
        self.assertIsNotNone(bot)

        self.assertEqual("Default response!", bot.get_initial_question(self._client_context))

    def test_get_initial_question_initial_question_srai_match(self):

        bot_config = BotConfiguration()
        self.assertIsNotNone(bot_config)

        client = TestClient()
        bot = MockBot(bot_config, client)
        self.assertIsNotNone(bot)

        client_context2 = ClientContext(TestClient(), "testid2")
        client_context2._bot = bot
        client_context2._brain = MockBrain(bot, bot.configuration.configurations[0])
        client_context2._brain._response = "Y DEFAULT RESPONSE"

        self.assertEqual("Y DEFAULT RESPONSE", bot.get_initial_question(client_context2))

    def test_get_initial_question_no_srai(self):

        bot_config = BotConfiguration()
        bot_config._initial_question = "Test This"
        bot_config._initial_question_srai = None

        self.assertIsNotNone(bot_config)

        client = TestClient()
        bot = Bot(bot_config, client)
        self.assertIsNotNone(bot)

        self.assertEqual("Test This", bot.get_initial_question(self._client_context))

    def test_get_exit_response_empty_string(self):

        bot_config = BotConfiguration()
        self.assertIsNotNone(bot_config)

        client = TestClient()
        bot = Bot(bot_config, client)
        self.assertIsNotNone(bot)

        self.assertEqual("Bye!", bot.get_exit_response(self._client_context))

    def test_get_exit_response_exit_response_only(self):

        bot_config = BotConfiguration()
        self.assertIsNotNone(bot_config)

        bot_config.exit_response = "Default response!"

        client = TestClient()
        bot = Bot(bot_config, client)
        self.assertIsNotNone(bot)

        self.assertEqual("Default response!", bot.get_exit_response(self._client_context))

    def test_get_exit_response_exit_response_srai_no_match(self):

        bot_config = BotConfiguration()
        self.assertIsNotNone(bot_config)

        bot_config.exit_response_srai = "YDEFAULTRESPONSE"
        bot_config.exit_response = "Default response!"

        client = TestClient()
        bot = Bot(bot_config, client)
        self.assertIsNotNone(bot)

        self.assertEqual("Default response!", bot.get_exit_response(self._client_context))

    def test_get_exit_response_exit_response_srai_match(self):

        bot_config = BotConfiguration()
        self.assertIsNotNone(bot_config)
        bot_config.exit_response_srai = "YDEFAULTRESPONSE"
        bot_config.exit_response = "Default response!"

        client = TestClient()
        bot = MockBot(bot_config, client)
        self.assertIsNotNone(bot)

        client_context2 = ClientContext(TestClient(), "testid2")
        client_context2._bot = bot
        client_context2._brain = MockBrain(bot, bot.configuration.configurations[0])
        client_context2._brain._response = "Y DEFAULT RESPONSE"

        self.assertEqual("Y DEFAULT RESPONSE", bot.get_exit_response(client_context2))

    def test_get_exit_response_no_srai(self):

        bot_config = BotConfiguration()
        bot_config._exit_response = "Test This"
        bot_config._exit_response_srai = None
        self.assertIsNotNone(bot_config)

        client = TestClient()
        bot = Bot(bot_config, client)
        self.assertIsNotNone(bot)

        self.assertEqual("Test This", bot.get_exit_response(self._client_context))

    def test_log_answer(self):
        bot_config = BotConfiguration()
        client = TestClient()
        bot = Bot(bot_config, client)

        bot.log_answer(self._client_context, "Hello", "Test", None)

        response_logger = unittest.mock.Mock()

        bot.log_answer(self._client_context, "Hello", "Test", response_logger)
