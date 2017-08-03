import unittest

from programy.utils.oob.camera import CameraOutOfBandProcessor
import xml.etree.ElementTree as ET

class CameraOutOfBandProcessorTests(unittest.TestCase):

    def test_processor_on(self):
        oob_processor = CameraOutOfBandProcessor()
        self.assertIsNotNone(oob_processor)

        oob_content = ET.fromstring("<camera>on</camera>")
        self.assertEqual("CAMERA", oob_processor.process_out_of_bounds(None, "console", oob_content))

    def test_processor_off(self):
        oob_processor = CameraOutOfBandProcessor()
        self.assertIsNotNone(oob_processor)

        oob_content = ET.fromstring("<camera>off</camera>")
        self.assertEqual("CAMERA", oob_processor.process_out_of_bounds(None, "console", oob_content))
