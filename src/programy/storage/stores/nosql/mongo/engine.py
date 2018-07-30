"""
Copyright (c) 2016-2018 Keith Sterling http://www.keithsterling.com

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

from pymongo import MongoClient

from programy.storage.engine import StorageEngine

from programy.storage.stores.nosql.mongo.store.categories import MongoCategoryStore
from programy.storage.stores.nosql.mongo.store.conversations import MongoConversationStore
from programy.storage.stores.nosql.mongo.store.links import MongoLinkStore
from programy.storage.stores.nosql.mongo.store.linkedaccounts import MongoLinkedAccountStore
from programy.storage.stores.nosql.mongo.store.properties import MongoPropertyStore
from programy.storage.stores.nosql.mongo.store.users import MongoUserStore


class MongoStorageEngine(StorageEngine):

    def __init__(self, configuration):
        StorageEngine.__init__(self, configuration)
        self._client = None
        self._database = None

    def initialise(self):
        self._client = MongoClient(self.configuration.url)
        self._database = self._client.get_database(self.configuration.database)

        if self.configuration.drop_all_first is True:
            self.user_store().drop()
            self.linked_account_store().drop()
            self.link_store().drop()
            self.property_store().drop ()
            self.conversation_store().drop ()

        return True

    def user_store(self):
        return MongoUserStore(self)

    def linked_account_store(self):
        return MongoLinkedAccountStore(self)

    def link_store(self):
        return MongoLinkStore(self)

    def property_store(self):
        return MongoPropertyStore(self)

    def conversation_store(self):
        return MongoConversationStore(self)

    def category_store(self):
        return MongoCategoryStore(self)
