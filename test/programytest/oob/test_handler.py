import unittest

from programy.config.brain.oob import BrainOOBConfiguration
from programy.config.brain.oobs import BrainOOBSConfiguration
from programy.oob.defaults.oob import OutOfBandProcessor
from programy.oob.handler import OOBHandler
from programytest.client import TestClient


class TestOOBHandler(unittest.TestCase):

    def test_init_empty_config(self):
        handler = OOBHandler(BrainOOBSConfiguration())
        self.assertIsNotNone(handler)
        self.assertIsNone(handler.default_oob)
        self.assertEquals({}, handler.oobs)

    def test_oob_in_response(self):
        handler = OOBHandler(BrainOOBSConfiguration())

        self.assertTrue(handler.oob_in_response("<oob>"))
        self.assertFalse(handler.oob_in_response("<xxx>"))
        self.assertFalse(handler.oob_in_response("<>"))
        self.assertFalse(handler.oob_in_response(None))

    def test_load_configuration_only_default(self):

        oobconfig1 = BrainOOBConfiguration("oob1")
        oobconfig1._classname = "programy.oob.defaults.oob.OutOfBandProcessor"

        oobsconfig = BrainOOBSConfiguration()
        oobsconfig._default = oobconfig1

        handler = OOBHandler(oobsconfig)

        handler.load_oob_processors()

        self.assertEqual({}, handler.oobs)
        self.assertIsInstance(handler.default_oob, OutOfBandProcessor)

    def test_load_configuration_invalid_default(self):

        oobconfig1 = BrainOOBConfiguration("oob1")
        oobconfig1._classname = "programy.oob.defaults.oob.OutOfBandProcessorXXXX"

        oobsconfig = BrainOOBSConfiguration()
        oobsconfig._default = oobconfig1

        handler = OOBHandler(oobsconfig)

        handler.load_oob_processors()

        self.assertEqual({}, handler.oobs)
        self.assertEqual(None, handler.default_oob)

    def test_load_configuration_none(self):
        with self.assertRaises(AssertionError):
            handler = OOBHandler(None)

    def test_load_configuration_no_default(self):

        oobconfig1 = BrainOOBConfiguration("oob1")
        oobconfig1._classname = "programy.oob.defaults.oob.OutOfBandProcessor"

        oobsconfig = BrainOOBSConfiguration()
        oobsconfig._oobs['test'] = oobconfig1

        handler = OOBHandler(oobsconfig)

        handler.load_oob_processors()

        self.assertTrue("test" in handler.oobs)
        self.assertEqual(None, handler.default_oob)

    def test_load_configuration_invalid_oobs(self):

        oobconfig1 = BrainOOBConfiguration("oob1")
        oobconfig1._classname = "programy.oob.defaults.oob.OutOfBandProcessorXXXX"

        oobsconfig = BrainOOBSConfiguration()
        oobsconfig._oobs['test'] = oobconfig1

        handler = OOBHandler(oobsconfig)

        handler.load_oob_processors()

        self.assertFalse("test" in handler.oobs)
        self.assertEqual(None, handler.default_oob)

    def test_strip_oob(self):
        handler = OOBHandler(BrainOOBSConfiguration())

        response, oob = handler.strip_oob("<oob><camera>on</camera></oob>")
        self.assertEqual("", response)
        self.assertEqual("<oob><camera>on</camera></oob>", oob)

        response, oob = handler.strip_oob("<oob><camera>on</camera></oob>Other Text")
        self.assertEqual("Other Text", response)
        self.assertEqual("<oob><camera>on</camera></oob>", oob)

        response, oob = handler.strip_oob("Some Text <oob><camera>on</camera></oob>Other Text")
        self.assertEqual("Some Text Other Text", response)
        self.assertEqual("<oob><camera>on</camera></oob>", oob)

        response, oob = handler.strip_oob("<camera>on</camera>")
        self.assertEqual("<camera>on</camera>", response)
        self.assertEqual(None, oob)

    def test_handle_with_oob(self):
        oobconfig1 = BrainOOBConfiguration("oob1")
        oobconfig1._classname = "programy.oob.defaults.camera.CameraOutOfBandProcessor"

        oobsconfig = BrainOOBSConfiguration()
        oobsconfig._oobs['camera'] = oobconfig1

        handler = OOBHandler(oobsconfig)

        handler.load_oob_processors()

        response = handler.handle(None, "<oob><camera>on</camera></oob>")
        self.assertEqual("CAMERA", response)

    def test_handle_with_oob_invalid_class_with_default(self):
        oobconfig1 = BrainOOBConfiguration("oob1")
        oobconfig1._classname = "programy.oob.defaults.camera.CameraOutOfBandProcessorXX"

        oobconfig2 = BrainOOBConfiguration("oob1")
        oobconfig2._classname = "programy.oob.defaults.map.MapOutOfBandProcessor"

        oobsconfig = BrainOOBSConfiguration()
        oobsconfig._oobs['camera'] = oobconfig1
        oobsconfig._default = oobconfig2

        handler = OOBHandler(oobsconfig)

        handler.load_oob_processors()

        response = handler.handle(None, "<oob><camera>on</camera></oob>")
        self.assertEqual("MAP", response)

    def test_handle_with_oob_invalid_class_no_default(self):
        oobconfig1 = BrainOOBConfiguration("oob1")
        oobconfig1._classname = "programy.oob.defaults.camera.CameraOutOfBandProcessorXX"

        oobsconfig = BrainOOBSConfiguration()
        oobsconfig._oobs['camera'] = oobconfig1

        handler = OOBHandler(oobsconfig)

        handler.load_oob_processors()

        response = handler.handle(None, "<oob><camera>on</camera></oob>")
        self.assertEqual("", response)

    def test_handle_without_oob(self):
        handler = OOBHandler(BrainOOBSConfiguration())
        response = handler.handle(None, "<camera>on</camera>")
        self.assertEqual("<camera>on</camera>", response)

    def test_process_oob(self):
        client = TestClient()
        self._client_context = client.create_client_context("testid")

        oobconfig1 = BrainOOBConfiguration("oob1")
        oobconfig1._classname = "programy.oob.defaults.camera.CameraOutOfBandProcessor"

        oobconfig2 = BrainOOBConfiguration("oob1")
        oobconfig2._classname = "programy.oob.defaults.map.MapOutOfBandProcessor"

        oobsconfig = BrainOOBSConfiguration()
        oobsconfig._oobs['camera'] = oobconfig1
        oobsconfig._default = oobconfig2

        handler = OOBHandler(oobsconfig)

        handler.load_oob_processors()

        response = handler.process_oob(self._client_context, "<oob><camera>on</camera></oob>")
        self.assertEquals("CAMERA", response)

    def test_process_oob_no_oob(self):
        client = TestClient()
        self._client_context = client.create_client_context("testid")

        oobconfig1 = BrainOOBConfiguration("oob1")
        oobconfig1._classname = "programy.oob.defaults.camera.CameraOutOfBandProcessor"

        oobconfig2 = BrainOOBConfiguration("oob1")
        oobconfig2._classname = "programy.oob.defaults.map.MapOutOfBandProcessor"

        oobsconfig = BrainOOBSConfiguration()
        oobsconfig._oobs['camera'] = oobconfig1
        oobsconfig._default = oobconfig2

        handler = OOBHandler(oobsconfig)

        handler.load_oob_processors()

        response = handler.process_oob(self._client_context, "<camera>on</camera>")
        self.assertEquals("", response)

    def test_process_oob_use_default(self):
        client = TestClient()
        self._client_context = client.create_client_context("testid")

        oobconfig1 = BrainOOBConfiguration("oob1")
        oobconfig1._classname = "programy.oob.defaults.camera.CameraOutOfBandProcessor"

        oobconfig2 = BrainOOBConfiguration("oob1")
        oobconfig2._classname = "programy.oob.defaults.map.MapOutOfBandProcessor"

        oobsconfig = BrainOOBSConfiguration()
        oobsconfig._oobs['camera'] = oobconfig1
        oobsconfig._default = oobconfig2

        handler = OOBHandler(oobsconfig)

        handler.load_oob_processors()

        response = handler.process_oob(self._client_context, "<oob><light>on</light></oob>")
        self.assertEquals("MAP", response)

