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
import re
import os
import os.path
from programy.utils.logging.ylogger import YLogger
from programy.storage.stores.nosql.mongo.store.mongostore import MongoStore
from programy.storage.entities.property import PropertyStore
from programy.storage.stores.nosql.mongo.dao.property import Property
from programy.mappings.base import DoubleStringPatternSplitCollection
from programy.storage.entities.store import Store


class MongoPropertyStore(PropertyStore, MongoStore):
    PROPERTIES = 'properties'
    SPLIT_CHAR = ':'
    COMMENT = '#'
    NAME = 'name'
    VALUE = 'value'

    def __init__(self, storage_engine):
        MongoStore.__init__(self, storage_engine)
        PropertyStore.__init__(self)

    def collection_name(self):
        return MongoPropertyStore.PROPERTIES

    def empty_properties(self):
        self.empty()

    def add_property(self, name, value):
        collection = self.collection()
        prop = collection.find_one({MongoPropertyStore.NAME: name})
        if prop is not None:
            prop['value'] = value
            YLogger.info(self, "Replacing property [%s] = [%s]", name, value)
            result = collection.replace_one({'_id': prop['_id']}, prop)
            return bool(result.modified_count > 0)

        prop = Property(name, value)
        YLogger.info(self, "Adding property [%s] = [%s]", name, value)
        return self.add_document(prop)

    def add_properties(self, properties):
        for name, value in properties.items():
            self.add_property(name, value)

    def get_properties(self):
        collection = self.collection()
        props_collection = collection.find()
        properties = {}
        for prop in props_collection:
            properties[prop[MongoPropertyStore.NAME]] = prop[MongoPropertyStore.VALUE]
        return properties

    def load(self, collector, name=None):
        del name
        YLogger.info(self, "Loading properties from Mongo")
        self.load_all(collector)

    def load_all(self, collector):
        YLogger.info(self, "Loading all properties from Mongo")
        collector.empty()
        collection = self.collection()
        db_propertys = collection.find()
        for db_property in db_propertys:
            self.add_to_collection(collector, db_property[MongoPropertyStore.NAME],
                                   db_property[MongoPropertyStore.VALUE])

    def add_to_collection(self, collection, name, value):
        collection.add_property(name, value)

    def _process_line(self, line, verbose):
        line = line.strip()
        if line.startswith(MongoPropertyStore.COMMENT) is False:
            splits = line.split(MongoPropertyStore.SPLIT_CHAR)
            if len(splits) > 1:
                key = splits[0].strip()
                val = ":".join(splits[1:]).strip()
                if verbose is True:
                    YLogger.debug(self, "Adding %s property [%s=%s] to Mongo",
                                  self.collection_name(), key, val)
                return self.add_property(key, val)

        return False

    def _read_lines_from_file(self, filename, verbose):
        count = 0
        success = 0
        with open(filename, "r") as vars_file:
            for line in vars_file:
                if self._process_line(line, verbose) is True:
                    success += 1
                count += 1
        return count, success

    def upload_from_file(self, filename, fileformat=Store.TEXT_FORMAT, commit=True, verbose=False):

        YLogger.info(self, "Uploading %s to Mongo from [%s]", filename, self.collection_name())

        try:
            return self._read_lines_from_file(filename, verbose)

        except Exception as excep:
            YLogger.exception(self, "Failed to upload %s from %s to Mongo", excep, self.collection_name(), filename)

        return 0, 0

    def split_into_fields(self, line):
        return DoubleStringPatternSplitCollection.split_line_by_pattern(line,
                                                                        DoubleStringPatternSplitCollection.
                                                                        RE_OF_SPLIT_PATTERN)


class MongoDefaultVariablesStore(MongoPropertyStore):
    DEFAULTS = 'defaults'

    def __init__(self, storage_engine):
        MongoPropertyStore.__init__(self, storage_engine)

    def collection_name(self):
        return MongoDefaultVariablesStore.DEFAULTS

    def add_defaults(self, defaults):
        self.add_properties(defaults)

    def get_default_values(self):
        return self.get_properties()

    def add_default(self, name, value):
        return self.add_property(name, value)


class MongoRegexesStore(MongoPropertyStore):
    REGEXES = 'regexes'

    def __init__(self, storage_engine):
        MongoPropertyStore.__init__(self, storage_engine)

    def collection_name(self):
        return MongoRegexesStore.REGEXES

    def add_regexes(self, regexes):
        self.add_properties(regexes)

    def get_regexes(self):
        return self.get_properties()

    def add_regex(self, name, regex):
        return self.add_property(name, regex)

    def add_to_collection(self, collection, name, value):
        try:
            collection.add_regex(name, re.compile(value, re.IGNORECASE))
        except Exception as excep:
            YLogger.exception(self, "Error adding regex to collection: [%s]", excep, value)
