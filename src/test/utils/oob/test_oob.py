import unittest

from programy.utils.oob.oob import OutOfBoundsProcessor

class OutOfBoundsProcessorTests(unittest.TestCase):

    def test_processor(self):
        oob_processor = OutOfBoundsProcessor()
        self.assertIsNotNone(oob_processor)
        with self.assertRaises(Exception):
            oob_processor.process_out_of_bounds(None, "console", "<something>process</something>")