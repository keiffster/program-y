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
from programy.storage.entities.user import UserStore
from programy.storage.stores.nosql.mongo.dao.user import User


class MongoUserStore(MongoStore, UserStore):

    USERS = 'users'
    USERID = 'userid'
    CLIENT = 'client'

    def __init__(self, storage_engine):
        MongoStore.__init__(self, storage_engine)

    def collection_name(self):
        return MongoUserStore.USERS

    def add_user(self, userid, client):
        YLogger.info(self, "Adding user [%s] for client [%s]", userid, client)
        user = User(userid, client)
        self.add_document(user)
        return True

    def exists(self, userid, clientid):
        collection = self.collection()
        user = collection.find_one({MongoUserStore.USERID: userid, MongoUserStore.CLIENT: clientid})
        return bool(user is not None)

    def get_links(self, userid):
        collection = self.collection()
        users = collection.find({MongoUserStore.USERID: userid})
        links = []
        for user in users:
            links.append(user['client'])
        return links

    def remove_user(self, userid, clientid):
        collection = self.collection()
        collection.delete_many({MongoUserStore.USERID: userid, MongoUserStore.CLIENT: clientid})
        return True

    def remove_user_from_all_clients(self, userid):
        collection = self.collection()
        collection.delete_many({MongoUserStore.USERID: userid})
        return True
