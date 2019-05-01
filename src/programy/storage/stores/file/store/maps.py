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

from programy.storage.entities.maps import MapsStore

class FileMapsStore(FileStore, MapsStore):

    def __init__(self, storage_engine):
        FileStore.__init__(self, storage_engine)

    def _load_file_contents(self, map_collection, filename):
        YLogger.debug(self, "Loading map [%s]", filename)

        the_map = {}
        try:
            with open(filename, 'r', encoding='utf8') as my_file:
                for line in my_file:
                    splits = line.split(":")
                    if len(splits) > 1:
                        key = splits[0].strip().upper()
                        value = ":".join(splits[1:]).strip()
                        the_map[key] = value.strip()
        except Exception as excep:
            YLogger.exception_nostack(self, "Failed to load map [%s]", excep, filename)

        map_name = self.get_just_filename_from_filepath(filename)
        map_collection.add_map(map_name, the_map, filename)

        return self.storage_engine.configuration.maps_storage

    def get_storage(self):
        return self.storage_engine.configuration.maps_storage

    def load(self, collection):
        col_store = self.get_storage()
        collection.empty()
        self._load_file_contents(collection, col_store.file)

    def reload(self, collection, map_name):
        filename = collection.storename(map_name)
        collection.empty()
        self._load_file_contents(collection, filename)
