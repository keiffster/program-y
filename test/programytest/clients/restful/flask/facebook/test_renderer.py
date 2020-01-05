import unittest

from programy.clients.restful.flask.facebook.client import FacebookBotClient
from programy.clients.restful.flask.facebook.renderer import FacebookRenderer
from programytest.clients.arguments import MockArgumentParser


class MockFacebookRenderer(FacebookRenderer):

    def __init__(self, client):
        FacebookRenderer.__init__(self, client)
        self._payload = None

    def send_payload(self, payload):
        self._payload = payload


class MockFacebookBotClient(FacebookBotClient):

    def __init__(self, argument_parser=None):
        FacebookBotClient.__init__(self, argument_parser)

    def get_license_keys(self):
        self._access_token = "FACEBOOK_ACCESS_TOKEN"
        self._verify_token = "FACEBOOK_VERIFY_TOKEN"


class FacebookRendererTests(unittest.TestCase):

    def setUp(self):
        arguments = MockArgumentParser()
        client = MockFacebookBotClient(arguments)
        self.renderer = MockFacebookRenderer(client)
        self.assertIsNone(self.renderer._payload)
        self.client_context = client.create_client_context("testid")

    def test_handle_text(self):
        text = {
            'type': 'text', 'text': "Hello"
        }
        self.renderer.handle_text(self.client_context, text)
        self.assertIsNotNone(self.renderer._payload)
        self.assertEqual("testid", self.renderer._payload['recipient']['id'])
        self.assertEqual("Hello", self.renderer._payload['message']['text'])

    def test_handle_url_button(self):
        button = {
            "type": "button", "text": "Servusai", "url": "https://www.servusai.com"
        }
        self.renderer.handle_url_button(self.client_context, button)
        self.assertIsNotNone(self.renderer._payload)
        self.assertEqual("testid", self.renderer._payload['recipient']['id'])
        self.assertEqual("template", self.renderer._payload['message']['attachment']['type'])
        self.assertEqual("button", self.renderer._payload['message']['attachment']['payload']['template_type'])
        self.assertEqual("Servusai", self.renderer._payload['message']['attachment']['payload']['text'])
        self.assertEqual(1, len(self.renderer._payload['message']['attachment']['payload']['buttons']))
        self.assertEqual("web_url", self.renderer._payload['message']['attachment']['payload']['buttons'][0]["type"])
        self.assertEqual("https://www.servusai.com", self.renderer._payload['message']['attachment']['payload']['buttons'][0]["url"])
        self.assertEqual("Servusai", self.renderer._payload['message']['attachment']['payload']['buttons'][0]["title"])

    def test_handle_postback_button(self):
        button = {
            "type": "button", "text": "Servusai", "postback": "Servusai"
        }
        self.renderer.handle_postback_button(self.client_context, button)
        self.assertIsNotNone(self.renderer._payload)
        self.assertEqual("testid", self.renderer._payload['recipient']['id'])
        self.assertEqual("template", self.renderer._payload['message']['attachment']['type'])
        self.assertEqual("button", self.renderer._payload['message']['attachment']['payload']['template_type'])
        self.assertEqual("Servusai", self.renderer._payload['message']['attachment']['payload']['text'])
        self.assertEqual(1, len(self.renderer._payload['message']['attachment']['payload']['buttons']))
        self.assertEqual("postback", self.renderer._payload['message']['attachment']['payload']['buttons'][0]["type"])
        self.assertEqual("Servusai", self.renderer._payload['message']['attachment']['payload']['buttons'][0]["payload"])
        self.assertEqual("Servusai", self.renderer._payload['message']['attachment']['payload']['buttons'][0]["title"])

    def test_handle_link(self):
        link = {
            "type": "link", "text": "Servusai", "url": "https://www.servusai.com"
        }
        self.renderer.handle_link(self.client_context, link)
        self.assertIsNotNone(self.renderer._payload)
        self.assertEqual("testid", self.renderer._payload['recipient']['id'])
        self.assertEqual("template", self.renderer._payload['message']['attachment']['type'])
        self.assertEqual("button", self.renderer._payload['message']['attachment']['payload']['template_type'])
        self.assertEqual("Servusai", self.renderer._payload['message']['attachment']['payload']['text'])
        self.assertEqual(1, len(self.renderer._payload['message']['attachment']['payload']['buttons']))
        self.assertEqual("web_url", self.renderer._payload['message']['attachment']['payload']['buttons'][0]["type"])
        self.assertEqual("https://www.servusai.com", self.renderer._payload['message']['attachment']['payload']['buttons'][0]["url"])
        self.assertEqual("Servusai", self.renderer._payload['message']['attachment']['payload']['buttons'][0]["title"])

    def test_handle_image(self):
        image = {
            "type": "image", "url": "https://www.servusai.com/test.png"
        }
        self.renderer.handle_image(self.client_context, image)
        self.assertIsNotNone(self.renderer._payload)
        self.assertEqual("testid", self.renderer._payload['recipient']['id'])
        self.assertEqual("template", self.renderer._payload['message']['attachment']['type'])
        self.assertEqual("media", self.renderer._payload['message']['attachment']['payload']['template_type'])
        self.assertEqual("image", self.renderer._payload['message']['attachment']['payload']['elements'][0]['media_type'])
        self.assertEqual("https://www.servusai.com/test.png", self.renderer._payload['message']['attachment']['payload']['elements'][0]['url'])

    def test_handle_video(self):
        video = {
            "type": "image", "url": "https://www.servusai.com/test.mov"
        }
        self.renderer.handle_video(self.client_context, video)
        self.assertIsNotNone(self.renderer._payload)
        self.assertEqual("testid", self.renderer._payload['recipient']['id'])
        self.assertEqual("template", self.renderer._payload['message']['attachment']['type'])
        self.assertEqual("media", self.renderer._payload['message']['attachment']['payload']['template_type'])
        self.assertEqual("video", self.renderer._payload['message']['attachment']['payload']['elements'][0]['media_type'])
        self.assertEqual("https://www.servusai.com/test.mov", self.renderer._payload['message']['attachment']['payload']['elements'][0]['url'])

    def test_handle_card(self):
        card = {
            "type": "card",
            "image": "http://www.servusai.com/test.png",
            "title": "Servusai.com",
            "subtitle": "The home of Program-Y",
            "buttons": [
                {"type": "button", "text": "Servusai", "url": "http://www.servusai.com"},
                {"type": "button", "text": "AIML Foundation", "url": "http://www.aiml.foundation"}
            ]
        }
        self.renderer.handle_card(self.client_context, card)
        self.assertIsNotNone(self.renderer._payload)
        self.assertEqual("testid", self.renderer._payload['recipient']['id'])
        message = self.renderer._payload['message']
        self.assertIsNotNone(message['attachment'])
        attachment = message['attachment']
        self.assertEqual("template", attachment['type'])
        self.assertIsNotNone(attachment['payload'])
        payload = attachment['payload']
        self.assertEqual("generic", payload["template_type"])
        self.assertIsNotNone(payload['elements'])
        elements = payload['elements']
        self.assertEqual(1, len(elements))
        element1 = elements[0]
        self.assertEqual("Servusai.com", element1["title"])
        self.assertEqual("The home of Program-Y", element1["subtitle"])
        self.assertEqual("http://www.servusai.com/test.png", element1["image_url"])
        self.assertIsNotNone(element1["buttons"])
        buttons = element1["buttons"]
        self.assertEqual(2, len(buttons))
        button1 = buttons[0]
        self.assertEqual("web_url", button1["type"])
        self.assertEqual("Servusai", button1["title"])
        self.assertEqual("http://www.servusai.com", button1["url"])
        button2 = buttons[1]
        self.assertEqual("web_url", button2["type"])
        self.assertEqual("AIML Foundation", button2["title"])
        self.assertEqual("http://www.aiml.foundation", button2["url"])

    def test_handle_carousel(self):
        carousel = {
            "type": "carousel",
            "cards": [
                {
                    "type": "card",
                    "image": "https://www.servusai.com/test.png",
                    "title": "Servusai.com",
                    "subtitle": "The home of Program-Y",
                    "buttons": [
                        {"type": "button", "text": "Servusai", "url": "httpw://www.servusai.com"}
                    ]
                },
                {
                    "type": "card",
                    "image": "https://aiml.foundation/test.png",
                    "title": "AIML Foundation",
                    "subtitle": "The home of AIML",
                    "buttons": [
                        {"type": "button", "text": "AIML Foundation", "url": "httpw://aiml.foundation"}
                    ]
                }
            ]
        }

        self.renderer.handle_carousel(self.client_context, carousel)
        self.assertIsNotNone(self.renderer._payload)
        self.assertEqual("testid", self.renderer._payload['recipient']['id'])
        message = self.renderer._payload['message']
        self.assertIsNotNone(message['attachment'])
        attachment = message['attachment']
        self.assertEqual("template", attachment['type'])
        self.assertIsNotNone(attachment['payload'])
        payload = attachment['payload']
        self.assertEqual("generic", payload["template_type"])
        self.assertIsNotNone(payload['elements'])
        elements = payload['elements']
        self.assertEqual(2, len(elements))

        element1 = elements[0]
        self.assertEqual("Servusai.com", element1["title"])
        self.assertEqual("The home of Program-Y", element1["subtitle"])
        self.assertEqual("https://www.servusai.com/test.png", element1["image_url"])
        self.assertIsNotNone(element1["buttons"])
        buttons = element1["buttons"]
        self.assertEqual(1, len(buttons))
        button1 = buttons[0]
        self.assertEqual("web_url", button1["type"])
        self.assertEqual("Servusai", button1["title"])
        self.assertEqual("httpw://www.servusai.com", button1["url"])

        element2 = elements[1]
        self.assertEqual("AIML Foundation", element2["title"])
        self.assertEqual("The home of AIML", element2["subtitle"])
        self.assertEqual("https://aiml.foundation/test.png", element2["image_url"])
        self.assertIsNotNone(element2["buttons"])
        buttons = element2["buttons"]
        self.assertEqual(1, len(buttons))
        button1 = buttons[0]
        self.assertEqual("web_url", button1["type"])
        self.assertEqual("AIML Foundation", button1["title"])
        self.assertEqual("httpw://aiml.foundation", button1["url"])

    def test_handle_reply(self):
        reply = {
            "type": "reply",
            "text": "Servusai",
            "postback": None
        }
        self.renderer.handle_reply(self.client_context, reply)
        self.assertIsNotNone(self.renderer._payload)
        self.assertEqual("testid", self.renderer._payload['recipient']['id'])
        self.assertEqual("template", self.renderer._payload['message']['attachment']['type'])
        self.assertEqual("button", self.renderer._payload['message']['attachment']['payload']['template_type'])
        self.assertEqual("Servusai", self.renderer._payload['message']['attachment']['payload']['text'])
        self.assertEqual(1, len(self.renderer._payload['message']['attachment']['payload']['buttons']))
        self.assertEqual("postback", self.renderer._payload['message']['attachment']['payload']['buttons'][0]["type"])
        self.assertEqual("Servusai", self.renderer._payload['message']['attachment']['payload']['buttons'][0]["payload"])
        self.assertEqual("Servusai", self.renderer._payload['message']['attachment']['payload']['buttons'][0]["title"])

    def test_handle_postback_reply(self):
        reply = {
            "type": "reply",
            "text": "Servusai",
            "postback": "SERVUSAI"
        }
        self.renderer.handle_reply(self.client_context, reply)
        self.assertIsNotNone(self.renderer._payload)
        self.assertEqual("testid", self.renderer._payload['recipient']['id'])
        self.assertEqual("template", self.renderer._payload['message']['attachment']['type'])
        self.assertEqual("button", self.renderer._payload['message']['attachment']['payload']['template_type'])
        self.assertEqual("Servusai", self.renderer._payload['message']['attachment']['payload']['text'])
        self.assertEqual(1, len(self.renderer._payload['message']['attachment']['payload']['buttons']))
        self.assertEqual("postback", self.renderer._payload['message']['attachment']['payload']['buttons'][0]["type"])
        self.assertEqual("SERVUSAI", self.renderer._payload['message']['attachment']['payload']['buttons'][0]["payload"])
        self.assertEqual("Servusai", self.renderer._payload['message']['attachment']['payload']['buttons'][0]["title"])

    def test_handle_delay(self):
        delay = {
            "type": "delay",
            "seconds": "0"
        }
        self.renderer.handle_delay(self.client_context, delay)
        self.assertIsNotNone(self.renderer._payload)
        self.assertEqual("testid", self.renderer._payload['recipient']['id'])
        self.assertEqual("typing_off", self.renderer._payload['sender_action'])

    def test_handle_split(self):
        split = {
            "type": "split"
        }
        self.renderer.handle_split(self.client_context, split)
        self.assertIsNone(self.renderer._payload)

    def test_handle_list(self):
        list = {
            'type': 'list',
            'items': [
                {'type': 'card', 'image': "https://www.servusai.com/test.png", 'title':"Servusai", "subtitle": "The home of Program-Y", "buttons": [
                    {"type": "button", "text": "Servusai", "url": "https://www.servusai.com", "postback": None}
                ]}
            ]
        }

        self.renderer.handle_list(self.client_context, list)
        self.assertIsNotNone(self.renderer._payload)
        self.assertEqual("testid", self.renderer._payload['recipient']['id'])
        message = self.renderer._payload['message']
        self.assertIsNotNone(message['attachment'])
        attachment = message['attachment']
        self.assertEqual("template", attachment['type'])
        self.assertIsNotNone(attachment['payload'])
        payload = attachment['payload']
        self.assertEqual("list", payload["template_type"])
        self.assertIsNotNone(payload['elements'])
        elements = payload['elements']
        self.assertEqual(1, len(elements))
        element1 = elements[0]
        self.assertEqual("Servusai", element1['title'])
        self.assertEqual("The home of Program-Y", element1['subtitle'])
        self.assertEqual("https://www.servusai.com/test.png", element1['image_url'])
        self.assertEqual(1, len(element1['buttons']))
        button1 = element1['buttons'][0]
        self.assertEqual("Servusai", button1['title'])
        self.assertEqual("web_url", button1['type'])
        self.assertEqual("https://www.servusai.com", button1['url'])

    def test_handle_ordered_list(self):
        list = {
            'type': 'list',
            'items': [
                {'type': 'card', 'image': "https://www.servusai.com/test.png", 'title':"Servusai", "subtitle": "The home of Program-Y", "buttons": [
                    {"type": "button", "text": "Servusai", "url": "https://www.servusai.com", "postback": None}
                ]}
            ]
        }

        self.renderer.handle_ordered_list(self.client_context, list)
        self.assertIsNotNone(self.renderer._payload)
        self.assertEqual("testid", self.renderer._payload['recipient']['id'])
        message = self.renderer._payload['message']
        self.assertIsNotNone(message['attachment'])
        attachment = message['attachment']
        self.assertEqual("template", attachment['type'])
        self.assertIsNotNone(attachment['payload'])
        payload = attachment['payload']
        self.assertEqual("list", payload["template_type"])
        self.assertIsNotNone(payload['elements'])
        elements = payload['elements']
        self.assertEqual(1, len(elements))
        element1 = elements[0]
        self.assertEqual("Servusai", element1['title'])
        self.assertEqual("The home of Program-Y", element1['subtitle'])
        self.assertEqual("https://www.servusai.com/test.png", element1['image_url'])
        self.assertEqual(1, len(element1['buttons']))
        button1 = element1['buttons'][0]
        self.assertEqual("Servusai", button1['title'])
        self.assertEqual("web_url", button1['type'])
        self.assertEqual("https://www.servusai.com", button1['url'])

    def test_render_payload(self):
        pass

    def test_handle_location(self):
        location = {
            "type": "location"
        }
        self.renderer.handle_location(self.client_context, location)
        self.assertIsNotNone(self.renderer._payload)
        self.assertEqual("testid", self.renderer._payload['recipient']['id'])
        self.assertEqual("Your location", self.renderer._payload['message']['text'])
        self.assertEqual("location", self.renderer._payload['message']['quick_replies'][0]['content_type'])

