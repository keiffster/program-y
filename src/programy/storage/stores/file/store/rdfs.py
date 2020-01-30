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
from programy.storage.entities.rdf import RDFReadOnlyStore


class FileRDFStore(FileStore, RDFReadOnlyStore):

    def __init__(self, storage_engine):
        FileStore.__init__(self, storage_engine)
        RDFReadOnlyStore.__init__(self)

    def _load_rdfs_from_file(self, filename, collection):
        with open(filename, 'r', encoding='utf8') as my_file:
            for line in my_file:
                splits = line.split(":")
                if len(splits) > 2:
                    subj = splits[0].upper()
                    pred = splits[1].upper()
                    obj = (":".join(splits[2:])).strip()
                    rdf_name = FileStore.get_just_filename_from_filepath(filename)
                    collection.add_entity(subj, pred, obj, rdf_name, filename)

    def _load_file_contents(self, collection, filename):
        YLogger.debug(self, "Loading rdf [%s]", filename)
        try:
            self._load_rdfs_from_file(filename, collection)
            return True

        except Exception as excep:
            YLogger.exception_nostack(self, "Failed to load rdf [%s]", excep, filename)

        return False

    def _get_storage_path(self):
        return self.storage_engine.configuration.rdf_storage.dirs

    def get_storage(self):
        return self.storage_engine.configuration.rdf_storage

    def reload(self, collection, rdf_name):
        filename = collection.storename(rdf_name)
        collection.empty(rdf_name)
        return self._load_file_contents(collection, filename)
