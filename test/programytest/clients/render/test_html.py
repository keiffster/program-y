import unittest
import unittest.mock

from programy.clients.render.html import HtmlRenderer


class MockHtmlBotClient(object):

    def __init__(self):
        self._response = None
        self.configuration = unittest.mock.Mock()
        self.configuration.host = "127.0.0.1"
        self.configuration.port = "6666"
        self.configuration.api  = "/api/web/v1.0/ask"

    def process_response(self, client_context, response):
        self._response = response


class HtmlRendererTests(unittest.TestCase):

    def test_create_postback_url(self):
        mock_console = MockHtmlBotClient()
        renderer = HtmlRenderer(mock_console)
        self.assertIsNotNone(renderer)

        postback = renderer.create_postback_url()
        self.assertIsNotNone(postback)
        self.assertEqual(postback, "#")

    def test_text_only(self):
        mock_console = MockHtmlBotClient()
        renderer = HtmlRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", "Hello world")

        self.assertEqual(mock_console._response, "Hello world")

    def test_url_button(self):
        mock_console = MockHtmlBotClient()
        renderer = HtmlRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", '<button"><text>Hello</text><url>http://click.me</url></button>')

        self.assertEqual(mock_console._response, '<a class="programy" href="http://click.me">Hello</a>')

    def test_url_button_with_class_and_id(self):
        mock_console = MockHtmlBotClient()
        renderer = HtmlRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", '<button class="class1" id="id1"><text>Hello</text><url>http://click.me</url></button>')

        self.assertEqual(mock_console._response, '<a class="class1 programy" id="id1" href="http://click.me">Hello</a>')

    def test_postback_button(self):
        mock_console = MockHtmlBotClient()
        renderer = HtmlRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", "<button><text>Hello</text><postback>HELLO</postback></button>")

        self.assertEqual(mock_console._response, '<a class="programy" postback="HELLO" href="#">Hello</a>')

    def test_postback_button_with_class_and_id(self):
        mock_console = MockHtmlBotClient()
        renderer = HtmlRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", '<button class="class1" id="id1"><text>Hello</text><postback>HELLO</postback></button>')

        self.assertEqual(mock_console._response, '<a class="class1 programy" id="id1" postback="HELLO" href="#">Hello</a>')

    def test_link(self):
        mock_console = MockHtmlBotClient()
        renderer = HtmlRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", "<link><text>Hello</text><url>http://click.me</url></link>")

        self.assertEqual(mock_console._response, '<a class="programy" href="http://click.me">Hello</a>')

    def test_link_with_class_and_id(self):
        mock_console = MockHtmlBotClient()
        renderer = HtmlRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", '<link class="class1" id="id1"><text>Hello</text><url>http://click.me</url></link>')

        self.assertEqual(mock_console._response, '<a class="class1 programy" id="id1" href="http://click.me">Hello</a>')

    def test_image(self):
        mock_console = MockHtmlBotClient()
        renderer = HtmlRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", '<image>http://servusai.com/aiml.png</image>')

        self.assertEqual(mock_console._response, '<img class="programy" src="http://servusai.com/aiml.png" />')

    def test_image_with_class_and_id(self):
        mock_console = MockHtmlBotClient()
        renderer = HtmlRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", '<image class="class1" id="id1">http://servusai.com/aiml.png</image>')

        self.assertEqual(mock_console._response, '<img class="class1 programy" id="id1" src="http://servusai.com/aiml.png" />')

    def test_video(self):
        mock_console = MockHtmlBotClient()
        renderer = HtmlRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", "<video>http://servusai.com/aiml.mov</video>")

        self.assertEqual(mock_console._response, """<video class="programy" src="http://servusai.com/aiml.mov">
Sorry, your browser doesn't support embedded videos, 
but don't worry, you can <a href="http://servusai.com/aiml.mov">download it</a>
and watch it with your favorite video player!
</video>""")

    def test_video_with_class_and_id(self):
        mock_console = MockHtmlBotClient()
        renderer = HtmlRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", '<video class="class1" id="id1">http://servusai.com/aiml.mov</video>')

        self.assertEqual(mock_console._response, """<video class="class1 programy" id="id1" src="http://servusai.com/aiml.mov">
Sorry, your browser doesn't support embedded videos, 
but don't worry, you can <a href="http://servusai.com/aiml.mov">download it</a>
and watch it with your favorite video player!
</video>""")

    def test_card(self):
        mock_console = MockHtmlBotClient()
        renderer = HtmlRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", '<card><image>http://servusai.com/aiml.png</image><title>Servusai</title><subtitle>Home of ProgramY</subtitle><button><text>Hello</text><url>http://click.me</url></button></card>')

        self.assertEqual(mock_console._response, '<div class="programy"><img src="http://servusai.com/aiml.png" /><h1>Servusai</h1><h2>Home of ProgramY</h2><a href="http://click.me">Hello</a></div>')

    def test_card_with_class_and_id(self):
        mock_console = MockHtmlBotClient()
        renderer = HtmlRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", '<card class="class1" id="id1"><image>http://servusai.com/aiml.png</image><title>Servusai</title><subtitle>Home of ProgramY</subtitle><button><text>Hello</text><url>http://click.me</url></button></card>')

        self.assertEqual(mock_console._response, '<div class="class1 programy" id="id1"><img src="http://servusai.com/aiml.png" /><h1>Servusai</h1><h2>Home of ProgramY</h2><a href="http://click.me">Hello</a></div>')

    def test_carousel(self):
        mock_console = MockHtmlBotClient()
        renderer = HtmlRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", "<carousel><card><image>http://servusai.com/aiml.png</image><title>Servusai</title><subtitle>Home of ProgramY</subtitle><button><text>Hello</text><url>http://click.me</url></button></card></carousel>")

        self.assertEqual(mock_console._response, '<div class="programy"><div class="programy"><img src="http://servusai.com/aiml.png" /><h1>Servusai</h1><h2>Home of ProgramY</h2><a href="http://click.me">Hello</a></div></div>')

    def test_carousel_with_class_and_id(self):
        mock_console = MockHtmlBotClient()
        renderer = HtmlRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", '<carousel class="class1" id="id1"><card><image>http://servusai.com/aiml.png</image><title>Servusai</title><subtitle>Home of ProgramY</subtitle><button><text>Hello</text><url>http://click.me</url></button></card></carousel>')

        self.assertEqual(mock_console._response, '<div class="class1 programy" id="id1"><div class="programy"><img src="http://servusai.com/aiml.png" /><h1>Servusai</h1><h2>Home of ProgramY</h2><a href="http://click.me">Hello</a></div></div>')

    def test_reply_with_postback(self):
        mock_console = MockHtmlBotClient()
        renderer = HtmlRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", "<reply><text>Hello</text><postback>HELLO</postback></reply>")

        self.assertEqual(mock_console._response, '<a class="programy" postback="HELLO" href="#">Hello</a>')

    def test_reply_with_postback_with_class_and_id(self):
        mock_console = MockHtmlBotClient()
        renderer = HtmlRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", '<reply class="class1" id="id1"><text>Hello</text><postback>HELLO</postback></reply>')

        self.assertEqual(mock_console._response, '<a class="class1 programy" id="id1" postback="HELLO" href="#">Hello</a>')

    def test_reply_without_postback(self):
        mock_console = MockHtmlBotClient()
        renderer = HtmlRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", "<reply><text>Hello</text></reply>")

        self.assertEqual(mock_console._response, '<a class="programy" postback="Hello" href="#">Hello</a>')

    def test_reply_without_postback_with_class_and_id(self):
        mock_console = MockHtmlBotClient()
        renderer = HtmlRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", '<reply class="class1" id="id1"><text>Hello</text></reply>')

        self.assertEqual(mock_console._response, '<a class="class1 programy" id="id1" postback="Hello" href="#">Hello</a>')

    def test_delay(self):
        mock_console = MockHtmlBotClient()
        renderer = HtmlRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", "<delay><seconds>0</seconds></delay>")

        self.assertEqual(mock_console._response, '<div class="programy">...</div>')

    def test_delay_with_class_and_id(self):
        mock_console = MockHtmlBotClient()
        renderer = HtmlRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", '<delay class="class1" id="id1" ><seconds>0</seconds></delay>')

        self.assertEqual(mock_console._response, '<div class="class1 programy" id="id1">...</div>')

    def test_split(self):
        mock_console = MockHtmlBotClient()
        renderer = HtmlRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", "<split />")

        self.assertEqual(mock_console._response, '<br class="programy" />')

    def test_split_with_class_and_id(self):
        mock_console = MockHtmlBotClient()
        renderer = HtmlRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", '<split class="class1" id="id1"/>')

        self.assertEqual(mock_console._response, '<br class="class1 programy" id="id1" />')

    def test_list(self):
        mock_console = MockHtmlBotClient()
        renderer = HtmlRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", '<list><item>Item1</item><item>Item2</item></list>')

        self.assertEqual(mock_console._response, '<ul class="programy"><li>Item1</li><li>Item2</li></ul>')

    def test_list_with_children(self):
        mock_console = MockHtmlBotClient()
        renderer = HtmlRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", '<list><item>Hi</item><item><button"><text>Hello</text><url>http://click.me</url></button></item><item><button"><text>Goodbye</text><url>http://click.me</url></button></item></list>')
        print(mock_console._response)
        self.assertEqual(mock_console._response, '<ul class="programy"><li>Hi</li><li><a class="programy" postback="Hello" href="#">Hello</a></li><li><a class="programy" postback="Goodbye" href="#">Goodbye</a></li></ul>')

    def test_list_with_class_and_id(self):
        mock_console = MockHtmlBotClient()
        renderer = HtmlRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", '<list class="class1" id="id1"><item>Item1</item><item>Item2</item></list>')

        self.assertEqual(mock_console._response, '<ul class="class1 programy" id="id1"><li>Item1</li><li>Item2</li></ul>')

    def test_olist(self):
        mock_console = MockHtmlBotClient()
        renderer = HtmlRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", "<olist><item>Item1</item><item>Item2</item></olist>")

        self.assertEqual(mock_console._response, '<ol class="programy"><li>Item1</li><li>Item2</li></ol>')

    def test_olist_with_children(self):
        mock_console = MockHtmlBotClient()
        renderer = HtmlRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", '<olist><item>Hi</item><item><button"><text>Hello</text><url>http://click.me</url></button></item><item><button"><text>Goodbye</text><url>http://click.me</url></button></item></olist>')
        print(mock_console._response)
        self.assertEqual(mock_console._response, '<ol class="programy"><li>Hi</li><li><a class="programy" postback="Hello" href="#">Hello</a></li><li><a class="programy" postback="Goodbye" href="#">Goodbye</a></li></ol>')

    def test_olist_with_class_and_id(self):
        mock_console = MockHtmlBotClient()
        renderer = HtmlRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", '<olist class="class1" id="id1"><item>Item1</item><item>Item2</item></olist>')

        self.assertEqual(mock_console._response, '<ol class="class1 programy" id="id1"><li>Item1</li><li>Item2</li></ol>')

    def test_location(self):
        mock_console = MockHtmlBotClient()
        renderer = HtmlRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", "<location />")

        self.assertEqual(mock_console._response, "")

    def test_location(self):
        mock_console = MockHtmlBotClient()
        renderer = HtmlRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", '<location />')

        self.assertEqual(mock_console._response, "")

    def test_location_with_class_and_id(self):
        mock_console = MockHtmlBotClient()
        renderer = HtmlRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", '<location class="class1 programy" id="id1"/>')

        self.assertEqual(mock_console._response, "")

    def test_tts(self):
        mock_console = MockHtmlBotClient()
        renderer = HtmlRenderer(mock_console)
        self.assertIsNotNone(renderer)

        rendered = renderer.render("testuser", '<tts>Some speech</tts>')

        self.assertEqual(rendered, '')

    def test_tts_with_class_and_id(self):
        mock_console = MockHtmlBotClient()
        renderer = HtmlRenderer(mock_console)
        self.assertIsNotNone(renderer)

        rendered = renderer.render("testuser", '<tts class="class1 programy" id="id1">Some speech</tts>')

        self.assertEqual(rendered, '')

    def test_card_with_xml_at_front(self):
        mock_console = MockHtmlBotClient()
        renderer = HtmlRenderer(mock_console)
        self.assertIsNotNone(renderer)

        rendered = renderer.render("testuser", '<something>Some speech</something><card><image>http://servusai.com/aiml.png</image><title>Servusai</title><subtitle>Home of ProgramY</subtitle><button><text>Hello</text><url>http://click.me</url></button></card>')

        self.assertEqual(rendered, '<something>Some speech</something><div class="programy"><img src="http://servusai.com/aiml.png" /><h1>Servusai</h1><h2>Home of ProgramY</h2><a href="http://click.me">Hello</a></div>')

    def test_card_with_xml_at_end(self):
        mock_console = MockHtmlBotClient()
        renderer = HtmlRenderer(mock_console)
        self.assertIsNotNone(renderer)

        rendered = renderer.render("testuser", '<card><image>http://servusai.com/aiml.png</image><title>Servusai</title><subtitle>Home of ProgramY</subtitle><button><text>Hello</text><url>http://click.me</url></button></card><something>Some speech</something>')

        self.assertEqual(rendered, '<div class="programy"><img src="http://servusai.com/aiml.png" /><h1>Servusai</h1><h2>Home of ProgramY</h2><a href="http://click.me">Hello</a></div><something>Some speech</something>')

    def test_card_with_xml_at_front_and_end(self):
        mock_console = MockHtmlBotClient()
        renderer = HtmlRenderer(mock_console)
        self.assertIsNotNone(renderer)

        rendered = renderer.render("testuser", '<something>Some speech</something><card><image>http://servusai.com/aiml.png</image><title>Servusai</title><subtitle>Home of ProgramY</subtitle><button><text>Hello</text><url>http://click.me</url></button></card><something>Some speech</something>')

        self.assertEqual(rendered, '<something>Some speech</something><div class="programy"><img src="http://servusai.com/aiml.png" /><h1>Servusai</h1><h2>Home of ProgramY</h2><a href="http://click.me">Hello</a></div><something>Some speech</something>')

    def test_card_with_text_at_front(self):
        mock_console = MockHtmlBotClient()
        renderer = HtmlRenderer(mock_console)
        self.assertIsNotNone(renderer)

        rendered = renderer.render("testuser", 'Hello<card><image>http://servusai.com/aiml.png</image><title>Servusai</title><subtitle>Home of ProgramY</subtitle><button><text>Hello</text><url>http://click.me</url></button></card>')

        self.assertEqual(rendered, 'Hello<div class="programy"><img src="http://servusai.com/aiml.png" /><h1>Servusai</h1><h2>Home of ProgramY</h2><a href="http://click.me">Hello</a></div>')

    def test_card_with_text_at_end(self):
        mock_console = MockHtmlBotClient()
        renderer = HtmlRenderer(mock_console)
        self.assertIsNotNone(renderer)

        rendered = renderer.render("testuser", '<card><image>http://servusai.com/aiml.png</image><title>Servusai</title><subtitle>Home of ProgramY</subtitle><button><text>Hello</text><url>http://click.me</url></button></card>Hello')

        self.assertEqual(rendered, '<div class="programy"><img src="http://servusai.com/aiml.png" /><h1>Servusai</h1><h2>Home of ProgramY</h2><a href="http://click.me">Hello</a></div>Hello')

    def test_card_with_text_at_front_and_end(self):
        mock_console = MockHtmlBotClient()
        renderer = HtmlRenderer(mock_console)
        self.assertIsNotNone(renderer)

        rendered = renderer.render("testuser", 'Hello<card><image>http://servusai.com/aiml.png</image><title>Servusai</title><subtitle>Home of ProgramY</subtitle><button><text>Hello</text><url>http://click.me</url></button></card>Hello')

        self.assertEqual(rendered, 'Hello<div class="programy"><img src="http://servusai.com/aiml.png" /><h1>Servusai</h1><h2>Home of ProgramY</h2><a href="http://click.me">Hello</a></div>Hello')
