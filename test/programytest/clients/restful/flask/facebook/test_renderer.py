import unittest

from programy.clients.restful.flask.facebook.renderer import FacebookRenderer
from programy.clients.restful.flask.facebook.client import FacebookBotClient
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
        self.renderer.handle_text(self.client_context, "Hello")
        self.assertIsNotNone(self.renderer._payload)
        self.assertEquals("testid", self.renderer._payload['recipient']['id'])
        self.assertEquals("Hello", self.renderer._payload['message']['text'])

    def test_handle_url_button(self):
        self.renderer.handle_url_button(self.client_context, "Servusai", "https://www.servusai.com")
        self.assertIsNotNone(self.renderer._payload)
        self.assertEquals("testid", self.renderer._payload['recipient']['id'])
        self.assertEquals("template", self.renderer._payload['message']['attachment']['type'])
        self.assertEquals("button", self.renderer._payload['message']['attachment']['payload']['template_type'])
        self.assertEquals("Servusai", self.renderer._payload['message']['attachment']['payload']['text'])
        self.assertEquals(1, len(self.renderer._payload['message']['attachment']['payload']['buttons']))
        self.assertEquals("web_url", self.renderer._payload['message']['attachment']['payload']['buttons'][0]["type"])
        self.assertEquals("https://www.servusai.com", self.renderer._payload['message']['attachment']['payload']['buttons'][0]["url"])
        self.assertEquals("Servusai", self.renderer._payload['message']['attachment']['payload']['buttons'][0]["title"])

    def test_handle_postback_button(self):
        self.renderer.handle_postback_button(self.client_context, "Servusai", "Servusai")
        self.assertIsNotNone(self.renderer._payload)
        self.assertEquals("testid", self.renderer._payload['recipient']['id'])
        self.assertEquals("template", self.renderer._payload['message']['attachment']['type'])
        self.assertEquals("button", self.renderer._payload['message']['attachment']['payload']['template_type'])
        self.assertEquals("Servusai", self.renderer._payload['message']['attachment']['payload']['text'])
        self.assertEquals(1, len(self.renderer._payload['message']['attachment']['payload']['buttons']))
        self.assertEquals("postback", self.renderer._payload['message']['attachment']['payload']['buttons'][0]["type"])
        self.assertEquals("Servusai", self.renderer._payload['message']['attachment']['payload']['buttons'][0]["payload"])
        self.assertEquals("Servusai", self.renderer._payload['message']['attachment']['payload']['buttons'][0]["title"])

    def test_handle_link(self):
        self.renderer.handle_link(self.client_context, "Servusai", "https://www.servusai.com")
        self.assertIsNotNone(self.renderer._payload)
        self.assertEquals("testid", self.renderer._payload['recipient']['id'])
        self.assertEquals("template", self.renderer._payload['message']['attachment']['type'])
        self.assertEquals("button", self.renderer._payload['message']['attachment']['payload']['template_type'])
        self.assertEquals("Servusai", self.renderer._payload['message']['attachment']['payload']['text'])
        self.assertEquals(1, len(self.renderer._payload['message']['attachment']['payload']['buttons']))
        self.assertEquals("web_url", self.renderer._payload['message']['attachment']['payload']['buttons'][0]["type"])
        self.assertEquals("https://www.servusai.com", self.renderer._payload['message']['attachment']['payload']['buttons'][0]["url"])
        self.assertEquals("Servusai", self.renderer._payload['message']['attachment']['payload']['buttons'][0]["title"])

    def test_handle_image(self):
        self.renderer.handle_image(self.client_context, "https://www.servusai.com/test.png")
        self.assertIsNotNone(self.renderer._payload)
        self.assertEquals("testid", self.renderer._payload['recipient']['id'])
        self.assertEquals("template", self.renderer._payload['message']['attachment']['type'])
        self.assertEquals("media", self.renderer._payload['message']['attachment']['payload']['template_type'])
        self.assertEquals("image", self.renderer._payload['message']['attachment']['payload']['elements'][0]['media_type'])
        self.assertEquals("https://www.servusai.com/test.png", self.renderer._payload['message']['attachment']['payload']['elements'][0]['url'])

    def test_handle_video(self):
        self.renderer.handle_video(self.client_context, "https://www.servusai.com/test.mov")
        self.assertIsNotNone(self.renderer._payload)
        self.assertEquals("testid", self.renderer._payload['recipient']['id'])
        self.assertEquals("template", self.renderer._payload['message']['attachment']['type'])
        self.assertEquals("media", self.renderer._payload['message']['attachment']['payload']['template_type'])
        self.assertEquals("video", self.renderer._payload['message']['attachment']['payload']['elements'][0]['media_type'])
        self.assertEquals("https://www.servusai.com/test.mov", self.renderer._payload['message']['attachment']['payload']['elements'][0]['url'])

    def test_handle_card(self):
        buttons = [
            ("Servusai", "https://www.servusai.com", None),
            ("AIML Foundation", "https://aiml.foundation", None)
        ]
        self.renderer.handle_card(self.client_context, "https://www.servusai.com/test.png", "Servusai.com", "The home of Program-Y", buttons)
        self.assertIsNotNone(self.renderer._payload)
        self.assertEquals("testid", self.renderer._payload['recipient']['id'])
        message = self.renderer._payload['message']
        self.assertIsNotNone(message['attachment'])
        attachment = message['attachment']
        self.assertEquals("template", attachment['type'])
        self.assertIsNotNone(attachment['payload'])
        payload = attachment['payload']
        self.assertEquals("generic", payload["template_type"])
        self.assertIsNotNone(payload['elements'])
        elements = payload['elements']
        self.assertEquals(1, len(elements))
        element1 = elements[0]
        self.assertEquals("Servusai.com", element1["title"])
        self.assertEquals("The home of Program-Y", element1["subtitle"])
        self.assertEquals("https://www.servusai.com/test.png", element1["image_url"])
        self.assertIsNotNone(element1["buttons"])
        buttons = element1["buttons"]
        self.assertEquals(2, len(buttons))
        button1 = buttons[0]
        self.assertEquals("web_url", button1["type"])
        self.assertEquals("Servusai", button1["title"])
        self.assertEquals("https://www.servusai.com", button1["url"])
        button2 = buttons[1]
        self.assertEquals("web_url", button2["type"])
        self.assertEquals("AIML Foundation", button2["title"])
        self.assertEquals("https://aiml.foundation", button2["url"])

    def test_handle_carousel(self):
        buttons1 = [
            ("Servusai", "https://www.servusai.com", None),
            ("About", "https://www.servusai.com/about", None),
            ("Contact", "https://www.servusai.com/contactus", None)
        ]
        buttons2 = [
            ("AIML Foundation", "https://aiml.foundation", None),
            ("About", "https://aiml.foundation/about", None),
            ("Contact", "https://aiml.foundation/contactus", None)
        ]
        cards = [
            ("https://www.servusai.com/test.png", "Servusai", "The home of Program-Y", buttons1),
            ("https://aiml.foundation/test.png", "AIML Foundation", "The home of AIML", buttons2)
        ]

        self.renderer.handle_carousel(self.client_context, cards)
        self.assertIsNotNone(self.renderer._payload)
        self.assertEquals("testid", self.renderer._payload['recipient']['id'])
        message = self.renderer._payload['message']
        self.assertIsNotNone(message['attachment'])
        attachment = message['attachment']
        self.assertEquals("template", attachment['type'])
        self.assertIsNotNone(attachment['payload'])
        payload = attachment['payload']
        self.assertEquals("generic", payload["template_type"])
        self.assertIsNotNone(payload['elements'])
        elements = payload['elements']
        self.assertEquals(2, len(elements))

        element1 = elements[0]
        self.assertEquals("Servusai", element1["title"])
        self.assertEquals("The home of Program-Y", element1["subtitle"])
        self.assertEquals("https://www.servusai.com/test.png", element1["image_url"])
        self.assertIsNotNone(element1["buttons"])
        buttons = element1["buttons"]
        self.assertEquals(3, len(buttons))
        button1 = buttons[0]
        self.assertEquals("web_url", button1["type"])
        self.assertEquals("Servusai", button1["title"])
        self.assertEquals("https://www.servusai.com", button1["url"])
        button2 = buttons[1]
        self.assertEquals("web_url", button2["type"])
        self.assertEquals("About", button2["title"])
        self.assertEquals("https://www.servusai.com/about", button2["url"])
        button3 = buttons[2]
        self.assertEquals("web_url", button3["type"])
        self.assertEquals("Contact", button3["title"])
        self.assertEquals("https://www.servusai.com/contactus", button3["url"])

        element2 = elements[1]
        self.assertEquals("AIML Foundation", element2["title"])
        self.assertEquals("The home of AIML", element2["subtitle"])
        self.assertEquals("https://aiml.foundation/test.png", element2["image_url"])
        self.assertIsNotNone(element2["buttons"])
        buttons = element2["buttons"]
        self.assertEquals(3, len(buttons))
        button1 = buttons[0]
        self.assertEquals("web_url", button1["type"])
        self.assertEquals("AIML Foundation", button1["title"])
        self.assertEquals("https://aiml.foundation", button1["url"])
        button2 = buttons[1]
        self.assertEquals("web_url", button2["type"])
        self.assertEquals("About", button2["title"])
        self.assertEquals("https://aiml.foundation/about", button2["url"])
        button3 = buttons[2]
        self.assertEquals("web_url", button3["type"])
        self.assertEquals("Contact", button3["title"])
        self.assertEquals("https://aiml.foundation/contactus", button3["url"])

    def test_handle_reply(self):
        self.renderer.handle_reply(self.client_context, "Servusai", None)
        self.assertIsNotNone(self.renderer._payload)
        self.assertEquals("testid", self.renderer._payload['recipient']['id'])
        self.assertEquals("template", self.renderer._payload['message']['attachment']['type'])
        self.assertEquals("button", self.renderer._payload['message']['attachment']['payload']['template_type'])
        self.assertEquals("Servusai", self.renderer._payload['message']['attachment']['payload']['text'])
        self.assertEquals(1, len(self.renderer._payload['message']['attachment']['payload']['buttons']))
        self.assertEquals("postback", self.renderer._payload['message']['attachment']['payload']['buttons'][0]["type"])
        self.assertEquals("Servusai", self.renderer._payload['message']['attachment']['payload']['buttons'][0]["payload"])
        self.assertEquals("Servusai", self.renderer._payload['message']['attachment']['payload']['buttons'][0]["title"])

    def test_handle_postback_reply(self):
        self.renderer.handle_reply(self.client_context, "Servusai", "SERVUSAI")
        self.assertIsNotNone(self.renderer._payload)
        self.assertEquals("testid", self.renderer._payload['recipient']['id'])
        self.assertEquals("template", self.renderer._payload['message']['attachment']['type'])
        self.assertEquals("button", self.renderer._payload['message']['attachment']['payload']['template_type'])
        self.assertEquals("Servusai", self.renderer._payload['message']['attachment']['payload']['text'])
        self.assertEquals(1, len(self.renderer._payload['message']['attachment']['payload']['buttons']))
        self.assertEquals("postback", self.renderer._payload['message']['attachment']['payload']['buttons'][0]["type"])
        self.assertEquals("SERVUSAI", self.renderer._payload['message']['attachment']['payload']['buttons'][0]["payload"])
        self.assertEquals("Servusai", self.renderer._payload['message']['attachment']['payload']['buttons'][0]["title"])

    def test_handle_delay(self):
        self.renderer.handle_delay(self.client_context, 0)
        self.assertIsNotNone(self.renderer._payload)
        self.assertEquals("testid", self.renderer._payload['recipient']['id'])
        self.assertEquals("typing_off", self.renderer._payload['sender_action'])

    def test_handle_split(self):
        self.renderer.handle_split(self.client_context)
        self.assertIsNone(self.renderer._payload)

    def test_handle_list(self):
        items= [

        ]
        self.renderer.handle_list(self.client_context, items)
        self.assertIsNotNone(self.renderer._payload)
        self.assertEquals("testid", self.renderer._payload['recipient']['id'])
        message = self.renderer._payload['message']
        self.assertIsNotNone(message['attachment'])
        attachment = message['attachment']
        self.assertEquals("template", attachment['type'])
        self.assertIsNotNone(attachment['payload'])
        payload = attachment['payload']
        self.assertEquals("list", payload["template_type"])
        self.assertIsNotNone(payload['elements'])
        elements = payload['elements']
        self.assertEquals(0, len(elements))

    def test_handle_ordered_list(self):
        items = [
            ("Servusai Home", "http://www.servusai.com", None)
            ("About Servusai", "http://www.servusai.com/about", None)
            ("Contact Servusai", "http://www.servusai.com/contact", None)
        ]
        self.renderer.handle_ordered_list(self.client_context, items)
        self.assertIsNotNone(self.renderer._payload)
        self.renderer.handle_list(self.client_context, items)
        self.assertIsNotNone(self.renderer._payload)
        self.assertEquals("testid", self.renderer._payload['recipient']['id'])
        message = self.renderer._payload['message']
        self.assertIsNotNone(message['attachment'])
        attachment = message['attachment']
        self.assertEquals("template", attachment['type'])
        self.assertIsNotNone(attachment['payload'])
        payload = attachment['payload']
        self.assertEquals("list", payload["template_type"])
        self.assertIsNotNone(payload['elements'])
        elements = payload['elements']
        self.assertEquals(0, len(elements))

    def test_render_payload(self):
        pass

    def test_handle_location(self):
        self.renderer.handle_location(self.client_context)
        self.assertIsNotNone(self.renderer._payload)
        self.assertEquals("testid", self.renderer._payload['recipient']['id'])
        self.assertEquals("Your location", self.renderer._payload['message']['text'])
        self.assertEquals("location", self.renderer._payload['message']['quick_replies'][0]['content_type'])

