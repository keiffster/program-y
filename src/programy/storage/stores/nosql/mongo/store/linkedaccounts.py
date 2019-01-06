"""
Copyright (c) 2016-2019 Keith Sterling http://www.keithsterling.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
from programy.utils.logging.ylogger import YLogger
from programy.storage.stores.nosql.mongo.store.mongostore import MongoStore
from programy.storage.entities.linked import LinkedAccountStore
from programy.storage.stores.nosql.mongo.dao.linked import LinkedAccount


class MongoLinkedAccountStore(MongoStore, LinkedAccountStore):

    LINKEDACCOUNTS = 'linkedaccounts'
    PRIMARY_USERID = "primary_userid"
    LINKED_USERID = "linked_userid"

    def __init__(self, storage_engine):
        MongoStore.__init__(self, storage_engine)

    def collection_name(self):
        return MongoLinkedAccountStore.LINKEDACCOUNTS

    def link_accounts(self, primary_userid, linked_userid):
        YLogger.info(self, "Linking accounts [%s] [%s] in Mongo", primary_userid, linked_userid)
        linked = LinkedAccount(primary_userid, linked_userid)
        self.add_document(linked)
        return True

    def unlink_accounts(self, primary_userid):
        YLogger.info(self, "Unlinking accounts [%s] in Mongo", primary_userid)
        collection = self.collection()
        collection.delete_many({MongoLinkedAccountStore.PRIMARY_USERID: primary_userid})
        return True

    def linked_accounts(self, primary_userid):
        collection = self.collection()
        linked_accounts = collection.find({MongoLinkedAccountStore.PRIMARY_USERID: primary_userid})
        accounts = []
        for account in linked_accounts:
            accounts.append(account['linked_userid'])
        return accounts

    def primary_account(self, linked_userid):
        collection = self.collection()
        account = collection.find_one({MongoLinkedAccountStore.LINKED_USERID: linked_userid})
        if account is not None:
            return account['primary_userid']
        return None
