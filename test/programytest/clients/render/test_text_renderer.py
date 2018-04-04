import unittest
import unittest.mock

from programy.clients.render.text_renderer import TextRenderer

class MockConsoleBotClient(object):

    def __init__(self):
        self._response = None

    def display_response(self, response, output_func=print):
        self._response = response

class TextRendererTests(unittest.TestCase):

    def test_text_only(self):
        mock_config = unittest.mock.Mock()
        mock_console = MockConsoleBotClient()
        renderer = TextRenderer(mock_config, mock_console)
        self.assertIsNotNone(renderer)

        renderer.send_message("testuser", "Hello world")

        self.assertEquals(mock_console._response, "Hello world")

    def test_url_button(self):
        mock_config = unittest.mock.Mock()
        mock_console = MockConsoleBotClient()
        renderer = TextRenderer(mock_config, mock_console)
        self.assertIsNotNone(renderer)

        renderer.send_message("testuser", "<button><text>Hello</text><url>http://click.me</url></button>")

        self.assertEquals(mock_console._response, "Hello, click http://click.me")

    def test_postback_button(self):
        mock_config = unittest.mock.Mock()
        mock_console = MockConsoleBotClient()
        renderer = TextRenderer(mock_config, mock_console)
        self.assertIsNotNone(renderer)

        renderer.send_message("testuser", "<button><text>Hello</text><postback>HELLO</postback></button>")

        self.assertEquals(mock_console._response, "HELLO")

    def test_link(self):
        mock_config = unittest.mock.Mock()
        mock_console = MockConsoleBotClient()
        renderer = TextRenderer(mock_config, mock_console)
        self.assertIsNotNone(renderer)

        renderer.send_message("testuser", "<link><text>Hello</text><url>http://click.me</url></link>")

        self.assertEquals(mock_console._response, "Open in browser, click http://click.me")

    def test_image(self):
        mock_config = unittest.mock.Mock()
        mock_console = MockConsoleBotClient()
        renderer = TextRenderer(mock_config, mock_console)
        self.assertIsNotNone(renderer)

        renderer.send_message("testuser", "<image>http://servusai.com/aiml.png</image>")

        self.assertEquals(mock_console._response, "To see the image, click http://servusai.com/aiml.png")

    def test_video(self):
        mock_config = unittest.mock.Mock()
        mock_console = MockConsoleBotClient()
        renderer = TextRenderer(mock_config, mock_console)
        self.assertIsNotNone(renderer)

        renderer.send_message("testuser", "<video>http://servusai.com/aiml.mov</video>")

        self.assertEquals(mock_console._response, "To see the video, click http://servusai.com/aiml.mov")

    def test_card(self):
        mock_config = unittest.mock.Mock()
        mock_console = MockConsoleBotClient()
        renderer = TextRenderer(mock_config, mock_console)
        self.assertIsNotNone(renderer)

        renderer.send_message("testuser", "<card><image>http://servusai.com/aiml.png</image><title>Servusai</title><subtitle>Home of ProgramY</subtitle><button><text>Hello</text><url>http://click.me</url></button></card>")

        self.assertEquals(mock_console._response, """Image: http://servusai.com/aiml.png
Title: Servusai
Subtitle: Home of ProgramY
---------------------------------------
Hello : http://click.me
---------------------------------------
""")

    def test_carousel(self):
        mock_config = unittest.mock.Mock()
        mock_console = MockConsoleBotClient()
        renderer = TextRenderer(mock_config, mock_console)
        self.assertIsNotNone(renderer)

        renderer.send_message("testuser", "<carousel><card><image>http://servusai.com/aiml.png</image><title>Servusai</title><subtitle>Home of ProgramY</subtitle><button><text>Hello</text><url>http://click.me</url></button></card></carousel>")

        self.assertEquals(mock_console._response, """=========================================
Image: http://servusai.com/aiml.png
Title: Servusai
Subtitle: Home of ProgramY
---------------------------------------
Hello : http://click.me
---------------------------------------
=========================================
""")

    def test_reply_with_postback(self):
        mock_config = unittest.mock.Mock()
        mock_console = MockConsoleBotClient()
        renderer = TextRenderer(mock_config, mock_console)
        self.assertIsNotNone(renderer)

        renderer.send_message("testuser", "<reply><text>Hello</text><postback>HELLO</postback></reply>")

        self.assertEquals(mock_console._response, "HELLO")

    def test_reply_without_postback(self):
        mock_config = unittest.mock.Mock()
        mock_console = MockConsoleBotClient()
        renderer = TextRenderer(mock_config, mock_console)
        self.assertIsNotNone(renderer)

        renderer.send_message("testuser", "<reply><text>Hello</text></reply>")

        self.assertEquals(mock_console._response, "Hello")

    def test_delay(self):
        mock_config = unittest.mock.Mock()
        mock_console = MockConsoleBotClient()
        renderer = TextRenderer(mock_config, mock_console)
        self.assertIsNotNone(renderer)

        renderer.send_message("testuser", "<delay><seconds>0</seconds></delay>")

        self.assertEquals(mock_console._response, "...")

    def test_split(self):
        mock_config = unittest.mock.Mock()
        mock_console = MockConsoleBotClient()
        renderer = TextRenderer(mock_config, mock_console)
        self.assertIsNotNone(renderer)

        renderer.send_message("testuser", "<split />")

        self.assertIsNone(mock_console._response)

    def test_list(self):
        mock_config = unittest.mock.Mock()
        mock_console = MockConsoleBotClient()
        renderer = TextRenderer(mock_config, mock_console)
        self.assertIsNotNone(renderer)

        renderer.send_message("testuser", "<list><item>Item1</item><item>Item2</item></list>")

        self.assertEquals(mock_console._response, "> Item1\n> Item2\n")

    def test_olist(self):
        mock_config = unittest.mock.Mock()
        mock_console = MockConsoleBotClient()
        renderer = TextRenderer(mock_config, mock_console)
        self.assertIsNotNone(renderer)

        renderer.send_message("testuser", "<olist><item>Item1</item><item>Item2</item></olist>")

        self.assertEquals(mock_console._response, "1. Item1\n2. Item2\n")

    def test_location(self):
        mock_config = unittest.mock.Mock()
        mock_console = MockConsoleBotClient()
        renderer = TextRenderer(mock_config, mock_console)
        self.assertIsNotNone(renderer)

        renderer.send_message("testuser", "<location />")

        self.assertEquals(mock_console._response, "")

