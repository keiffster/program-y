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
from programy.utils.console.console import outputLog


class SQLLookupsStore(SQLStore, LookupsStore):

    def __init__(self, storage_engine):
        SQLStore.__init__(self, storage_engine)
        LookupsStore.__init__(self)

    def load_all(self, collector):
        self.load(collector)

    def load(self, collector, name=None):
        db_lookups = self._get_all()
        for db_lookup in db_lookups:
            key, value = DoubleStringPatternSplitCollection.process_key_value(db_lookup.key, db_lookup.value)
            collector.add_to_lookup(key, value)

    def _get_entity(self, key, value):
        raise NotImplementedError()  # pragma: no cover

    def _exists(self, key):
        raise NotImplementedError()  # pragma: no cover

    def add_to_lookup(self, key, value, overwrite_existing=False):
        lookup = self._exists(key)
        if lookup is not None:
            if overwrite_existing is True:
                YLogger.info(self, "Updating lookup in SQL [%s] [%s]", key, value)
                lookup.value = value

            else:
                YLogger.error(self, "Existing value in SQL lookup [%s] = [%s]", key, value)
                return False

        else:
            YLogger.debug(self, "Adding lookup to SQL [%s] = [%s]", key, value)
            lookup = self._get_entity(key=key, value=value)
            self._storage_engine.session.add(lookup)

        self._storage_engine.session.commit()
        return True

    def get_lookup(self):
        all = self._get_all()
        lookups = {}
        for keyvalue in all:
            lookups[keyvalue.key] = keyvalue.value
        return lookups

    def remove_lookup_key(self, key):
        raise NotImplementedError()         # pragma: no cover

    def remove_lookup(self):
        raise NotImplementedError()         # pragma: no cover

    def split_into_fields(self, line):
        return DoubleStringPatternSplitCollection.\
            split_line_by_pattern(line, DoubleStringPatternSplitCollection.RE_OF_SPLIT_PATTERN)

    def process_line(self, name, fields, verbose=False):
        if fields and len(fields) == 2:
            result = self.add_to_lookup(fields[0].upper(), fields[1].upper())
            if verbose is True:
                outputLog(self, "Key=[%s], Value={%s]" % (fields[0].upper(), fields[1].upper()))
            return result
        return False

    def _read_lookups_from_file(self, filename, verbose):
        count = 0
        success = 0
        with open(filename, "r") as lookup_file:
            for line in lookup_file:
                line = line.strip()
                fields = self.split_into_fields(line)
                if self.process_line(None, fields, verbose) is True:
                    success += 1
                count += 1
        return count, success

    def upload_from_file(self, filename, fileformat=Store.TEXT_FORMAT, commit=True, verbose=False):
        try:
            count, success = self._read_lookups_from_file(filename, verbose)
            self.commit(commit)
            return count, success

        except Exception as e:
            YLogger.exception(None, "Failed to upload lookups from file [%s]", e, filename)

        return 0, 0

class SQLDenormalStore(SQLLookupsStore):

    def __init__(self, storage_engine):
        SQLLookupsStore.__init__(self, storage_engine)

    def empty(self):
        self._get_all().delete()

    def remove_lookup_key(self, key):
        self._storage_engine.session.query(Denormal).filter(Denormal.key == key).delete()

    def remove_lookup(self):
        self._storage_engine.session.query(Denormal).delete()

    def _get_all(self):
        return self._storage_engine.session.query(Denormal)

    def _get_entity(self, key, value):
        return Denormal(key=key, value=value)

    def _exists(self, key):
        try:
            return self._storage_engine.session.query(Denormal).filter(Denormal.key == key).one()

        except Exception:
            return None


class SQLNormalStore(SQLLookupsStore):

    def __init__(self, storage_engine):
        SQLLookupsStore.__init__(self, storage_engine)

    def _get_all(self):
        return self._storage_engine.session.query(Normal)

    def empty(self):
        self._get_all().delete()

    def remove_lookup_key(self, key):
        self._storage_engine.session.query(Normal).filter(Normal.key == key).delete()

    def remove_lookup(self):
        self._storage_engine.session.query(Normal).delete()

    def _get_entity(self, key, value):
        return Normal(key=key, value=value)

    def _exists(self, key):
        try:
            return self._storage_engine.session.query(Normal).filter(Denormal.key == key).one()

        except Exception:
            return None


class SQLGenderStore(SQLLookupsStore):

    def __init__(self, storage_engine):
        SQLLookupsStore.__init__(self, storage_engine)

    def _get_all(self):
        return self._storage_engine.session.query(Gender)

    def empty(self):
        return self._get_all().delete()

    def remove_lookup_key(self, key):
        self._storage_engine.session.query(Gender).filter(Gender.key == key).delete()

    def remove_lookup(self):
        self._storage_engine.session.query(Gender).delete()

    def _get_entity(self, key, value):
        return Gender(key=key, value=value)

    def _exists(self, key):
        try:
            return self._storage_engine.session.query(Gender).filter(Gender.key == key).one()

        except Exception:
            return None


class SQLPersonStore(SQLLookupsStore):

    def __init__(self, storage_engine):
        SQLLookupsStore.__init__(self, storage_engine)

    def _get_all(self):
        return self._storage_engine.session.query(Person)

    def empty(self):
        return self._get_all().delete()

    def remove_lookup_key(self, key):
        self._storage_engine.session.query(Person).filter(Person.key == key).delete()

    def remove_lookup(self):
        self._storage_engine.session.query(Person).delete()

    def _get_entity(self, key, value):
        return Person(key=key, value=value)

    def _exists(self, key):
        try:
            return self._storage_engine.session.query(Person).filter(Person.key == key).one()

        except Exception:
            return None


class SQLPerson2Store(SQLLookupsStore):

    def __init__(self, storage_engine):
        SQLLookupsStore.__init__(self, storage_engine)

    def _get_all(self):
        return self._storage_engine.session.query(Person2)

    def empty(self):
        return self._get_all().delete()

    def remove_lookup_key(self, key):
        self._storage_engine.session.query(Person2).filter(Person2.key == key).delete()

    def remove_lookup(self):
        self._storage_engine.session.query(Person2).delete()

    def _get_entity(self, key, value):
        return Person2(key=key, value=value)

    def _exists(self, key):
        try:
            return self._storage_engine.session.query(Person2).filter(Denormal.key == key).one()

        except Exception:
            return None
