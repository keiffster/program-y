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
import shutil

from programy.storage.stores.file.store.filestore import FileStore
from programy.storage.entities.duplicates import DuplicatesStore


class FileDuplicatesStore(FileStore, DuplicatesStore):

    def __init__(self, storage_engine):
        FileStore.__init__(self, storage_engine)

    def _get_storage_path(self):
        return self.storage_engine.configuration.duplicates_storage.file

    def empty(self):
        filename = self._get_storage_path()
        if os.path.exists(filename) is True:
            shutil.rmtree(filename)

    def save_duplicates(self, duplicates):
        filename = self._get_storage_path()
        file_dir = self._get_dir_from_path(filename)
        self._ensure_dir_exists(file_dir)

        try:
            YLogger.debug(self, "Saving duplicates to [%s]", filename)

            with open(filename, "w+") as duplicates_file:
                duplicates_file.write("Duplicate\tFile\tStart Line\tEnd Line")
                for duplicate in duplicates:
                    duplicates_file.write("%s\t%s\t%s\t%s\n" % (duplicate[0], duplicate[1], duplicate[2], duplicate[3]))
                duplicates_file.flush()

        except Exception as excep:
           YLogger.exception_nostack(self, "Failed to write duplicates file [%s]", excep, filename)
