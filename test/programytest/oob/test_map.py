import unittest
import unittest.mock

from programy.oob.map import MapOutOfBandProcessor
import xml.etree.ElementTree as ET

class MapOutOfBandProcessorTests(unittest.TestCase):

    def test_processor_xml_parsing(self):
        oob_processor = MapOutOfBandProcessor()
        self.assertIsNotNone(oob_processor)

        self.assertFalse(oob_processor.parse_oob_xml(None))

        oob = unittest.mock.Mock()
        oob.text = None
        self.assertFalse(oob_processor.parse_oob_xml(oob))

        oob = unittest.mock.Mock()
        oob.text = "Kinghorn"
        self.assertTrue(oob_processor.parse_oob_xml(oob))

    def test_processor(self):
        oob_processor = MapOutOfBandProcessor()
        self.assertIsNotNone(oob_processor)

        oob_content = ET.fromstring("<geomap>Kinghorn</geomap>")
        self.assertEqual("MAP", oob_processor.process_out_of_bounds(None, "console", oob_content))
