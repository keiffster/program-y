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
import os.path
import re
from programy.utils.logging.ylogger import YLogger
from programy.storage.stores.sql.store.sqlstore import SQLStore
from programy.storage.entities.property import PropertyStore
from programy.storage.stores.sql.dao.property import Property
from programy.storage.stores.sql.dao.property import DefaultVariable
from programy.storage.stores.sql.dao.property import Regex
from programy.mappings.base import DoubleStringPatternSplitCollection
from programy.storage.entities.store import Store


class SQLBasePropertyStore(SQLStore, PropertyStore):
    SPLIT_CHAR = ':'
    COMMENT = '#'

    def __init__(self, storage_engine):
        SQLStore.__init__(self, storage_engine)
        PropertyStore.__init__(self)

    def empty(self):
        self._get_all().delete()

    def empty_properties(self):
        self._get_all().delete()

    def _get_entity(self, name, value):
        raise NotImplementedError()  # pragma: no cover

    def add_property(self, name, value):
        prop = self._get_entity(name=name, value=value)
        self._storage_engine.session.add(prop)
        return True

    def add_properties(self, properties):
        prop_list = []
        for name, value in properties.items():
            prop_list.append(self._get_entity(name=name, value=value))
        self._storage_engine.session.add_all(prop_list)
        return True

    def get_properties(self):
        db_properties = self._get_all()
        properties = {}
        for prop in db_properties:
            properties[prop.name] = prop.value
        return properties

    def load(self, collector, name=None):
        del name
        self.load_all(collector)

    def load_all(self, collector):
        collector.empty()
        db_propertys = self._get_all()
        for db_property in db_propertys:
            self.add_to_collection(collector, db_property.name, db_property.value)

    def add_to_collection(self, collection, name, value):
        collection.add_property(name, value)

    def split_into_fields(self, line):
        return DoubleStringPatternSplitCollection.\
            split_line_by_pattern(line, DoubleStringPatternSplitCollection.RE_OF_SPLIT_PATTERN)

    def _read_lines_from_file(self, filename, verbose):
        count = 0
        success= 0
        with open(filename, "r") as vars_file:
            for line in vars_file:
                line = line.strip()
                if line.startswith(SQLBasePropertyStore.COMMENT) is False:
                    splits = line.split(SQLBasePropertyStore.SPLIT_CHAR)
                    if len(splits) > 1:
                        key = splits[0].strip()
                        val = ":".join(splits[1:]).strip()
                        self.add_property(key, val)
                        success += 1
                count += 1

        return count, success

    def upload_from_file(self, filename, fileformat=Store.TEXT_FORMAT, commit=True, verbose=False):
        try:
            count, success = self._read_lines_from_file(filename, verbose)

            self.commit(commit)

            return count, success

        except Exception as error:
            YLogger.exception(self, "Failed to load properties from [%s]", error, filename)

        return 0, 0


class SQLPropertyStore(SQLBasePropertyStore, PropertyStore):

    def __init__(self, storage_engine):
        SQLBasePropertyStore.__init__(self, storage_engine)

    def _get_all(self):
        return self._storage_engine.session.query(Property)

    def _get_entity(self, name, value):
        return Property(name=name, value=value)


class SQLDefaultVariableStore(SQLBasePropertyStore, PropertyStore):

    def __init__(self, storage_engine):
        SQLBasePropertyStore.__init__(self, storage_engine)

    def _get_all(self):
        return self._storage_engine.session.query(DefaultVariable)

    def _get_entity(self, name, value):
        return DefaultVariable(name=name, value=value)

    def add_default(self, name, value):
        return self.add_property(name, value)

    def add_defaults(self, defaults):
        self.add_properties(defaults)

    def get_default_values(self):
        return self.get_properties()


class SQLRegexStore(SQLBasePropertyStore, PropertyStore):

    def __init__(self, storage_engine):
        SQLBasePropertyStore.__init__(self, storage_engine)

    def _get_all(self):
        return self._storage_engine.session.query(Regex)

    def _get_entity(self, name, value):
        return Regex(name=name, value=value)

    def add_regex(self, name, value):
        return self.add_property(name, value)

    def add_regexes(self, defaults):
        self.add_properties(defaults)

    def get_regexes(self):
        return self.get_properties()

    def add_to_collection(self, collection, name, value):
        try:
            collection.add_regex(name, re.compile(value, re.IGNORECASE))

        except Exception as excep:
            YLogger.exception_nostack(self, "Error adding regex to collection: [%s]" % value, excep)
