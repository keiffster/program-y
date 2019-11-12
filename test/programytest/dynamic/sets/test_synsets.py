import unittest

from programy.context import ClientContext
from programy.dynamic.sets.synsets import IsSynset
from programytest.client import TestClient


class IsSynsetDynamicSetTests(unittest.TestCase):

    def setUp(self):
        self._client_context = ClientContext(TestClient(), "testid")

    def test_is_synset(self):
        dyn_var = IsSynset(None)
        self.assertIsNotNone(dyn_var)
        self.assertFalse(dyn_var.is_member(self._client_context, None))
        self.assertTrue(dyn_var.is_member(self._client_context, "chop", {"similar": "hack"}))

    def test_is_synset_no_additional(self):
        dyn_var = IsSynset(None)
        self.assertIsNotNone(dyn_var)
        self.assertFalse(dyn_var.is_member(self._client_context, None))
        self.assertFalse(dyn_var.is_member(self._client_context, "chop"))

    def test_is_synset_invalid_similar(self):
        dyn_var = IsSynset(None)
        self.assertIsNotNone(dyn_var)
        self.assertFalse(dyn_var.is_member(self._client_context, None))
        self.assertFalse(dyn_var.is_member(self._client_context, "chop", {"other": "hack"}))
