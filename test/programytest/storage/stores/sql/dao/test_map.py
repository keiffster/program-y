
import unittest

from programy.storage.stores.sql.dao.map import Map

class MapTests(unittest.TestCase):

    def test_init(self):
        lookup1 = Map(name='map', key="key", value="value")
        self.assertIsNotNone(lookup1)
        self.assertEqual("<Map(id='n/a', name='map', key='key', value='value')>", str(lookup1))

        lookup2 = Map(id=1, name='map', key="key", value="value")
        self.assertIsNotNone(lookup2)
        self.assertEqual("<Map(id='1', name='map', key='key', value='value')>", str(lookup2))
