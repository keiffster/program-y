import unittest
import json

from programy.services.openchatbot.domain import OpenChatBotDomainHandler
from programy.config.brain.openchatbots import BrainOpenChatBotsConfiguration


class MockHTTPResponse(object):

    def __init__(self, status_code, text=None):
        self.status_code = status_code
        self.text = text

    def json(self):
        return json.loads(self.text)


class MockHTTPRequests(object):

    def __init__(self, response=None, status_code=200, valid_domain=".com"):
        self._response = response
        self._status_code = status_code
        self._valid_domain = valid_domain

    def get(self, url):
        if self._valid_domain in url:
            return MockHTTPResponse(self._status_code, self._response)
        else:
            return MockHTTPResponse(404)


class OpenChatBotDomainHandlerTests(unittest.TestCase):

    def test_construction_with_create_query_url(self):
        config = BrainOpenChatBotsConfiguration()
        handler = OpenChatBotDomainHandler(config)
        self.assertIsNotNone(handler)

        self.assertEquals("https://website1.com/.well-known/openchatbot-configuration", handler._create_query_url("website1", "https", "com"))
        self.assertEquals("http://website1.com/.well-known/openchatbot-configuration", handler._create_query_url("website1", "http", "com"))

        self.assertEquals("https://website1.org/.well-known/openchatbot-configuration", handler._create_query_url("website1", "https", ext="org"))
        self.assertEquals("http://website1.org/.well-known/openchatbot-configuration", handler._create_query_url("website1", "http", ext="org"))

    def test_construction_with_scan_alternatives_com(self):

        mock_requests = MockHTTPRequests(response="""{
                       "openchatbot": {
                           "endpoint": "api/mybot/v1.0/ask",
                           "host": "https://website1.com",
                           "port": 80,
                           "methods": ["GET", "POST"]
                       }
                    }""")

        config = BrainOpenChatBotsConfiguration()
        handler = OpenChatBotDomainHandler(config, http_requests=mock_requests)
        self.assertIsNotNone(handler)

        domaincb = handler.get_endpoint("website1")
        self.assertIsNotNone(domaincb)

        self.assertEquals("https://website1.com:80/api/mybot/v1.0/ask", domaincb.url)

    def test_construction_with_scan_alternatives_org(self):

        mock_requests = MockHTTPRequests(response="""{
                       "openchatbot": {
                           "endpoint": "api/mybot/v1.0/ask",
                           "host": "https://website1.com",
                           "port": 80,
                           "methods": ["GET", "POST"]
                       }
                    }""",
                    valid_domain=".org")

        config = BrainOpenChatBotsConfiguration()
        config._domains = ['org']
        handler = OpenChatBotDomainHandler(config, http_requests=mock_requests)
        self.assertIsNotNone(handler)

        domaincb = handler.get_endpoint("website1")
        self.assertIsNotNone(domaincb)

        self.assertEquals("https://website1.com:80/api/mybot/v1.0/ask", domaincb.url)

    def test_construction_with_no_scan_alternatives(self):

        mock_requests = MockHTTPRequests(response="""{
                       "openchatbot": {
                           "endpoint": "api/mybot/v1.0/ask",
                           "host": "https://website1.com",
                           "port": 80,
                           "methods": ["GET", "POST"]
                       }
                    }""")

        config = BrainOpenChatBotsConfiguration()
        handler = OpenChatBotDomainHandler(config, http_requests=mock_requests)
        self.assertIsNotNone(handler)

        domaincb = handler.get_endpoint("website1")
        self.assertIsNotNone(domaincb)

        self.assertEquals("https://website1.com:80/api/mybot/v1.0/ask", domaincb.url)
