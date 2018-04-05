import unittest
import unittest.mock

from programy.clients.render.html_renderer import HtmlRenderer

class MockHtmlBotClient(object):

    def __init__(self):
        self._response = None
        self.configuration = unittest.mock.Mock()
        self.configuration.host = "127.0.0.1"
        self.configuration.port = "6666"
        self.configuration.api  = "/api/web/v1.0/ask"

    def display_response(self, response, output_func=print):
        self._response = response


class HtmlRendererTests(unittest.TestCase):

    def test_create_postback_url(self):
        mock_console = MockHtmlBotClient()
        renderer = HtmlRenderer(mock_console)
        self.assertIsNotNone(renderer)

        postback = renderer.create_postback_url("Hello world")
        self.assertIsNotNone(postback)
        self.assertEquals(postback, "http://127.0.0.1:6666/api/web/v1.0/askquestion=Hello+world")

    def test_text_only(self):
        mock_console = MockHtmlBotClient()
        renderer = HtmlRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.send_message("testuser", "Hello world")

        self.assertEquals(mock_console._response, "<p>Hello world</p>")

    def test_url_button(self):
        mock_console = MockHtmlBotClient()
        renderer = HtmlRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.send_message("testuser", "<button><text>Hello</text><url>http://click.me</url></button>")

        self.assertEquals(mock_console._response, '<a href="http://click.me">Hello</a>')

    def test_postback_button(self):
        mock_console = MockHtmlBotClient()
        renderer = HtmlRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.send_message("testuser", "<button><text>Hello</text><postback>HELLO</postback></button>")

        self.assertEquals(mock_console._response, '<a href="http://127.0.0.1:6666/api/web/v1.0/askquestion=HELLO">Hello</a>')

    def test_link(self):
        mock_console = MockHtmlBotClient()
        renderer = HtmlRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.send_message("testuser", "<link><text>Hello</text><url>http://click.me</url></link>")

        self.assertEquals(mock_console._response, '<a href="http://click.me">Hello</a>')

    def test_image(self):
        mock_console = MockHtmlBotClient()
        renderer = HtmlRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.send_message("testuser", "<image>http://servusai.com/aiml.png</image>")

        self.assertEquals(mock_console._response, '<img src="http://servusai.com/aiml.png" />')

    def test_video(self):
        mock_console = MockHtmlBotClient()
        renderer = HtmlRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.send_message("testuser", "<video>http://servusai.com/aiml.mov</video>")

        self.assertEquals(mock_console._response, """<video src="http://servusai.com/aiml.mov">
Sorry, your browser doesn't support embedded videos, 
but don't worry, you can <a href="http://servusai.com/aiml.mov">download it</a>
and watch it with your favorite video player!
</video>""")

    def test_card(self):
        mock_console = MockHtmlBotClient()
        renderer = HtmlRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.send_message("testuser", "<card><image>http://servusai.com/aiml.png</image><title>Servusai</title><subtitle>Home of ProgramY</subtitle><button><text>Hello</text><url>http://click.me</url></button></card>")

        self.assertEquals(mock_console._response, '<div class="card" ><img src="http://servusai.com/aiml.png" /><h1>Servusai</h1><h2>Home of ProgramY</h2><a href="http://click.me">Hello</a></div>')

    def test_carousel(self):
        mock_console = MockHtmlBotClient()
        renderer = HtmlRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.send_message("testuser", "<carousel><card><image>http://servusai.com/aiml.png</image><title>Servusai</title><subtitle>Home of ProgramY</subtitle><button><text>Hello</text><url>http://click.me</url></button></card></carousel>")

        self.assertEquals(mock_console._response, '<carousel><div class="card" ><img src="http://servusai.com/aiml.png" /><h1>Servusai</h1><h2>Home of ProgramY</h2><a href="http://click.me">Hello</a></div></carousel>')

    def test_reply_with_postback(self):
        mock_console = MockHtmlBotClient()
        renderer = HtmlRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.send_message("testuser", "<reply><text>Hello</text><postback>HELLO</postback></reply>")

        self.assertEquals(mock_console._response, '<div class="reply"><a href="http://127.0.0.1:6666/api/web/v1.0/askquestion=HELLO">Hello</a></div>')

    def test_reply_without_postback(self):
        mock_console = MockHtmlBotClient()
        renderer = HtmlRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.send_message("testuser", "<reply><text>Hello</text></reply>")

        self.assertEquals(mock_console._response, '<div class="reply"><a href="http://127.0.0.1:6666/api/web/v1.0/askquestion=Hello">Hello</a></div>')

    def test_delay(self):
        mock_console = MockHtmlBotClient()
        renderer = HtmlRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.send_message("testuser", "<delay><seconds>0</seconds></delay>")

        self.assertEquals(mock_console._response, '<div class="delay">...</div>')

    def test_split(self):
        mock_console = MockHtmlBotClient()
        renderer = HtmlRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.send_message("testuser", "<split />")

        self.assertEquals(mock_console._response, "")

    def test_list(self):
        mock_console = MockHtmlBotClient()
        renderer = HtmlRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.send_message("testuser", "<list><item>Item1</item><item>Item2</item></list>")

        self.assertEquals(mock_console._response, "<ul><li>Item1</li><li>Item2</li></ul>")

    def test_olist(self):
        mock_console = MockHtmlBotClient()
        renderer = HtmlRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.send_message("testuser", "<olist><item>Item1</item><item>Item2</item></olist>")

        self.assertEquals(mock_console._response, "<ol><li>Item1</li><li>Item2</li></ol>")

    def test_location(self):
        mock_console = MockHtmlBotClient()
        renderer = HtmlRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.send_message("testuser", "<location />")

        self.assertEquals(mock_console._response, "")

