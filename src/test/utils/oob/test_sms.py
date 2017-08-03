import unittest

from programy.utils.oob.sms import SMSOutOfBandProcessor
import xml.etree.ElementTree as ET

class SMSOutOfBandProcessorTests(unittest.TestCase):

    def test_processor(self):
        oob_processor = SMSOutOfBandProcessor()
        self.assertIsNotNone(oob_processor)

        oob_content = ET.fromstring("<sms><recipient>077777777</recipient><message>Hello!</message></sms>")
        self.assertEqual("SMS", oob_processor.process_out_of_bounds(None, "console", oob_content))
