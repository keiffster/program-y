import unittest
import unittest.mock

from programy.clients.render.passthrough import PassThroughRenderer


class MockConsoleBotClient(object):

    def __init__(self):
        self._response = None

    def process_response(self, client_context, response):
        self._response = response


class PassThroughRendererTests(unittest.TestCase):

    def test_text_only(self):
        mock_console = MockConsoleBotClient()
        renderer = PassThroughRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", "Hello world")

        self.assertEqual(mock_console._response, "Hello world")
