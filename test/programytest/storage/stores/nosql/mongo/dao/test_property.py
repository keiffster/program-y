import unittest

from programy.storage.stores.nosql.mongo.dao.property import Property

class PropertyTests(unittest.TestCase):

    def test_init(self):
        property = Property()

        self.assertIsNotNone(property)
        self.assertIsNone(property.id)

