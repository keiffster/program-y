import unittest

class Vistor(object):
    def visit(self, text):
        pass

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
        link_store.create_link(primary_userid=1, generated_key='AFG37CE', provided_key="Password")
        link_store.commit ()

    def property_asserts(self, storage_engine):
        property_store = storage_engine.property_store()
        property_store.add_property(name="topic", value="*")
        property_store.add_properties({"name": "Fred",
                                                                  "age": "47",
                                                                  "occupation": "Gardener"})
        property_store.commit()

    def conversation_asserts(self, storage_engine, visit=True):
        convo_store = storage_engine.conversation_store()
        convo_store.store_conversation(clientid="twitter", userid="@keiffster", botid="botid1", brainid="brainid1",
                                       depth=0, question="Hello", response="Hi there!")
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
        self.assertEquals(1, last_direct_message_id)
        self.assertEquals(2, last_status_id)

