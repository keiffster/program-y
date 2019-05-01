import unittest

from programy.storage.stores.sql.loader import Uploader


class UploaderTests(unittest.TestCase):

        def test_create_arguments(self):
            arguments = Uploader.create_arguments()
            self.assertIsNotNone(arguments)
