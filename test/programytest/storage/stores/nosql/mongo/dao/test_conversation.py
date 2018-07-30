import unittest

from programy.storage.stores.nosql.mongo.dao.conversation import Conversation

class ConversationTests(unittest.TestCase):

    def test_init(self):
        conversation = Conversation("console", "user1", "bot1", "brain1", 0, "Hello", "Hi there")

        self.assertIsNotNone(conversation)
        self.assertIsNone(conversation.id)
        self.assertEquals("console", conversation.clientid)
        self.assertEquals("user1", conversation.userid)
        self.assertEquals("bot1", conversation.botid)
        self.assertEquals("brain1", conversation.brainid)
        self.assertEquals(0, conversation.depth)
        self.assertEquals("Hello", conversation.question)
        self.assertEquals("Hi there", conversation.response)

