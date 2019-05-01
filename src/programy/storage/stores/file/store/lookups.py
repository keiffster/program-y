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

from programy.storage.stores.file.store.filestore import FileStore

from programy.storage.entities.lookups import LookupsStore
from programy.mappings.base import DoubleStringPatternSplitCollection


class FileLookupsStore(FileStore, LookupsStore):

    def __init__(self, storage_engine):
        FileStore.__init__(self, storage_engine)

    def _load_file_contents(self, lookup_collection, filename):
        YLogger.debug(self, "Loading lookup [%s]", filename)
        try:
            with open(filename, 'r', encoding='utf8') as my_file:
                for line in my_file:
                    if line:
                        splits = DoubleStringPatternSplitCollection.split_line_by_pattern(line, DoubleStringPatternSplitCollection.RE_OF_SPLIT_PATTERN)
                        if splits and len(splits) > 1:
                            index, pattern = self.process_key_value(splits[0].upper(), splits[1])
                            lookup_collection.add_to_lookup(index, pattern)

        except Exception as excep:
            YLogger.exception_nostack(self, "Failed to load lookup [%s]", excep, filename)


class FileDenormalStore(FileLookupsStore):

    def __init__(self, storage_engine):
        FileLookupsStore.__init__(self, storage_engine)

    def get_storage(self):
        return self.storage_engine.configuration.denormal_storage


class FileNormalStore(FileLookupsStore):

    def __init__(self, storage_engine):
        FileLookupsStore.__init__(self, storage_engine)

    def get_storage(self):
        return self.storage_engine.configuration.normal_storage


class FileGenderStore(FileLookupsStore):

    def __init__(self, storage_engine):
        FileLookupsStore.__init__(self, storage_engine)

    def get_storage(self):
        return self.storage_engine.configuration.gender_storage


class FilePersonStore(FileLookupsStore):

    def __init__(self, storage_engine):
        FileLookupsStore.__init__(self, storage_engine)

    def get_storage(self):
        return self.storage_engine.configuration.person_storage


class FilePerson2Store(FileLookupsStore):

    def __init__(self, storage_engine):
        FileLookupsStore.__init__(self, storage_engine)

    def get_storage(self):
        return self.storage_engine.configuration.person2_storage
