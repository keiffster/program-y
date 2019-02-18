
import unittest

from programy.storage.stores.sql.dao.conversation import Conversation

class ConversationTests(unittest.TestCase):
    
    def test_init(self):

        conversation1 = Conversation(clientid='clientid', userid='userid', botid='botid', brainid='brainid', question='question', sentence='sentence', response='response')
        self.assertIsNotNone(conversation1)
        self.assertEqual("<Conversation(id='n/a', clientid='clientid', userid='userid', botid='botid', brainid='brainid', question='question', sentence='sentence', response='response'>", str(conversation1))
        
        conversation2 = Conversation(id=1, clientid='clientid', userid='userid', botid='botid', brainid='brainid', question='question', sentence='sentence', response='response')
        self.assertIsNotNone(conversation2)
        self.assertEqual("<Conversation(id='1', clientid='clientid', userid='userid', botid='botid', brainid='brainid', question='question', sentence='sentence', response='response'>", str(conversation2))
