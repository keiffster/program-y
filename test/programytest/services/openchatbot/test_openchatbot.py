import unittest
import json

from programy.services.openchatbot.openchatbot import OpenChatBot


class OpenChatBotTests(unittest.TestCase):

    def test_construction_with_valid_json_with_port(self):
        payload = json.loads("""{
                       "openchatbot": {
                           "endpoint": "/api/mybot/v1.0/ask",
                           "host": "https://website1.com",
                           "port": 80,
                           "methods": ["GET", "POST"]
                       }
                    }""")
        domaincb = OpenChatBot.create("openchatbot", payload)
        self.assertIsNotNone(domaincb)

        self.assertEquals(["GET", "POST"], domaincb.methods)

        self.assertEquals("https://website1.com:80/api/mybot/v1.0/ask", domaincb.url)

    def test_construction_with_valid_json_no_port(self):
        payload = json.loads("""{
                       "openchatbot": {
                           "endpoint": "/api/mybot/v1.0/ask",
                           "host": "https://website1.com",
                           "methods": ["GET", "POST"]
                       }
                    }""")
        domaincb = OpenChatBot.create("openchatbot", payload)
        self.assertIsNotNone(domaincb)

        self.assertEquals(["GET", "POST"], domaincb.methods)

        self.assertEquals("https://website1.com/api/mybot/v1.0/ask", domaincb.url)

    def test_construction_with_uri_no_slash(self):
        payload = json.loads("""{
                       "openchatbot": {
                           "endpoint": "api/mybot/v1.0/ask",
                           "host": "https://website1.com",
                           "port": 80,
                           "methods": ["GET", "POST"]
                       }
                    }""")
        domaincb = OpenChatBot.create("openchatbot", payload)
        self.assertIsNotNone(domaincb)

        self.assertEquals(["GET", "POST"], domaincb.methods)

        self.assertEquals("https://website1.com:80/api/mybot/v1.0/ask", domaincb.url)
