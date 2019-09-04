import unittest
import unittest.mock

from programy.clients.render.renderer import RichMediaRenderer


class MockRichMediaRenderer(RichMediaRenderer):

    def __init__(self, config):
        RichMediaRenderer.__init__(self, config)

    def handle_text(self, userid, text):
        self._userid = userid
        self._text = text
        return None

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

    def handle_tts(self, userid, text):
        self._userid = userid
        self._text = text
        return None


class OpenChatBotRichMediaRendererTests(unittest.TestCase):

    def test_card(self):
        mock_config = unittest.mock.Mock()
        renderer = MockRichMediaRenderer(mock_config)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", """
			<card>
				<image>https://www.ikea.com/fr/fr/images/products/strandmon-fauteuil-enfant-gris__0574584_PE668407_S4.JPG</image>
				<title>Fauteuil enfant, Visslegris</title>
				<subtitle>Quand ils peuvent imiter les adultes, les enfants sesentent spéciaux et importants. C'est pourquoi nous avons créé une version miniature du fauteuil STRANDMON, l'un de nos produits favoris.</subtitle>
				<button>
					<text>Acheter en ligne</text>
					<url>https://serv-api.target2sell.com/1.1/R/cookie/OFCBMN5RRHSG5L/1200/OFCBMN5RRHSG5L-1200-5/20343224/1/viewTogether-%7BtypeOfContextList%3A%5B%22current%22%2C%22view%22%5D%7D/f082e51f-561d-47f7-c0cb-13735e58bfc1</url>
				</button>
            </card>""")

        self.assertEqual(renderer._userid, "testuser")
        self.assertIsNotNone(renderer._card)
        self.assertEqual("card", renderer._card['type'])
        self.assertEqual(renderer._card['image'], "https://www.ikea.com/fr/fr/images/products/strandmon-fauteuil-enfant-gris__0574584_PE668407_S4.JPG")
        self.assertEqual(renderer._card['title'], "Fauteuil enfant, Visslegris")
        self.assertEqual(renderer._card['subtitle'], "Quand ils peuvent imiter les adultes, les enfants sesentent spéciaux et importants. C'est pourquoi nous avons créé une version miniature du fauteuil STRANDMON, l'un de nos produits favoris.")
        self.assertEqual(len(renderer._card['buttons']), 1)

        button1 = renderer._card['buttons'][0]
        self.assertEqual("button", button1['type'])
        self.assertEqual(button1['text'], "Acheter en ligne")
        self.assertEqual(button1['url'], "https://serv-api.target2sell.com/1.1/R/cookie/OFCBMN5RRHSG5L/1200/OFCBMN5RRHSG5L-1200-5/20343224/1/viewTogether-%7BtypeOfContextList%3A%5B%22current%22%2C%22view%22%5D%7D/f082e51f-561d-47f7-c0cb-13735e58bfc1")
