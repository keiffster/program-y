import unittest

from programy.storage.stores.nosql.mongo.dao.trigger import Trigger


class TriggerTests(unittest.TestCase):

    def test_init_no_id(self):
        trigger = Trigger(name="test", trigger_class="test.triggerclass")

        self.assertIsNotNone(trigger)
        self.assertIsNone(trigger.id)
        self.assertEqual("test", trigger.name)
        self.assertEqual("test.triggerclass", trigger.trigger_class)
        self.assertEqual({'name': 'test', 'trigger_class': 'test.triggerclass'}, trigger.to_document())

    def test_init_with_id(self):
        trigger = Trigger(name="test", trigger_class="test.triggerclass")
        trigger.id = '666'

        self.assertIsNotNone(trigger)
        self.assertIsNotNone(trigger.id)
        self.assertEqual('666', trigger.id)
        self.assertEqual("test", trigger.name)
        self.assertEqual("test.triggerclass", trigger.trigger_class)
        self.assertEqual({'_id': '666', 'name': 'test', 'trigger_class': 'test.triggerclass'}, trigger.to_document())

    def test_from_document_no_id(self):
        trigger1 = Trigger.from_document({'name': 'test', 'trigger_class': 'test.triggerclass'})
        self.assertIsNotNone(trigger1)
        self.assertIsNone(trigger1.id)
        self.assertEqual("test", trigger1.name)
        self.assertEqual("test.triggerclass", trigger1.trigger_class)

    def test_from_document_with_id(self):
        trigger2 = Trigger.from_document({'_id': '666', 'name': 'test', 'trigger_class': 'test.triggerclass'})
        self.assertIsNotNone(trigger2)
        self.assertIsNotNone(trigger2.id)
        self.assertEqual('666', trigger2.id)
        self.assertEqual("test", trigger2.name)
        self.assertEqual("test.triggerclass", trigger2.trigger_class)

    def test_from_document_no_id(self):
        trigger1 = Trigger.from_document({'name': 'test', 'trigger_class': 'test.triggerclass'})
        self.assertEquals("<Trigger(id='n/a', name='test', trigger_class='test.triggerclass')>", str(trigger1))

    def test_from_document_with_id(self):
        trigger2 = Trigger.from_document({'_id': '666', 'name': 'test', 'trigger_class': 'test.triggerclass'})
        self.assertEquals("<Trigger(id='666', name='test', trigger_class='test.triggerclass')>", str(trigger2))

