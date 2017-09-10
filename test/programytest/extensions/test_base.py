import unittest
import unittest.mock

from programy.extensions.base import Extension

class ExtensionTests(unittest.TestCase):

    def test_ensure_not_implemented(self):
        bot = unittest.mock.Mock()

        extension = Extension()
        self.assertIsNotNone(extension)
        with self.assertRaises(Exception):
            extension.execute(bot, "testid", "Some Data")