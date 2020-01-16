
import unittest

from programy.storage.stores.sql.dao.trigger import Trigger


class TriggerTests(unittest.TestCase):
    
    def test_init(self):
        trigger1 = Trigger(name='name', trigger_class='class')
        self.assertIsNotNone(trigger1)
        self.assertEqual("<Trigger(id='n/a', name='name', trigger_class='class')>", str(trigger1))
        
        trigger2 = Trigger(id=1, name='name', trigger_class='class')
        self.assertIsNotNone(trigger2)
        self.assertEqual("<Trigger(id='1', name='name', trigger_class='class')>", str(trigger2))

