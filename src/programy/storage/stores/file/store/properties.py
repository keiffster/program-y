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

import os
import os.path
import re

from programy.storage.stores.file.store.filestore import FileStore
from programy.storage.entities.property import PropertyStore

class FilePropertyStore(FileStore, PropertyStore):

    SPLIT_CHAR = ':'
    COMMENT = '#'

    def __init__(self, storage_engine):
        FileStore.__init__(self, storage_engine)

    def _get_storage_path(self):
        return self._storage_engine.configuration.properties_storage.file

    def empty(self):
        props_path = self._get_storage_path()
        if os.path.exists(props_path) is True:
            os.remove(props_path)

    def empty_properties(self):
        property_filepath = self._get_storage_path()
        if os.path.exists(property_filepath):
            os.remove(property_filepath)

    def add_property(self, name, value):
        props_path = self._get_storage_path()
        properties = self._load_properties(props_path)
        properties[name] = value
        self._write_properties(props_path, properties)

    def add_properties(self, properties):
        props_path = self._get_storage_path()
        self._write_properties(props_path, properties)

    def get_properties(self):
        property_filepath = self._get_storage_path()
        properties = self._load_properties(property_filepath)
        return properties

    def _load_properties(self, property_filepath):
        properties = {}
        if os.path.exists(property_filepath):
            try:
                YLogger.debug(self, "Loading properties from [%s]", property_filepath)

                with open(property_filepath, "r") as props_file:
                    for line in props_file:
                        line = line.strip()
                        if line:
                            if line.startswith(FilePropertyStore.COMMENT) is False:
                                splits = line.split(FilePropertyStore.SPLIT_CHAR)
                                if len(splits)>1:
                                    key = splits[0].strip()
                                    val = self.process_value(splits[1:])
                                    if val is not None:
                                        properties[key] = val

            except Exception as excep:
               YLogger.exception_nostack(self, "Failed to load properties file [%s]", excep, property_filepath)

        return properties

    def process_value(self, splits):
        return (FilePropertyStore.SPLIT_CHAR.join(splits)).strip()

    def _write_properties(self, property_filepath, properties):
        try:
            with open(property_filepath, "w+") as props_file:
                for key, value in properties.items():
                    props_file.write("%s%s%s\n"%(key, FilePropertyStore.SPLIT_CHAR, value))
                props_file.write("\n")

        except Exception as excep:
            YLogger.exception_nostack(self, "Failed to write properties file [%s]", excep, property_filepath)

    def _load_file_contents(self, collection, filename):
        properties = self._load_properties(filename)
        for key, value in properties.items():
            collection.add_property(key, value)

    def get_storage(self):
        return self.storage_engine.configuration.properties_storage


class FileRegexStore(FilePropertyStore):

    def __init__(self, storage_engine):
        FilePropertyStore.__init__(self, storage_engine)

    def get_storage(self):
        return self.storage_engine.configuration.regex_storage

    def process_value(self, splits):
        try:
            pattern = (FilePropertyStore.SPLIT_CHAR.join(splits)).strip()
            return re.compile(pattern, re.IGNORECASE)
        except Exception:
            YLogger.error(self, "Invalid regex template [%s]", pattern)
            return None

    def get_regular_expressions(self):
        return self.get_properties()



class FileDefaultVariablesStore(FilePropertyStore):

    def __init__(self, storage_engine):
        FilePropertyStore.__init__(self, storage_engine)

    def get_storage(self):
        return self.storage_engine.configuration.defaults_storage

    def get_defaults_values(self):
        return self.get_properties()
