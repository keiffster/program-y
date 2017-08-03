import unittest

from programy.utils.oob.map import MapOutOfBandProcessor
import xml.etree.ElementTree as ET

class MapOutOfBandProcessorTests(unittest.TestCase):

    def test_processor(self):
        oob_processor = MapOutOfBandProcessor()
        self.assertIsNotNone(oob_processor)

        oob_content = ET.fromstring("<map>Kinghorn</map>")
        self.assertEqual("MAP", oob_processor.process_out_of_bounds(None, "console", oob_content))
