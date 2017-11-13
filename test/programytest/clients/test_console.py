import unittest

from programy.clients.console import ConsoleBotClient

from programytest.clients.arguments import MockArgumentParser

class MockConsoleBotClient(ConsoleBotClient):

    def __init__(self, argument_parser=None):
        ConsoleBotClient.__init__(self, argument_parser)
        self.question = None
        self.response = ""
        self.get_question_exception = False
        self.process_question_answer_do_nothing = False
        self.process_question_answer_keyboard_interrupt = False
        self.process_question_answer_exception = False

    def get_question(self, input_func=input):
        if self.get_question_exception is True:
            raise Exception("Bad Thing Happen")
        else:
            return self.question

    def display_response(self, response, output_func=print):
        super (MockConsoleBotClient, self).display_response(response, output_func)
        self.response += response

    def ask_question(self, question):
        return self.question

    def process_question_answer(self):
        if self.process_question_answer_keyboard_interrupt is True:
            self.running = False
            raise KeyboardInterrupt()
        elif self.process_question_answer_exception is True:
            self.running = False
            raise Exception()
        elif self.process_question_answer_do_nothing is True:
            self.running = False
            return "question"
        else:
            return super(MockConsoleBotClient, self).process_question_answer()

def mock_input_func(ask):
    return "Hello"

class ConsoleBotClientTests(unittest.TestCase):

    def test_console_client_init(self):
        arguments = MockArgumentParser()
        client = ConsoleBotClient(arguments)
        self.assertIsNotNone(client)
        self.assertIsNotNone(client.arguments)
        self.assertEqual(client.clientid, "Console")

    def test_get_question(self):
        arguments = MockArgumentParser()
        client = ConsoleBotClient(arguments)
        self.assertIsNotNone(client)
        question = client.get_question(input_func=mock_input_func)
        self.assertEquals("Hello", question)

    def test_display_response(self):
        arguments = MockArgumentParser()
        client = MockConsoleBotClient(arguments)
        self.assertIsNotNone(client)
        client.display_response("Answer")
        self.assertEquals("Answer", client.response)

    def test_display_startup_messages(self):
        arguments = MockArgumentParser()
        client = MockConsoleBotClient(arguments)
        self.assertIsNotNone(client)
        client._arguments.context = False
        client.display_startup_messages()
        self.assertEquals("None, App: vNone Grammar vNone, initiated NoneHello", client.response)

    def test_process_question_answer(self):
        arguments = MockArgumentParser()
        client = MockConsoleBotClient(arguments)
        self.assertIsNotNone(client)
        client.question = "Hello"
        question = client.process_question_answer()
        self.assertEquals("Hello", question)

    def test_process_question_answer_no_response(self):
        arguments = MockArgumentParser()
        client = MockConsoleBotClient(arguments)
        self.assertIsNotNone(client)
        client.question = None
        question = client.process_question_answer()
        self.assertEquals(None, question)

    def test_process_question_answer_with_context(self):
        arguments = MockArgumentParser()
        client = MockConsoleBotClient(arguments)
        client._arguments.context = True
        self.assertIsNotNone(client)
        client.question = "Hello"
        question = client.process_question_answer()
        self.assertEquals("Hello", question)

    def test_run_loop_no_loop(self):
        arguments = MockArgumentParser()
        client = MockConsoleBotClient(arguments)
        client.arguments._no_loop = True
        client.run()

    def test_run_loop(self):
        arguments = MockArgumentParser()
        client = MockConsoleBotClient(arguments)
        client.arguments._no_loop = False
        client.process_question_answer_do_nothing = True
        client.run()

    def test_run_loop_keyboard_interrupt(self):
        arguments = MockArgumentParser()
        client = MockConsoleBotClient(arguments)
        client.arguments._no_loop = False
        client.process_question_answer_keyboard_interrupt = True
        client.run()

    def test_run_loop_general_exception(self):
        arguments = MockArgumentParser()
        client = MockConsoleBotClient(arguments)
        client.arguments._no_loop = False
        client.process_question_answer_exception = True
        client.run()