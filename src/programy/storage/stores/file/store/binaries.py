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

from programy.storage.stores.file.store.filestore import FileStore
from programy.storage.entities.binaries import BinariesStore
try:
    import _pickle as pickle
except:
    import pickle
import gc
import datetime

class FileBinariesStore(FileStore, BinariesStore):

    def __init__(self, storage_engine):
        FileStore.__init__(self, storage_engine)

    def _get_storage_path(self):
        return self.storage_engine.configuration.binaries_storage.file

    def save_binary(self, aiml_parser):
        try:
            bin_file_path = self._get_storage_path()
            YLogger.info(self, "Saving binary brain to [%s]", bin_file_path)
            bin_file_dir = self._get_dir_from_path(bin_file_path)

            self._ensure_dir_exists(bin_file_dir)
            start = datetime.datetime.now()

            with open(bin_file_path, "wb") as bin_file:
                pickle.dump(aiml_parser, bin_file)
                bin_file.close()

            stop = datetime.datetime.now()
            diff = stop - start
            YLogger.info(self, "Brain save took a total of %.2f sec", diff.total_seconds())

        except Exception as excep:
            YLogger.exception_nostack(self, "Failed to save binary file", excep)

    def load_binary(self):
        try:
            bin_file_path = self._get_storage_path()
            YLogger.info(self, "Loading binary brain from [%s]", bin_file_path)

            start = datetime.datetime.now()
            gc.disable()

            with open(bin_file_path, "rb") as bin_file:
                aiml_parser = pickle.load(bin_file)
                bin_file.close()

            gc.enable()

            stop = datetime.datetime.now()
            diff = stop - start
            YLogger.info(self, "Brain load took a total of %.2f sec", diff.total_seconds())
            return aiml_parser

        except Exception as excep:
            YLogger.exception_nostack(self, "Failed to load binary file", excep)
            return None

