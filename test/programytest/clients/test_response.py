import unittest

from programy.clients.response import ResponseLogger


class ResponseLoggerTests(unittest.TestCase):

    def test_init(self):

        logger = ResponseLogger()
        self.assertIsNotNone(logger)

        logger.log_response("question", "answer")

        logger.log_unknown_response("question")
