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
from programy.storage.entities.category import CategoryStore
from programy.storage.stores.nosql.mongo.dao.category import Category


class MongoCategoryStore(CategoryStore, MongoStore):

    CATEGORIES  = 'categories'
    GROUPID     = 'groupid'
    PATTERN     = 'pattern'
    TOPIC       = 'topic'
    THAT        = 'that'
    TEMPLATE    = 'template'

    def __init__(self, storage_engine):
        MongoStore.__init__(self, storage_engine)

    def collection_name(self):
        return MongoCategoryStore.CATEGORIES

    def empty_named(self, name):
        YLogger.info(self, "Emptying Category from Mongo[%s]", name)
        collection = self.collection()
        collection.delete_many({MongoCategoryStore.GROUPID, name})

    def store_category(self, groupid, userid, topic, that, pattern, template):
        YLogger.debug(self, "Storing category in Mongo [%s] [%s] [%s] [%s] [%s]", groupid, pattern, topic, that, template)
        category = Category(groupid=groupid, userid=userid, topic=topic, that=that, pattern=pattern, template=template)
        self.add_document(category)
        return True

    def load_all(self, parser):
        YLogger.info(self, "Loading all categories from Mongo")
        collection = self.collection()
        documents = collection.find()
        self._load_documents(documents, parser)

    def load_categories(self, groupid, parser):
        YLogger.info(self, "Loading categories for [%s] from Mongo", groupid)
        collection = self.collection()
        documents = collection.find({MongoCategoryStore.GROUPID: groupid})
        self._load_documents(documents, parser)

    def _load_documents(self, documents, parser):
        for doc in documents:
            category = Category.from_document(doc)
            YLogger.debug(self, "Loading category [%s] [%s] [%s] [%s] [%s]",
                                category.groupid,
                                category.pattern,
                                category.topic,
                                category.that,
                                category.template)
            self._load_category(category.groupid,
                                category.pattern,
                                category.topic,
                                category.that,
                                category.template,
                                parser)
