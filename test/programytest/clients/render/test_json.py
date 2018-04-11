import unittest.mock

from programy.clients.render.json import JSONRenderer

class MockConsoleBotClient(object):

    def __init__(self):
        self._response = None

    def process_response(self, client_context, response):
        self._response = response
        return response

class JSONRendererTests(unittest.TestCase):

    def test_text_only(self):
        mock_console = MockConsoleBotClient()
        renderer = JSONRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", "Hello world")

        data = mock_console._response
        self.assertTrue('text' in data)
        self.assertEquals(data['text'], "Hello world")

    def test_url_button(self):
        mock_console = MockConsoleBotClient()
        renderer = JSONRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", "<button><text>Hello</text><url>http://click.me</url></button>")

        data = mock_console._response
        self.assertTrue('button' in data)

    def test_postback_button(self):
        mock_console = MockConsoleBotClient()
        renderer = JSONRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", "<button><text>Hello</text><postback>HELLO</postback></button>")

        data = mock_console._response
        self.assertTrue('button' in data)

    def test_link(self):
        mock_console = MockConsoleBotClient()
        renderer = JSONRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", "<link><text>Hello</text><url>http://click.me</url></link>")

        data = mock_console._response
        self.assertTrue('link' in data)

    def test_image(self):
        mock_console = MockConsoleBotClient()
        renderer = JSONRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", "<image>http://servusai.com/aiml.png</image>")

        data = mock_console._response
        self.assertTrue('image' in data)

    def test_video(self):
        mock_console = MockConsoleBotClient()
        renderer = JSONRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", "<video>http://servusai.com/aiml.mov</video>")

        data = mock_console._response
        self.assertTrue('video' in data)

    def test_card(self):
        mock_console = MockConsoleBotClient()
        renderer = JSONRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", "<card><image>http://servusai.com/aiml.png</image><title>Servusai</title><subtitle>Home of ProgramY</subtitle><button><text>Hello</text><url>http://click.me</url></button></card>")

        data = mock_console._response
        self.assertTrue('card' in data)

    def test_carousel(self):
        mock_console = MockConsoleBotClient()
        renderer = JSONRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", "<carousel><card><image>http://servusai.com/aiml.png</image><title>Servusai</title><subtitle>Home of ProgramY</subtitle><button><text>Hello</text><url>http://click.me</url></button></card></carousel>")

        data = mock_console._response
        self.assertTrue('carousel' in data)

    def test_reply_with_postback(self):
        mock_console = MockConsoleBotClient()
        renderer = JSONRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", "<reply><text>Hello</text><postback>HELLO</postback></reply>")

        data = mock_console._response
        self.assertTrue('reply' in data)

    def test_reply_without_postback(self):
        mock_console = MockConsoleBotClient()
        renderer = JSONRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", "<reply><text>Hello</text></reply>")

        data = mock_console._response
        self.assertTrue('reply' in data)

    def test_delay(self):
        mock_console = MockConsoleBotClient()
        renderer = JSONRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", "<delay><seconds>0</seconds></delay>")

        data = mock_console._response
        self.assertTrue('delay' in data)

    def test_split(self):
        mock_console = MockConsoleBotClient()
        renderer = JSONRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", "<split />")

        data = mock_console._response
        self.assertTrue('split' in data)

    def test_list(self):
        mock_console = MockConsoleBotClient()
        renderer = JSONRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", "<list><item>Item1</item><item>Item2</item></list>")

        data = mock_console._response
        self.assertTrue('list' in data)

    def test_olist(self):
        mock_console = MockConsoleBotClient()
        renderer = JSONRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", "<olist><item>Item1</item><item>Item2</item></olist>")

        data = mock_console._response
        self.assertTrue('olist' in data)

    def test_location(self):
        mock_console = MockConsoleBotClient()
        renderer = JSONRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", "<location />")

        data = mock_console._response
        self.assertTrue('location' in data)

