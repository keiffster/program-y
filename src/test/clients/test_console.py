import unittest

from programy.clients.console import ConsoleBotClient

def mock_input(question):
    return question

class ConsoleBotClientTests(unittest.TestCase):

    def test_console_client(self):
        pass