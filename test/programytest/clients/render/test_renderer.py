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

        self.assertEqual(renderer._userid, "testuser")
        self.assertIsNotNone(renderer._text)
        self.assertEqual("text", renderer._text['type'])
        self.assertEqual("Hello world", renderer._text['text'])

    def test_xml_html(self):
        mock_config = unittest.mock.Mock()
        renderer = MockRichMediaRenderer(mock_config)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", """
            <ul>
                <li>item1</li>
                <li>item2</li>
            </ul>""")

        self.assertEqual(renderer._userid, "testuser")
        self.assertIsNotNone(renderer._text)
        self.assertEqual("text", renderer._text['type'])
        self.assertEqual("<ul>\n<li>item1</li>\n<li>item2</li>\n</ul>", renderer._text['text'])

    def test_url_button(self):
        mock_config = unittest.mock.Mock()
        renderer = MockRichMediaRenderer(mock_config)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", """
            <button>
                <text>Hello</text>
                <url>http://click.me</url>
            </button>""")

        self.assertEqual(renderer._userid, "testuser")
        self.assertIsNotNone(renderer._button)
        self.assertEqual("button", renderer._button['type'])
        self.assertEqual(renderer._button['text'], "Hello")
        self.assertEqual(renderer._button['url'], "http://click.me")

    def test_postback_button(self):
        mock_config = unittest.mock.Mock()
        renderer = MockRichMediaRenderer(mock_config)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", """
            <button>
                <text>Hello</text>
                <postback>HELLO</url></postback>
            </button>""")

        self.assertEqual(renderer._userid, "testuser")
        self.assertIsNotNone(renderer._button)
        self.assertEqual("button", renderer._button['type'])
        self.assertEqual(renderer._button['text'], "Hello")
        self.assertEqual(renderer._button['postback'], "HELLO")

    def test_link(self):
        mock_config = unittest.mock.Mock()
        renderer = MockRichMediaRenderer(mock_config)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", """
            <link>
                <text>Hello</text>
                <url>http://click.me</url>
            </link>""")

        self.assertEqual(renderer._userid, "testuser")
        self.assertIsNotNone(renderer._link)
        self.assertEqual("link", renderer._link['type'])
        self.assertEqual(renderer._link['text'], "Hello")
        self.assertEqual(renderer._link['url'], "http://click.me")

    def test_image(self):
        mock_config = unittest.mock.Mock()
        renderer = MockRichMediaRenderer(mock_config)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", """
            <image>
                http://servusai.com/aiml.png
            </image>""")

        self.assertEqual(renderer._userid, "testuser")
        self.assertIsNotNone(renderer._image)
        self.assertEqual("image", renderer._image['type'])
        self.assertEqual(renderer._image['url'], "http://servusai.com/aiml.png")

    def test_video(self):
        mock_config = unittest.mock.Mock()
        renderer = MockRichMediaRenderer(mock_config)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", """
            <video>
                http://servusai.com/aiml.mov
            </video>""")

        self.assertEqual(renderer._userid, "testuser")
        self.assertIsNotNone(renderer._video)
        self.assertEqual("video", renderer._video['type'])
        self.assertEqual(renderer._video['url'], "http://servusai.com/aiml.mov")

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

        self.assertEqual(renderer._userid, "testuser")
        self.assertIsNotNone(renderer._card)
        self.assertEqual("card", renderer._card['type'])
        self.assertEqual(renderer._card['image'], "http://servusai.com/aiml.png")
        self.assertEqual(renderer._card['title'], "Servusai")
        self.assertEqual(renderer._card['subtitle'], "Home of ProgramY")
        self.assertEqual(len(renderer._card['buttons']), 1)

        button1 = renderer._card['buttons'][0]
        self.assertEqual("button", button1['type'])
        self.assertEqual(button1['text'], "Hello")
        self.assertEqual(button1['url'], "http://click.me")

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

        self.assertEqual(renderer._userid, "testuser")
        self.assertIsNotNone(renderer._carousel)
        self.assertEqual("carousel", renderer._carousel['type'])
        self.assertEqual(1, len(renderer._carousel['cards']))

        card1 = renderer._carousel['cards'][0]
        self.assertEqual(card1['image'], "http://servusai.com/aiml.png")
        self.assertEqual(card1['title'], "Servusai")
        self.assertEqual(card1['subtitle'], "Home of ProgramY")
        self.assertEqual(len(card1['buttons']), 1)

        button1 = card1['buttons'][0]
        self.assertEqual("button", button1['type'])
        self.assertEqual(button1['text'], "Hello")
        self.assertEqual(button1['url'], "http://click.me")

    def test_reply_with_postback(self):
        mock_config = unittest.mock.Mock()
        renderer = MockRichMediaRenderer(mock_config)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", """
            <reply>
                <text>Hello</text>
                <postback>HELLO</postback>
            </reply>""")

        self.assertEqual(renderer._userid, "testuser")
        self.assertIsNotNone(renderer._reply)
        self.assertEqual("reply", renderer._reply['type'])
        self.assertEqual(renderer._reply['text'], "Hello")
        self.assertEqual(renderer._reply['postback'], "HELLO")

    def test_reply_without_postback(self):
        mock_config = unittest.mock.Mock()
        renderer = MockRichMediaRenderer(mock_config)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", """
            <reply>
                <text>Hello</text>
            </reply>""")

        self.assertEqual(renderer._userid, "testuser")
        self.assertIsNotNone(renderer._reply)
        self.assertEqual("reply", renderer._reply['type'])
        self.assertEqual(renderer._reply['text'], "Hello")
        self.assertIsNone(renderer._reply['postback'])

    def test_delay(self):
        mock_config = unittest.mock.Mock()
        renderer = MockRichMediaRenderer(mock_config)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", """
            <delay>
                <seconds>10</seconds>
            </delay>""")

        self.assertEqual(renderer._userid, "testuser")
        self.assertIsNotNone(renderer._delay)
        self.assertEqual("delay", renderer._delay['type'])
        self.assertEqual(renderer._delay['seconds'], "10")

    def test_split(self):
        mock_config = unittest.mock.Mock()
        renderer = MockRichMediaRenderer(mock_config)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", "<split />")

        self.assertEqual(renderer._userid, "testuser")

    def test_list_with_text_only(self):
        mock_config = unittest.mock.Mock()
        renderer = MockRichMediaRenderer(mock_config)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", """
            <list>
                <item>Item1</item>
                <item>Item2</item>
            </list>""")

        self.assertEqual(renderer._userid, "testuser")
        self.assertIsNotNone(renderer._list)
        self.assertEqual("list", renderer._list['type'])
        self.assertEqual(2, len(renderer._list['items']))

        item1 = renderer._list['items'][0]
        self.assertEqual("text", item1['type'])
        self.assertEqual("Item1", item1['text'])

        item2 = renderer._list['items'][1]
        self.assertEqual("text", item2['type'])
        self.assertEqual("Item2", item2['text'])

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

        self.assertEqual(renderer._userid, "testuser")
        self.assertIsNotNone(renderer._list)
        self.assertEqual("list", renderer._list['type'])
        self.assertEqual(2, len(renderer._list['items']))

        item1 = renderer._list['items'][0]
        self.assertEqual("list", item1['type'])
        self.assertEqual(2, len(item1['items']))
        item1_1 = item1['items'][0]
        self.assertEqual("text", item1_1['type'])
        self.assertEqual("Item1.1", item1_1['text'])
        item1_2 = item1['items'][1]
        self.assertEqual("text", item1_2['type'])
        self.assertEqual("Item1.2", item1_2['text'])

        item2 = renderer._list['items'][1]
        self.assertEqual("text", item2['type'])
        self.assertEqual("Item2", item2['text'])

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
        self.assertEqual("list", renderer._list['type'])
        self.assertEqual(2, len(renderer._list['items']))

        item1 = renderer._list['items'][0]
        self.assertEqual("text", item1['type'])
        self.assertEqual("Item1", item1['text'])

        item2 = renderer._list['items'][1]
        self.assertEqual("text", item2['type'])
        self.assertEqual("Item2", item2['text'])

    def test_location(self):
        mock_config = unittest.mock.Mock()
        renderer = MockRichMediaRenderer(mock_config)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", "<location />")

        self.assertEqual(renderer._userid, "testuser")

