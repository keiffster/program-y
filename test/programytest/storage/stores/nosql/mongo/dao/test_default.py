import unittest

from programy.storage.stores.nosql.mongo.dao.default import Default

class DefaultTests(unittest.TestCase):

    def test_init(self):
        default = Default()

        self.assertIsNotNone(default)
        self.assertIsNone(default.id)

