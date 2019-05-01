import unittest

from programy.activate import Activatable


class ActivatableTests(unittest.TestCase):

    def test_init(self):
        activatable = Activatable()
        self.assertIsNotNone(activatable)
        self.assertEquals(Activatable.ON, activatable.active)
        self.assertTrue(activatable.is_active())

        activatable = Activatable(Activatable.ON)
        self.assertIsNotNone(activatable)
        self.assertEquals(Activatable.ON, activatable.active)
        self.assertTrue(activatable.is_active())

        activatable = Activatable(Activatable.OFF)
        self.assertIsNotNone(activatable)
        self.assertEquals(Activatable.OFF, activatable.active)
        self.assertFalse(activatable.is_active())

    def test_on_off(self):
        activatable = Activatable()
        self.assertIsNotNone(activatable)
        self.assertEquals(Activatable.ON, activatable.active)

        activatable.active = Activatable.OFF
        self.assertEquals(Activatable.OFF, activatable.active)
        self.assertFalse(activatable.is_active())

        activatable.active = Activatable.ON
        self.assertEquals(Activatable.ON, activatable.active)
        self.assertTrue(activatable.is_active())

    def test_invalid_state(self):
        activatable = Activatable()
        self.assertIsNotNone(activatable)
        self.assertEquals(Activatable.ON, activatable.active)

        activatable.active = "OTHER"

        self.assertEquals(Activatable.ON, activatable.active)
