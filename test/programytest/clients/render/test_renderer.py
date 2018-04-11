import unittest
import unittest.mock

from programy.clients.render.renderer import RichMediaRenderer

class MockRichMediaRenderer(RichMediaRenderer):

    def __init__(self, config):
        RichMediaRenderer.__init__(self, config)

    def handle_text(self, userid, text):
        self._userid = userid
        self._text = text
        return text

    def handle_url_button(self, userid, text, url):
        self._userid = userid
        self._text = text
        self._url = url
        return text

    def handle_postback_button(self, userid, text, postback):
        self._userid = userid
        self._text = text
        self._postback = postback
        return text

    def handle_link(self, userid, text, url):
        self._userid = userid
        self._text = text
        self._url = url
        return text

    def handle_image(self, userid, url):
        self._userid = userid
        self._url = url
        return url

    def handle_video(self, userid, url):
        self._userid = userid
        self._url = url
        return url

    def handle_card(self, userid, image, title, subtitle, buttons):
        self._userid = userid
        self._image = image
        self._title = title
        self._subtitle = subtitle
        self._buttons = buttons
        return "image"

    def handle_carousel(self, userid, cards):
        self._userid = userid
        self._cards = cards
        return "carousel"

    def handle_reply(self, userid, text, postback):
        self._userid = userid
        self._text = text
        self._postback = postback
        return text

    def handle_delay(self, userid, seconds):
        self._userid = userid
        self._seconds = seconds
        return seconds

    def handle_split(self, userid):
        self._userid = userid
        return "split"

    def handle_list(self, userid, items):
        self._userid = userid
        self._items = items
        return items

    def handle_ordered_list(self, userid, items):
        self._userid = userid
        self._items = items
        return items

    def handle_location(self, userid):
        self._userid = userid
        return "location"

class RichMediaRendererTests(unittest.TestCase):

    def test_text_only(self):
        mock_config = unittest.mock.Mock()
        renderer = MockRichMediaRenderer(mock_config)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", "Hello world")

        self.assertEquals(renderer._userid, "testuser")
        self.assertEquals(renderer._text, "Hello world")

    def test_url_button(self):
        mock_config = unittest.mock.Mock()
        renderer = MockRichMediaRenderer(mock_config)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", "<button><text>Hello</text><url>http://click.me</url></button>")

        self.assertEquals(renderer._userid, "testuser")
        self.assertEquals(renderer._text, "Hello")
        self.assertEquals(renderer._url, "http://click.me")

    def test_postback_button(self):
        mock_config = unittest.mock.Mock()
        renderer = MockRichMediaRenderer(mock_config)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", "<button><text>Hello</text><postback>HELLO</url></postback></button>")

        self.assertEquals(renderer._userid, "testuser")
        self.assertEquals(renderer._text, "Hello")
        self.assertEquals(renderer._postback, "HELLO")

    def test_link(self):
        mock_config = unittest.mock.Mock()
        renderer = MockRichMediaRenderer(mock_config)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", "<link><text>Hello</text><url>http://click.me</url></link>")

        self.assertEquals(renderer._userid, "testuser")
        self.assertEquals(renderer._text, "Hello")
        self.assertEquals(renderer._url, "http://click.me")

    def test_image(self):
        mock_config = unittest.mock.Mock()
        renderer = MockRichMediaRenderer(mock_config)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", "<image>http://servusai.com/aiml.png</image>")

        self.assertEquals(renderer._userid, "testuser")
        self.assertEquals(renderer._url, "http://servusai.com/aiml.png")

    def test_video(self):
        mock_config = unittest.mock.Mock()
        renderer = MockRichMediaRenderer(mock_config)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", "<video>http://servusai.com/aiml.mov</video>")

        self.assertEquals(renderer._userid, "testuser")
        self.assertEquals(renderer._url, "http://servusai.com/aiml.mov")

    def test_card(self):
        mock_config = unittest.mock.Mock()
        renderer = MockRichMediaRenderer(mock_config)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", "<card><image>http://servusai.com/aiml.png</image><title>Servusai</title><subtitle>Home of ProgramY</subtitle><button><text>Hello</text><url>http://click.me</url></button></card>")

        self.assertEquals(renderer._userid, "testuser")
        self.assertEquals(renderer._image, "http://servusai.com/aiml.png")
        self.assertEquals(renderer._title, "Servusai")
        self.assertEquals(renderer._subtitle, "Home of ProgramY")
        self.assertEquals(len(renderer._buttons), 1)
        self.assertEquals(renderer._buttons[0], ("Hello", "http://click.me", None))

    def test_carousel(self):
        mock_config = unittest.mock.Mock()
        renderer = MockRichMediaRenderer(mock_config)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", "<carousel><card><image>http://servusai.com/aiml.png</image><title>Servusai</title><subtitle>Home of ProgramY</subtitle><button><text>Hello</text><url>http://click.me</url></button></card></carousel>")

        self.assertEquals(renderer._userid, "testuser")
        self.assertEquals(len(renderer._cards), 1)
        self.assertEquals(renderer._cards[0], ('http://servusai.com/aiml.png', 'Servusai', 'Home of ProgramY', [('Hello', 'http://click.me', None)]))

    def test_reply_with_postback(self):
        mock_config = unittest.mock.Mock()
        renderer = MockRichMediaRenderer(mock_config)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", "<reply><text>Hello</text><postback>HELLO</url></postback></reply>")

        self.assertEquals(renderer._userid, "testuser")
        self.assertEquals(renderer._text, "Hello")
        self.assertEquals(renderer._postback, "HELLO")

    def test_reply_without_postback(self):
        mock_config = unittest.mock.Mock()
        renderer = MockRichMediaRenderer(mock_config)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", "<reply><text>Hello</text></reply>")

        self.assertEquals(renderer._userid, "testuser")
        self.assertEquals(renderer._text, "Hello")
        self.assertIsNone(renderer._postback)

    def test_delay(self):
        mock_config = unittest.mock.Mock()
        renderer = MockRichMediaRenderer(mock_config)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", "<delay><seconds>10</seconds></delay>")

        self.assertEquals(renderer._userid, "testuser")
        self.assertEquals(renderer._seconds, "10")

    def test_split(self):
        mock_config = unittest.mock.Mock()
        renderer = MockRichMediaRenderer(mock_config)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", "<split />")

        self.assertEquals(renderer._userid, "testuser")

    def test_list(self):
        mock_config = unittest.mock.Mock()
        renderer = MockRichMediaRenderer(mock_config)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", "<list><item>Item1</item><item>Item2</item></list>")

        self.assertEquals(renderer._userid, "testuser")
        self.assertIsNotNone(renderer._items)
        self.assertEquals(len(renderer._items), 2)
        self.assertEquals(renderer._items[0], "Item1")
        self.assertEquals(renderer._items[1], "Item2")

    def test_list_with_nested_rcs(self):
        mock_config = unittest.mock.Mock()
        renderer = MockRichMediaRenderer(mock_config)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", """
        <list>
            <item>
                <list>
                    <item>Item1.1</item>
                    <item>Item1.2</item>
                </list>
            </item>
            <item>
                Item2
            </item>
        </list>
        """)

        self.assertEquals(renderer._userid, "testuser")
        self.assertIsNotNone(renderer._items)
        self.assertEquals(len(renderer._items), 2)
        self.assertEquals(renderer._items[0], ['Item1.1', 'Item1.2'])
        self.assertEquals(renderer._items[1], "Item2")

    def test_olist(self):
        mock_config = unittest.mock.Mock()
        renderer = MockRichMediaRenderer(mock_config)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", "<olist><item>Item1</item><item>Item2</item></olist>")

        self.assertEquals(renderer._userid, "testuser")
        self.assertIsNotNone(renderer._items)
        self.assertEquals(len(renderer._items), 2)
        self.assertEquals(renderer._items[0], "Item1")
        self.assertEquals(renderer._items[1], "Item2")

    def test_location(self):
        mock_config = unittest.mock.Mock()
        renderer = MockRichMediaRenderer(mock_config)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", "<location />")

        self.assertEquals(renderer._userid, "testuser")

    def test_xml_html(self):
        mock_config = unittest.mock.Mock()
        renderer = MockRichMediaRenderer(mock_config)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", "<ul><li>item1</li><li>item2</li></ul>")

        self.assertEquals(renderer._userid, "testuser")
        self.assertEquals(renderer._text, "<ul><li>item1</li><li>item2</li></ul>")

