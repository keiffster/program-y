import unittest

from programy.utils.oob.url import URLOutOfBandProcessor
import xml.etree.ElementTree as ET

class URLOutOfBandProcessorTests(unittest.TestCase):

    def test_processor(self):
        oob_processor = URLOutOfBandProcessor()
        self.assertIsNotNone(oob_processor)

        oob_content = ET.fromstring("<url>http://www.keithsterling.com</url>")
        self.assertEqual("URL", oob_processor.process_out_of_bounds(None, "console", oob_content))
