import unittest

from programy.utils.oob.email import EmailOutOfBoundsProcessor

class DefaultOutOfBoundsProcessorTests(unittest.TestCase):

    def test_processor(self):
        oob_processor = EmailOutOfBoundsProcessor()
        self.assertIsNotNone(oob_processor)
        self.assertEqual("", oob_processor.process_out_of_bounds(None, "console", "<email>keiffster@gmail.com</email>"))