import unittest
import time

from programy.context import ClientContext


class MockClient:

    def __init__(self, id):
        self._id = id

    @property
    def id(self):
        return self._id


class MockBotConfiguration:

    def __init__(self, max_question_recursion, max_question_timeout):
        self._max_question_recursion = max_question_recursion
        self._max_question_timeout = max_question_timeout

    @property
    def max_question_recursion(self):
        return self._max_question_recursion

    @property
    def max_question_timeout(self):
        return self._max_question_timeout


class MockBot:

    def __init__(self, id, config):
        self._id = id
        self._config = config

    @property
    def id(self):
        return self._id

    @property
    def configuration(self):
        return self._config


class MockBrain:

    def __init__(self, id):
        self._id = id

    @property
    def id(self):
        return self._id


class ClientContextTests(unittest.TestCase):

    def test_base_init(self):
        client = MockClient("clientid")
        context = ClientContext(client, "testid")
        self.assertEqual("[clientid] [testid] [] [] [0]", str(context))

    def test_init_with_bot(self):
        client = MockClient("clientid")
        bot = MockBot("botid", None)
        context = ClientContext(client, "testid")
        context.bot = bot
        self.assertEqual("[clientid] [testid] [botid] [] [0]", str(context))

    def test_init_with_bot_brain(self):
        client = MockClient("clientid")
        bot = MockBot("botid", None)
        brain = MockBrain("brainid")
        context = ClientContext(client, "testid")
        context.bot = bot
        context.brain = brain
        self.assertEqual("[clientid] [testid] [botid] [brainid] [0]", str(context))

    def test_question(self):
        client = MockClient("clientid")
        bot = MockBot("botid", None)
        brain = MockBrain("brainid")
        context = ClientContext(client, "testid")
        context.bot = bot
        context.brain = brain
        self.assertEqual("[clientid] [testid] [botid] [brainid] [0]", str(context))

        context.mark_question_start("question")

        self.assertEqual("[clientid] [testid] [botid] [brainid] [1]", str(context))

        context.mark_question_start("question")

        self.assertEqual("[clientid] [testid] [botid] [brainid] [2]", str(context))

        context.reset_question()

        self.assertEqual("[clientid] [testid] [botid] [brainid] [0]", str(context))

    def test_max_recursion(self):
        client = MockClient("clientid")
        bot_config = MockBotConfiguration(1, 1)
        bot = MockBot("botid", bot_config)
        brain = MockBrain("brainid")
        context = ClientContext(client, "testid")
        context.bot = bot
        context.brain = brain
        self.assertEqual("[clientid] [testid] [botid] [brainid] [0]", str(context))

        context.mark_question_start("question1")

        context.check_max_recursion()

        context.mark_question_start("question2")

        with self.assertRaises(Exception):
            context.check_max_recursion()

    def test_check_max_timeout(self):
        client = MockClient("clientid")
        bot_config = MockBotConfiguration(999, 1)
        bot = MockBot("botid", bot_config)
        brain = MockBrain("brainid")
        context = ClientContext(client, "testid")
        context.bot = bot
        context.brain = brain
        self.assertEqual("[clientid] [testid] [botid] [brainid] [0]", str(context))

        context.mark_question_start("question1")

        context.check_max_timeout()

        time.sleep(1)

        context.mark_question_start("question2")

        with self.assertRaises(Exception):
            context.check_max_timeout()
