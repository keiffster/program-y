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
import datetime

from programy.storage.stores.file.store.filestore import FileStore
from programy.storage.entities.errors import ErrorsStore


class FileErrorsStore(FileStore, ErrorsStore):

    def __init__(self, storage_engine):
        FileStore.__init__(self, storage_engine)

    def _get_storage_path(self):
        return self.storage_engine.configuration.errors_storage.file

    def empty(self):
        filename = self._get_storage_path()
        if os.path.exists(filename) is True:
            shutil.rmtree(filename)

    def save_errors(self, errors):
        filename = self._get_storage_path()
        file_dir = self._get_dir_from_path(filename)
        self._ensure_dir_exists(file_dir)
        try:
            YLogger.debug(self, "Saving errors to [%s]", filename)

            with open(filename, "w+") as errors_file:
                errors_file.write("Error,File,Start Line,End Line\n")
                for error in errors:
                    errors_file.write("%s,%s,%s,%s\n"%(error[0],error[1],error[2],error[3]))
                errors_file.flush()

        except Exception as excep:
           YLogger.exception_nostack(self, "Failed to write errors file [%s]", excep, filename)
