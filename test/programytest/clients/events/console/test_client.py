import unittest

from programy.clients.events.console.client import ConsoleBotClient

from programytest.clients.arguments import MockArgumentParser


class MockConsoleBotClient(ConsoleBotClient):

    def __init__(self, argument_parser=None):
        ConsoleBotClient.__init__(self, argument_parser)
        self.answer = None
        self.question = None
        self.response = ""
        self.get_question_exception = False
        self.process_question_answer_do_nothing = False
        self.process_question_answer_keyboard_interrupt = False
        self.process_question_answer_exception = False

    def get_question(self, client_context, input_func=input):
        return self.question

    def process_question(self, client_context, input_func=input):
        if self.get_question_exception is True:
            raise Exception("Bad Thing Happen")
        else:
            return self.question

    def process_response(self, client_context, response):
        super (MockConsoleBotClient, self).process_response(client_context, response)
        self.response += response

    def process_question_answer(self, client_context):
        if self.process_question_answer_keyboard_interrupt is True:
            raise KeyboardInterrupt()
        elif self.process_question_answer_exception is True:
            raise Exception()
        elif self.process_question_answer_do_nothing is True:
            pass
        else:
            super(MockConsoleBotClient, self).process_question_answer(client_context)


def mock_input_func(ask):
    return "Hello"


class ConsoleBotClientTests(unittest.TestCase):

    def test_console_client_init(self):
        arguments = MockArgumentParser()
        client = ConsoleBotClient(arguments)
        self.assertIsNotNone(client)
        self.assertIsNotNone(client.arguments)
        self.assertEqual(client.id, "Console")
        self.assertEqual('ProgramY AIML2.0 Client', client.get_description())

    def test_get_question(self):
        arguments = MockArgumentParser()
        client = ConsoleBotClient(arguments)
        self.assertIsNotNone(client)
        context = client.create_client_context("console")
        question = client.get_question(context, input_func=mock_input_func)
        self.assertEqual("Hello", question)

    def test_process_response(self):
        arguments = MockArgumentParser()
        client = MockConsoleBotClient(arguments)
        self.assertIsNotNone(client)
        context = client.create_client_context("console")
        client.process_response(context, "Answer")
        self.assertEqual("Answer", client.response)

    def test_display_startup_messages(self):
        arguments = MockArgumentParser()
        client = MockConsoleBotClient(arguments)
        self.assertIsNotNone(client)
        client._arguments.context = False
        context = client.create_client_context("console")
        client.display_startup_messages(context)
        self.assertEqual("None, App: vNone Grammar vNone, initiated NoneHello", client.response)

    def test_process_question_answer(self):
        arguments = MockArgumentParser()
        client = MockConsoleBotClient(arguments)
        self.assertIsNotNone(client)
        client.question = "Hello"
        client.answer = "Hello"
        context = client.create_client_context("console")
        client.process_question_answer(context)
        self.assertEqual("Hello", client.response)

    def test_process_question_answer_no_response(self):
        arguments = MockArgumentParser()
        client = MockConsoleBotClient(arguments)
        self.assertIsNotNone(client)
        client.question = None
        context = client.create_client_context("console")
        client.process_question_answer(context)
        self.assertEqual('', client.response)

    def test_process_question_answer_with_context(self):
        arguments = MockArgumentParser()
        client = MockConsoleBotClient(arguments)
        client._arguments.context = True
        self.assertIsNotNone(client)
        client.question = "Hello"
        context = client.create_client_context("console")
        client.process_question_answer(context)
        self.assertEqual("Hello", client.response)

    def test_run_loop_no_loop(self):
        arguments = MockArgumentParser()
        client = MockConsoleBotClient(arguments)
        client.arguments._no_loop = True
        client.run()

