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
from programy.storage.stores.sql.store.sqlstore import SQLStore
from programy.storage.entities.lookups import LookupsStore
from programy.storage.stores.sql.dao.lookup import Denormal
from programy.storage.stores.sql.dao.lookup import Normal
from programy.storage.stores.sql.dao.lookup import Person
from programy.storage.stores.sql.dao.lookup import Person2
from programy.storage.stores.sql.dao.lookup import Gender


class SQLLookupsStore(SQLStore, LookupsStore):

    def load_all(self, lookup_collection):
        lookup_collection.empty()
        db_lookups = self._get_all()
        for db_lookup in db_lookups:
            lookup_collection.add_to_lookup(db_lookup.key,  db_lookup.value)

    def split_into_fields(self, line):
        pass

    def process_line(self, name, fields):
        pass


class SQLDenormalStore(SQLLookupsStore):

    def empty(self):
        self._storage_engine.session.query(Denormal).delete()

    def _get_all(self):
        return self._storage_engine.session.query(Denormal)


class SQLNormalStore(SQLLookupsStore):

    def empty(self):
        self._storage_engine.session.query(Normal).delete()

    def _get_all(self):
        return self._storage_engine.session.query(Normal)


class SQLGenderStore(SQLLookupsStore):

    def empty(self):
        self._storage_engine.session.query(Gender).delete()

    def _get_all(self):
        return self._storage_engine.session.query(Gender)


class SQLPersonStore(SQLLookupsStore):

    def empty(self):
        self._storage_engine.session.query(Person).delete()

    def _get_all(self):
        return self._storage_engine.session.query(Person)


class SQLPerson2Store(SQLLookupsStore):

    def empty(self):
        self._storage_engine.session.query(Person2).delete()

    def _get_all(self):
        return self._storage_engine.session.query(Person2)
