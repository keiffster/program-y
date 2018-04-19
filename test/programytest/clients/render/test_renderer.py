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

    def handle_url_button(self, userid, button):
        self._userid = userid
        self._button = button
        return None

    def handle_postback_button(self, userid, button):
        self._userid = userid
        self._button = button
        return None

    def handle_link(self, userid, link):
        self._userid = userid
        self._link = link
        return None

    def handle_image(self, userid, image):
        self._userid = userid
        self._image = image
        return None

    def handle_video(self, userid, video):
        self._userid = userid
        self._video = video
        return None

    def handle_card(self, userid, card):
        self._userid = userid
        self._card = card
        return None

    def handle_carousel(self, userid, carousel):
        self._userid = userid
        self._carousel = carousel
        return None

    def handle_reply(self, userid, reply):
        self._userid = userid
        self._reply = reply
        return None

    def handle_delay(self, userid, delay):
        self._userid = userid
        self._delay = delay
        return None

    def handle_split(self, userid, split):
        self._userid = userid
        self._split = split
        return None

    def handle_list(self, userid, list):
        self._userid = userid
        self._list = list
        return None

    def handle_ordered_list(self, userid, items):
        self._userid = userid
        self._list = list
        return None

    def handle_location(self, userid, location):
        self._userid = userid
        self._location = location
        return None


class RichMediaRendererTests(unittest.TestCase):

    def test_text_only(self):
        mock_config = unittest.mock.Mock()
        renderer = MockRichMediaRenderer(mock_config)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", "Hello world")

        self.assertEquals(renderer._userid, "testuser")
        self.assertIsNotNone(renderer._text)
        self.assertEquals("text", renderer._text['type'])
        self.assertEquals("Hello world", renderer._text['text'])

    def test_xml_html(self):
        mock_config = unittest.mock.Mock()
        renderer = MockRichMediaRenderer(mock_config)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", """
            <ul>
                <li>item1</li>
                <li>item2</li>
            </ul>""")

        self.assertEquals(renderer._userid, "testuser")
        self.assertIsNotNone(renderer._text)
        self.assertEquals("text", renderer._text['type'])
        self.assertEquals("<ul>\n<li>item1</li>\n<li>item2</li>\n</ul>", renderer._text['text'])

    def test_url_button(self):
        mock_config = unittest.mock.Mock()
        renderer = MockRichMediaRenderer(mock_config)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", """
            <button>
                <text>Hello</text>
                <url>http://click.me</url>
            </button>""")

        self.assertEquals(renderer._userid, "testuser")
        self.assertIsNotNone(renderer._button)
        self.assertEquals("button", renderer._button['type'])
        self.assertEquals(renderer._button['text'], "Hello")
        self.assertEquals(renderer._button['url'], "http://click.me")

    def test_postback_button(self):
        mock_config = unittest.mock.Mock()
        renderer = MockRichMediaRenderer(mock_config)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", """
            <button>
                <text>Hello</text>
                <postback>HELLO</url></postback>
            </button>""")

        self.assertEquals(renderer._userid, "testuser")
        self.assertIsNotNone(renderer._button)
        self.assertEquals("button", renderer._button['type'])
        self.assertEquals(renderer._button['text'], "Hello")
        self.assertEquals(renderer._button['postback'], "HELLO")

    def test_link(self):
        mock_config = unittest.mock.Mock()
        renderer = MockRichMediaRenderer(mock_config)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", """
            <link>
                <text>Hello</text>
                <url>http://click.me</url>
            </link>""")

        self.assertEquals(renderer._userid, "testuser")
        self.assertIsNotNone(renderer._link)
        self.assertEquals("link", renderer._link['type'])
        self.assertEquals(renderer._link['text'], "Hello")
        self.assertEquals(renderer._link['url'], "http://click.me")

    def test_image(self):
        mock_config = unittest.mock.Mock()
        renderer = MockRichMediaRenderer(mock_config)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", """
            <image>
                http://servusai.com/aiml.png
            </image>""")

        self.assertEquals(renderer._userid, "testuser")
        self.assertIsNotNone(renderer._image)
        self.assertEquals("image", renderer._image['type'])
        self.assertEquals(renderer._image['url'], "http://servusai.com/aiml.png")

    def test_video(self):
        mock_config = unittest.mock.Mock()
        renderer = MockRichMediaRenderer(mock_config)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", """
            <video>
                http://servusai.com/aiml.mov
            </video>""")

        self.assertEquals(renderer._userid, "testuser")
        self.assertIsNotNone(renderer._video)
        self.assertEquals("video", renderer._video['type'])
        self.assertEquals(renderer._video['url'], "http://servusai.com/aiml.mov")

    def test_card(self):
        mock_config = unittest.mock.Mock()
        renderer = MockRichMediaRenderer(mock_config)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", """
            <card>
                <image>http://servusai.com/aiml.png</image>
                <title>Servusai</title>
                <subtitle>Home of ProgramY</subtitle>
                <button>
                    <text>Hello</text>
                    <url>http://click.me</url>
                </button>
            </card>""")

        self.assertEquals(renderer._userid, "testuser")
        self.assertIsNotNone(renderer._card)
        self.assertEquals("card", renderer._card['type'])
        self.assertEquals(renderer._card['image'], "http://servusai.com/aiml.png")
        self.assertEquals(renderer._card['title'], "Servusai")
        self.assertEquals(renderer._card['subtitle'], "Home of ProgramY")
        self.assertEquals(len(renderer._card['buttons']), 1)

        button1 = renderer._card['buttons'][0]
        self.assertEquals("button", button1['type'])
        self.assertEquals(button1['text'], "Hello")
        self.assertEquals(button1['url'], "http://click.me")

    def test_carousel(self):
        mock_config = unittest.mock.Mock()
        renderer = MockRichMediaRenderer(mock_config)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", """
            <carousel>
                <card>
                    <image>http://servusai.com/aiml.png</image>
                    <title>Servusai</title>
                    <subtitle>Home of ProgramY</subtitle>
                    <button>
                        <text>Hello</text>
                        <url>http://click.me</url>
                    </button>
                </card>
            </carousel>""")

        self.assertEquals(renderer._userid, "testuser")
        self.assertIsNotNone(renderer._carousel)
        self.assertEquals("carousel", renderer._carousel['type'])
        self.assertEquals(1, len(renderer._carousel['cards']))

        card1 = renderer._carousel['cards'][0]
        self.assertEquals(card1['image'], "http://servusai.com/aiml.png")
        self.assertEquals(card1['title'], "Servusai")
        self.assertEquals(card1['subtitle'], "Home of ProgramY")
        self.assertEquals(len(card1['buttons']), 1)

        button1 = card1['buttons'][0]
        self.assertEquals("button", button1['type'])
        self.assertEquals(button1['text'], "Hello")
        self.assertEquals(button1['url'], "http://click.me")

    def test_reply_with_postback(self):
        mock_config = unittest.mock.Mock()
        renderer = MockRichMediaRenderer(mock_config)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", """
            <reply>
                <text>Hello</text>
                <postback>HELLO</postback>
            </reply>""")

        self.assertEquals(renderer._userid, "testuser")
        self.assertIsNotNone(renderer._reply)
        self.assertEquals("reply", renderer._reply['type'])
        self.assertEquals(renderer._reply['text'], "Hello")
        self.assertEquals(renderer._reply['postback'], "HELLO")

    def test_reply_without_postback(self):
        mock_config = unittest.mock.Mock()
        renderer = MockRichMediaRenderer(mock_config)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", """
            <reply>
                <text>Hello</text>
            </reply>""")

        self.assertEquals(renderer._userid, "testuser")
        self.assertIsNotNone(renderer._reply)
        self.assertEquals("reply", renderer._reply['type'])
        self.assertEquals(renderer._reply['text'], "Hello")
        self.assertIsNone(renderer._reply['postback'])

    def test_delay(self):
        mock_config = unittest.mock.Mock()
        renderer = MockRichMediaRenderer(mock_config)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", """
            <delay>
                <seconds>10</seconds>
            </delay>""")

        self.assertEquals(renderer._userid, "testuser")
        self.assertIsNotNone(renderer._delay)
        self.assertEquals("delay", renderer._delay['type'])
        self.assertEquals(renderer._delay['seconds'], "10")

    def test_split(self):
        mock_config = unittest.mock.Mock()
        renderer = MockRichMediaRenderer(mock_config)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", "<split />")

        self.assertEquals(renderer._userid, "testuser")

    def test_list_with_text_only(self):
        mock_config = unittest.mock.Mock()
        renderer = MockRichMediaRenderer(mock_config)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", """
            <list>
                <item>Item1</item>
                <item>Item2</item>
            </list>""")

        self.assertEquals(renderer._userid, "testuser")
        self.assertIsNotNone(renderer._list)
        self.assertEquals("list", renderer._list['type'])
        self.assertEquals(2, len(renderer._list['items']))

        item1 = renderer._list['items'][0]
        self.assertEquals("text", item1['type'])
        self.assertEquals("Item1", item1['text'])

        item2 = renderer._list['items'][1]
        self.assertEquals("text", item2['type'])
        self.assertEquals("Item2", item2['text'])

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
        self.assertIsNotNone(renderer._list)
        self.assertEquals("list", renderer._list['type'])
        self.assertEquals(2, len(renderer._list['items']))

        item1 = renderer._list['items'][0]
        self.assertEquals("list", item1['type'])
        self.assertEquals(2, len(item1['items']))
        item1_1 = item1['items'][0]
        self.assertEquals("text", item1_1['type'])
        self.assertEquals("Item1.1", item1_1['text'])
        item1_2 = item1['items'][1]
        self.assertEquals("text", item1_2['type'])
        self.assertEquals("Item1.2", item1_2['text'])

        item2 = renderer._list['items'][1]
        self.assertEquals("text", item2['type'])
        self.assertEquals("Item2", item2['text'])

    def test_olist(self):
        mock_config = unittest.mock.Mock()
        renderer = MockRichMediaRenderer(mock_config)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", """
             <list>
                <item>Item1</item>
                <item>Item2</item>
            </list>""")

        self.assertIsNotNone(renderer._list)
        self.assertEquals("list", renderer._list['type'])
        self.assertEquals(2, len(renderer._list['items']))

        item1 = renderer._list['items'][0]
        self.assertEquals("text", item1['type'])
        self.assertEquals("Item1", item1['text'])

        item2 = renderer._list['items'][1]
        self.assertEquals("text", item2['type'])
        self.assertEquals("Item2", item2['text'])

    def test_location(self):
        mock_config = unittest.mock.Mock()
        renderer = MockRichMediaRenderer(mock_config)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", "<location />")

        self.assertEquals(renderer._userid, "testuser")

