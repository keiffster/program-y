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
import os
from programy.utils.logging.ylogger import YLogger
from programy.storage.stores.sql.store.sqlstore import SQLStore
from programy.storage.entities.lookups import LookupsStore
from programy.storage.stores.sql.dao.lookup import Denormal
from programy.storage.stores.sql.dao.lookup import Normal
from programy.storage.stores.sql.dao.lookup import Person
from programy.storage.stores.sql.dao.lookup import Person2
from programy.storage.stores.sql.dao.lookup import Gender
from programy.storage.entities.store import Store
from programy.mappings.base import DoubleStringPatternSplitCollection


class SQLLookupsStore(SQLStore, LookupsStore):

    def load_all(self, collection):
        self.load(collection)

    def load(self, collection):
        db_lookups = self._get_all()
        for db_lookup in db_lookups:
            key, value = DoubleStringPatternSplitCollection.process_key_value(db_lookup.key, db_lookup.value)
            collection.add_to_lookup(key, value)

    def _get_all(self):
        raise NotImplementedError()

    def _get_entity(self, key, value):
        raise NotImplementedError()

    def _exists(self, key):
        raise NotImplementedError()

    def add(self, key, value, overwrite_existing=False):
        lookup = self._get_entity(key=key, value=value)
        if self._exists(key):
            if overwrite_existing:
                YLogger.info(self, "Updating lookup in SQL [%s] [%s]", key, value)
                lookup.value = value
                self._storage_engine.session.commit()
            else:
                YLogger.error(self, "Existing value in SQL lookup [%s] = [%s]", key, value)
                return False
        else:
            YLogger.debug(self, "Adding lookup to SQL [%s] = [%s]", key, value)
            self._storage_engine.session.add(lookup)

        return True

    def split_into_fields(self, line):
        return DoubleStringPatternSplitCollection.split_line_by_pattern(line, DoubleStringPatternSplitCollection.RE_OF_SPLIT_PATTERN)

    def process_line(self, fields, verbose=False):
        if fields and len(fields) == 2:
            result = self.add(fields[0].upper(), fields[1].upper())
            if verbose is True:
                print(fields[0].upper(), fields[1].upper())
            return result
        return False

    def upload_from_file(self, filename, format=Store.TEXT_FORMAT, commit=True, verbose=False):

        count = 0
        success = 0

        if os.path.exists(filename):
            try:
                with open(filename, "r") as lookup_file:
                    for line in lookup_file:
                        line = line.strip()
                        if line:
                            fields = self.split_into_fields(line)
                            if self.process_line(fields, verbose) is True:
                                success += 1
                        count += 1

                if commit is True:
                    self.commit()

            except Exception as e:
                YLogger.exception(None, "Failed to upload lookups from file [%s]", e, filename)

        return count, success

class SQLDenormalStore(SQLLookupsStore):

    def empty(self):
        self._storage_engine.session.query(Denormal).delete()

    def _get_all(self):
        return self._storage_engine.session.query(Denormal)

    def _get_entity(self, key, value):
        return Denormal(key=key, value=value)

    def _exists(self, key):
        try:
            self._storage_engine.session.query(Denormal).filter(Denormal.key==key).one()
            return True
        except Exception as e:
            print (e)
        return False


class SQLNormalStore(SQLLookupsStore):

    def empty(self):
        self._storage_engine.session.query(Normal).delete()

    def _get_all(self):
        return self._storage_engine.session.query(Normal)

    def _get_entity(self, key, value):
        return Normal(key=key, value=value)

    def _exists(self, key):
        try:
            self._storage_engine.session.query(Normal).filter(Denormal.key==key).one()
            return True
        except Exception as e:
            print (e)
        return False


class SQLGenderStore(SQLLookupsStore):

    def empty(self):
        self._storage_engine.session.query(Gender).delete()

    def _get_all(self):
        return self._storage_engine.session.query(Gender)

    def _get_entity(self, key, value):
        return Gender(key=key, value=value)

    def _exists(self, key):
        try:
            self._storage_engine.session.query(Normal).filter(Gender.key==key).one()
            return True
        except Exception as e:
            print (e)
        return False


class SQLPersonStore(SQLLookupsStore):

    def empty(self):
        self._storage_engine.session.query(Person).delete()

    def _get_all(self):
        return self._storage_engine.session.query(Person)

    def _get_entity(self, key, value):
        return Person(key=key, value=value)

    def _exists(self, key):
        try:
            self._storage_engine.session.query(Normal).filter(Person.key==key).one()
            return True
        except Exception as e:
            print (e)
        return False


class SQLPerson2Store(SQLLookupsStore):

    def empty(self):
        self._storage_engine.session.query(Person2).delete()

    def _get_all(self):
        return self._storage_engine.session.query(Person2)

    def _get_entity(self, key, value):
        return Person2(key=key, value=value)

    def _exists(self, key):
        try:
            self._storage_engine.session.query(Person2).filter(Denormal.key==key).one()
            return True
        except Exception as e:
            print (e)
        return False
