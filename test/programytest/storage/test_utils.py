import unittest

from programy.dialog.question import Question
from programy.dialog.conversation import Conversation

from programytest.client import TestClient
import datetime

class StorageEngineTestUtils(unittest.TestCase):

    def user_asserts(self, storage_engine):
        user_store = storage_engine.user_store()
        user_store.add_user(userid="@keiffster", client="twitter")
        user_store.add_user(userid="keiffster@gmail.com", client="hangouts")
        user_store.add_user(userid="keiffster", client="telegram")
        user_store.commit()

    def linked_account_asserts(self, storage_engine):
        linked_accounts_store = storage_engine.linked_account_store()
        linked_accounts_store.link_accounts(primary_userid=1, linked_userid=2)
        linked_accounts_store.link_accounts(primary_userid=1, linked_userid=3)
        linked_accounts_store.commit()

    def link_asserts(self, storage_engine):
        link_store = storage_engine.link_store()
        link_store.create_link(primary_userid=1, generated_key='AFG37CE', provided_key="Password", expires=datetime.datetime.now())
        link_store.commit ()

    def property_asserts(self, storage_engine):
        property_store = storage_engine.property_store()
        property_store.add_property(name="topic", value="*")
        property_store.add_properties({"name": "Fred",
                                       "age": "47",
                                       "occupation": "Gardener"})
        property_store.commit()

    def conversation_asserts(self, storage_engine, visit=True):

        client = TestClient()
        client_context = client.create_client_context("user1")

        conversation = Conversation(client_context)

        question1 = Question.create_from_text(client_context, "Hello There")
        question1.sentence(0).response = "Hi"
        conversation.record_dialog(question1)

        convo_store = storage_engine.conversation_store()
        convo_store.store_conversation(client_context, conversation)
        convo_store.commit()

    def category_asserts(self, storage_engine):
        category_store = storage_engine.category_store()
        category_store.store_category(groupid="group1", userid="keiffster", topic="*", that=None, pattern="Hello", template="Hi there!")
        category_store.commit()

    def twitter_asserts(self, storage_engine, visit=True):
        twitter_store = storage_engine.twitter_store()
        twitter_store.store_last_message_ids(1, 2)
        twitter_store.commit()

        last_direct_message_id, last_status_id = twitter_store.load_last_message_ids()
        self.assertEqual(1, int(last_direct_message_id))
        self.assertEqual(2, int(last_status_id))

