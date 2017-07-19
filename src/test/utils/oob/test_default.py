import unittest

from programy.utils.oob.default import DefaultOutOfBoundsProcessor

class DefaultOutOfBoundsProcessorTests(unittest.TestCase):

    def test_processor(self):
        oob_processor = DefaultOutOfBoundsProcessor()
        self.assertIsNotNone(oob_processor)
        self.assertEqual("<something>process</something>", oob_processor.process_out_of_bounds(None, "console", "<something>process</something>"))