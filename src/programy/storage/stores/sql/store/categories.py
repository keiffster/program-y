"""
Copyright (c) 2016-2020 Keith Sterling http://www.keithsterling.com

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
from programy.storage.stores.sql.store.sqlstore import SQLStore
from programy.storage.entities.category import CategoryReadWriteStore
from programy.storage.stores.sql.dao.category import Category


class SQLCategoryStore(CategoryReadWriteStore, SQLStore):

    def __init__(self, storage_engine):
        SQLStore.__init__(self, storage_engine)
        CategoryReadWriteStore.__init__(self)

    def _get_all(self):
        return self._storage_engine.session.query(Category)

    def empty(self):
        self._get_all().delete()

    def empty_named(self, name):
        self._storage_engine.session.query(Category).filter(Category.groupid == name).delete()

    def store_category(self, groupid, userid, topic, that, pattern, template):
        category = Category(groupid=groupid, userid=userid, topic=topic, that=that, pattern=pattern, template=template)
        self._storage_engine.session.add(category)
        return True

    def load(self, collector, name=None):
        del name
        self.load_all(collector)

    def load_all(self, collector):
        categories = self._storage_engine.session.query(Category)
        for category in categories:
            self._load_category(category.groupid,
                                category.pattern.strip(),
                                category.topic.strip(),
                                category.that.strip(),
                                category.template.strip(),
                                collector)

    def load_categories(self, groupid, parser):
        categories = self._storage_engine.session.query(Category).filter(Category.groupid == groupid)
        for category in categories:
            self._load_category(category.groupid,
                                category.pattern.strip(),
                                category.topic.strip(),
                                category.that.strip(),
                                category.template.strip(),
                                parser)
