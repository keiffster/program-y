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
from programy.utils.logging.ylogger import YLogger
from programy.storage.stores.file.store.filestore import FileStore
from programy.storage.entities.sets import SetsReadOnlyStore


class FileSetsStore(FileStore, SetsReadOnlyStore):

    def __init__(self, storage_engine):
        FileStore.__init__(self, storage_engine)
        SetsReadOnlyStore.__init__(self)

    def _load_sets_from_file(self, filename, the_set):
        with open(filename, 'r', encoding='utf8') as my_file:
            for line in my_file:
                line = line.strip()
                self.add_set_values(the_set, line)

    def _load_file_contents(self, collection, filename):
        YLogger.debug(self, "Loading set [%s]", filename)
        try:
            the_set = {}
            self._load_sets_from_file(filename, the_set)
            set_name = FileStore.get_just_filename_from_filepath(filename)
            collection.add_set(set_name, the_set, filename)
            return True

        except Exception as excep:
            YLogger.exception_nostack(self, "Failed to load set [%s]", excep, filename)

        return False

    def _get_storage_path(self):
        return self.storage_engine.configuration.sets_storage.dirs

    def get_storage(self):
        return self.storage_engine.configuration.sets_storage

    def load(self, collector, name=None):
        collector.empty()
        return self._load_file_contents(collector, name)

    def reload(self, collection, set_name):
        filename = collection.storename(set_name)
        collection.empty()
        return self._load_file_contents(collection, filename)
