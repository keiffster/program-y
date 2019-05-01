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
from programy.storage.entities.triggers import TriggersStore


class FileTriggersStore(FileStore, TriggersStore):

    SPLIT_CHAR = ':'
    COMMENT = '#'

    def __init__(self, storage_engine):
        FileStore.__init__(self, storage_engine)

    def _get_storage_path(self):
        return self._storage_engine.configuration.triggers_storage.dirs[0]

    def empty(self):
        vars_path = self._get_storage_path()
        if os.path.exists(vars_path) is True:
            shutil.rmtree(vars_path)

    def _load_file_contents(self, trigger_collection, filename):
        if os.path.exists(filename):
            try:
                with open(filename, "r") as vars_file:
                    for line in vars_file:
                        line = line.strip()
                        if line:
                            if line.startswith(FileTriggersStore.COMMENT) is False:
                                splits = line.split(FileTriggersStore.SPLIT_CHAR)
                                if len(splits) > 1:
                                    event = splits[0].strip()
                                    classname = splits[1].strip()
                                    trigger_collection.add_trigger(event, classname)

            except Exception as e:
                YLogger.exception_nostack(None, "Failed to load triggers [%s]", e, filename)

    def get_storage(self):
        return self.storage_engine.configuration.triggers_storage
