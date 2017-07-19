import unittest

from programy.utils.oob.dial import DialOutOfBoundsProcessor

class DefaultOutOfBoundsProcessorTests(unittest.TestCase):

    def test_processor(self):
        oob_processor = DialOutOfBoundsProcessor()
        self.assertIsNotNone(oob_processor)
        self.assertEqual("", oob_processor.process_out_of_bounds(None, "console", "<dial>07777777777</dial>"))