import unittest
import unittest.mock

from programy.clients.render.text import TextRenderer

class MockConsoleBotClient(object):

    def __init__(self):
        self._response = None

    def process_response(self, client_context, response, output_func=print):
        self._response = response


class TextRendererTests(unittest.TestCase):

    def test_text_only(self):
        mock_console = MockConsoleBotClient()
        renderer = TextRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", "Hello world")

        self.assertEqual(mock_console._response, "Hello world")

    def test_url_button(self):
        mock_console = MockConsoleBotClient()
        renderer = TextRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", "<button><text>Hello</text><url>http://click.me</url></button>")

        self.assertEqual(mock_console._response, "Hello, click http://click.me")

    def test_postback_button(self):
        mock_console = MockConsoleBotClient()
        renderer = TextRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", "<button><text>Hello</text><postback>HELLO</postback></button>")

        self.assertEqual(mock_console._response, "HELLO")

    def test_link(self):
        mock_console = MockConsoleBotClient()
        renderer = TextRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", "<link><text>Hello</text><url>http://click.me</url></link>")

        self.assertEqual(mock_console._response, "Open in browser, click http://click.me")

    def test_image(self):
        mock_console = MockConsoleBotClient()
        renderer = TextRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", "<image>http://servusai.com/aiml.png</image>")

        self.assertEqual(mock_console._response, "To see the image, click http://servusai.com/aiml.png")

    def test_video(self):
        mock_console = MockConsoleBotClient()
        renderer = TextRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", "<video>http://servusai.com/aiml.mov</video>")

        self.assertEqual(mock_console._response, "To see the video, click http://servusai.com/aiml.mov")

    def test_card(self):
        mock_console = MockConsoleBotClient()
        renderer = TextRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", "<card><image>http://servusai.com/aiml.png</image><title>Servusai</title><subtitle>Home of ProgramY</subtitle><button><text>Hello</text><url>http://click.me</url></button></card>")

        self.assertEqual(mock_console._response, """Image: http://servusai.com/aiml.png
Title: Servusai
Subtitle: Home of ProgramY
---------------------------------------
Hello : http://click.me
---------------------------------------
""")

    def test_carousel(self):
        mock_console = MockConsoleBotClient()
        renderer = TextRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", "<carousel><card><image>http://servusai.com/aiml.png</image><title>Servusai</title><subtitle>Home of ProgramY</subtitle><button><text>Hello</text><url>http://click.me</url></button></card></carousel>")

        self.assertEqual(mock_console._response, """=========================================
Image: http://servusai.com/aiml.png
Title: Servusai
Subtitle: Home of ProgramY
---------------------------------------
Hello : http://click.me
---------------------------------------
=========================================
""")

    def test_reply_with_postback(self):
        mock_console = MockConsoleBotClient()
        renderer = TextRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", "<reply><text>Hello</text><postback>HELLO</postback></reply>")

        self.assertEqual(mock_console._response, "HELLO")

    def test_reply_without_postback(self):
        mock_console = MockConsoleBotClient()
        renderer = TextRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", "<reply><text>Hello</text></reply>")

        self.assertEqual(mock_console._response, "Hello")

    def test_delay(self):
        mock_console = MockConsoleBotClient()
        renderer = TextRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", "<delay><seconds>0</seconds></delay>")

        self.assertEqual(mock_console._response, "...")

    def test_split(self):
        mock_console = MockConsoleBotClient()
        renderer = TextRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", "<split />")

        self.assertEqual(mock_console._response, "\n")

    def test_list(self):
        mock_console = MockConsoleBotClient()
        renderer = TextRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", "<list><item>Item1</item><item>Item2</item></list>")

        self.assertEqual(mock_console._response, "> Item1\n> Item2\n")

    def test_olist(self):
        mock_console = MockConsoleBotClient()
        renderer = TextRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", "<olist><item>Item1</item><item>Item2</item></olist>")

        self.assertEqual(mock_console._response, "1. Item1\n2. Item2\n")

    def test_location(self):
        mock_console = MockConsoleBotClient()
        renderer = TextRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", "<location />")

        self.assertEqual(mock_console._response, "")

