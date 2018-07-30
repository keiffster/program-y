import unittest

from programy.storage.stores.nosql.mongo.dao.variable import Variables

class VariablesTests(unittest.TestCase):

    def test_init(self):
        variables = Variables("console", "keiffster")

        self.assertIsNotNone(variables)
        self.assertIsNone(variables.id)
        self.assertEquals("keiffster", variables.userid)
        self.assertEquals("console", variables.clientid)

