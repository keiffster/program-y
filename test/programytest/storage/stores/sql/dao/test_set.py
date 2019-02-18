import unittest

from programy.storage.stores.sql.dao.set import Set


class SetTests(unittest.TestCase):
    
    def test_init(self):
        property1 = Set(name='name', value='value')
        self.assertIsNotNone(property1)
        self.assertEqual("<Set(id='n/a', name='name', value='value')>", str(property1))

        property2 = Set(id=1, name='name', value='value')
        self.assertIsNotNone(property2)
        self.assertEqual("<Set(id='1', name='name', value='value')>", str(property2))
