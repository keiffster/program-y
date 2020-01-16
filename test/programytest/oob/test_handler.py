import unittest
from programy.oob.default import DefaultOutOfBandProcessor
from programy.oob.callmom.camera import CameraOutOfBandProcessor
from programy.oob.handler import OOBHandler
from programytest.client import TestClient


class TestOOBHandler(unittest.TestCase):

    def test_init_empty_config(self):
        handler = OOBHandler()
        self.assertIsNotNone(handler)
        self.assertIsNone(handler.default_oob)
        self.assertEquals({}, handler.oobs)

    def test_oob_in_response(self):
        handler = OOBHandler()

        self.assertTrue(handler.oob_in_response("<oob>"))
        self.assertFalse(handler.oob_in_response("<xxx>"))
        self.assertFalse(handler.oob_in_response("<>"))
        self.assertFalse(handler.oob_in_response(None))

    def test_load_configuration_only_default(self):

        handler = OOBHandler()
        handler.oobs['default'] = DefaultOutOfBandProcessor()

        self.assertTrue('default' in handler.oobs)
        self.assertIsInstance(handler.default_oob, DefaultOutOfBandProcessor)

    def test_load_configuration_no_default(self):
        handler = OOBHandler()
        handler.oobs['test'] = DefaultOutOfBandProcessor()

        self.assertTrue("test" in handler.oobs)
        self.assertEqual(None, handler.default_oob)

    def test_strip_oob(self):
        handler = OOBHandler()

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
        handler = OOBHandler()

        handler.oobs['camera'] = CameraOutOfBandProcessor()

        response = handler.handle(None, "<oob><camera>on</camera></oob>")
        self.assertEqual("CAMERA", response)

    def test_handle_with_oob_invalid_class_with_default(self):
        handler = OOBHandler()

        handler.oobs['test'] = DefaultOutOfBandProcessor()
        handler.oobs['default'] = DefaultOutOfBandProcessor()

        response = handler.handle(None, "<oob><camera>on</camera></oob>")
        self.assertEqual("", response)

    def test_handle_with_oob_invalid_class_no_default(self):
        handler = OOBHandler()

        response = handler.handle(None, "<oob><camera>on</camera></oob>")
        self.assertEqual("", response)

    def test_process_oob(self):
        client = TestClient()
        self._client_context = client.create_client_context("testid")

        handler = OOBHandler()

        handler.oobs['camera'] = CameraOutOfBandProcessor()
        handler.oobs['default'] = DefaultOutOfBandProcessor()

        response = handler.process_oob(self._client_context, "<oob><camera>on</camera></oob>")
        self.assertEquals("CAMERA", response)

    def test_process_oob_no_oob(self):
        client = TestClient()
        self._client_context = client.create_client_context("testid")

        handler = OOBHandler()

        handler.oobs['camera'] = CameraOutOfBandProcessor()
        handler.oobs['default'] = DefaultOutOfBandProcessor()

        response = handler.process_oob(self._client_context, "<camera>on</camera>")
        self.assertEquals("", response)

    def test_process_oob_use_default(self):
        client = TestClient()
        self._client_context = client.create_client_context("testid")

        handler = OOBHandler()

        handler.oobs['camera'] = CameraOutOfBandProcessor()
        handler.oobs['default'] = DefaultOutOfBandProcessor()

        response = handler.process_oob(self._client_context, "<oob><light>on</light></oob>")
        self.assertEquals("", response)

