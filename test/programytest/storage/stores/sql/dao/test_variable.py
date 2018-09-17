
import unittest

from programy.storage.stores.sql.dao.variables import Variable

class VariableTests(unittest.TestCase):
    
    def test_init(self):
        variable1 = Variable(clientid='client', userid='user', name='name', value='value')
        self.assertIsNotNone(variable1)
        self.assertEqual("<Variable(id='n/a', clientid='client', userid='user', name='name', value='value')>", str(variable1))
        
        variable2 = Variable(id=1, clientid='client', userid='user', name='name', value='value')
        self.assertIsNotNone(variable2)
        self.assertEqual("<Variable(id='1', clientid='client', userid='user', name='name', value='value')>", str(variable2))
