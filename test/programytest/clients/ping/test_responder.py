import unittest

from programy.clients.ping.responder import PingResponder
from programytest.client import TestClient


class PingResponderTests(unittest.TestCase):

    def test_output(self):

        client = TestClient()

        responder = PingResponder(client)

        result = responder.ping()

        self.assertIsNotNone(result)
        self.assertTrue("start_time" in result)
        self.assertTrue("client" in result)
        self.assertTrue("bots" in result)
        self.assertTrue("logging" in result)


