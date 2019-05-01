import unittest

from programy.triggers.receiver import handle_trigger


class ReceiverTests(unittest.TestCase):

    def test_trigger(self):
        response = handle_trigger('{"key": "value"}')
        self.assertIsNotNone(response)
        self.assertEquals("OK", response)

    def test_trigger_no_json(self):
        response = handle_trigger(None)
        self.assertIsNotNone(response)
        self.assertEquals("OK", response)

    def test_trigger_invalid_json(self):
        response = handle_trigger('{"key":}')
        self.assertIsNotNone(response)
        self.assertEquals("OK", response)