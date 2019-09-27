import unittest
import unittest.mock

from programy.extensions.base import Extension


class MockExtension(Extension):

    def execute(self,context, data):
        raise NotImplementedError()



class ExtensionTests(unittest.TestCase):

    def test_ensure_not_implemented(self):
        bot = unittest.mock.Mock()

        extension = MockExtension()
        self.assertIsNotNone(extension)
        with self.assertRaises(Exception):
            extension.execute(bot, "testid", "Some Data")