import unittest

from programy.utils.oob.dialog import DialogOutOfBandProcessor
import xml.etree.ElementTree as ET

class DialogOutOfBandProcessorTests(unittest.TestCase):

    def test_processor(self):
        oob_processor = DialogOutOfBandProcessor()
        self.assertIsNotNone(oob_processor)

        oob_content = ET.fromstring("<dialog><title>Which contact?</title><list>contact1, contact2, contact3</list></dialog>")
        self.assertEqual("DIALOG", oob_processor.process_out_of_bounds(None, "console", oob_content))
