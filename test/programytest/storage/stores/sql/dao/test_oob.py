
import unittest

from programy.storage.stores.sql.dao.oob import OOB


class OOBTests(unittest.TestCase):
    
    def test_init(self):
        oob1 = OOB(name='name', oob_class='class')
        self.assertIsNotNone(oob1)
        self.assertEqual("<OOB(id='n/a', name='name', oob_class='class')>", str(oob1))
        
        oob2 = OOB(id=1, name='name', oob_class='class')
        self.assertIsNotNone(oob2)
        self.assertEqual("<OOB(id='1', name='name', oob_class='class')>", str(oob2))

