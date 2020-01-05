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
import os
import os.path
import shutil
from programy.utils.logging.ylogger import YLogger
from programy.storage.stores.file.store.filestore import FileStore
from programy.storage.entities.triggers import TriggersStore


class FileTriggersStore(FileStore, TriggersStore):
    SPLIT_CHAR = ':'
    COMMENT = '#'

    def __init__(self, storage_engine):
        FileStore.__init__(self, storage_engine)
        TriggersStore.__init__(self)

    def _get_storage_path(self):
        return self._storage_engine.configuration.triggers_storage.dirs[0]

    def get_storage(self):
        return self.storage_engine.configuration.triggers_storage

    def _process_line(self, line, collection):
        line = line.strip()
        if line.startswith(FileTriggersStore.COMMENT) is False:
            splits = line.split(FileTriggersStore.SPLIT_CHAR)
            if len(splits) > 1:
                event = splits[0].strip()
                classname = splits[1].strip()
                collection.add_trigger(event, classname)
                return True

        return False

    def _load_triggers_from_file(self, filename, collection):
        with open(filename, "r") as vars_file:
            for line in vars_file:
                self._process_line(line, collection)

    def _load_file_contents(self, collection, filename):
        try:
            self._load_triggers_from_file(filename, collection)
            return True

        except Exception as e:
            YLogger.exception_nostack(None, "Failed to load triggers [%s]", e, filename)

        return False