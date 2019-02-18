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
from programy.storage.entities.link import LinkStore
from programy.storage.stores.nosql.mongo.dao.link import Link


class MongoLinkStore(MongoStore, LinkStore):

    LINKS = "links"
    PRIMARY_USER = "primary_user"
    PROVIDED_KEY = 'provided_key'
    GENERATED_KEY = 'generated_key'

    def __init__(self, storage_engine):
        MongoStore.__init__(self, storage_engine)

    def collection_name(self):
        return MongoLinkStore.LINKS

    def create_link(self, primary_userid, provided_key, generated_key, expires, expired=False, retry_count=0):
        YLogger.info(self, "Creating link in Mongo [%s] [%s] [%s]", primary_userid, generated_key, provided_key)
        link = Link(primary_userid, provided_key, generated_key, expires, expired, retry_count)
        self.add_document(link)
        return True

    def get_link(self, primary_user):
        collection = self.collection()
        doc = collection.find_one({MongoLinkStore.PRIMARY_USER: primary_user})
        if doc is not None:
            return Link.from_document(doc)
        return None

    def remove_link(self, primary_user):
        collection = self.collection()
        collection.delete_many({MongoLinkStore.PRIMARY_USER: primary_user})
        return True

    def link_exists(self, userid, provided_key, generated_key):
        collection = self.collection()
        link = collection.find_one({MongoLinkStore.PRIMARY_USER: userid, MongoLinkStore.PROVIDED_KEY: provided_key, MongoLinkStore.GENERATED_KEY: generated_key})
        return bool(link is not None)

    def update_link(self, link):
        collection = self.collection()
        collection.update({'_id': link.id}, Link.to_document(link))
        return True