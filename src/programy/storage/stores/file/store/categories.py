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
from programy.storage.entities.category import CategoryStore


class FileCategoryStore(FileStore, CategoryStore):

    def __init__(self, storage_engine):
        FileStore.__init__(self, storage_engine)

    def get_storage(self):
        return self.storage_engine.configuration.categories_storage

    def load_all(self, parser):
        dirs    = self.storage_engine.configuration.categories_storage.dirs
        cat_ext = self.storage_engine.configuration.categories_storage.extension
        subdirs = self.storage_engine.configuration.categories_storage.subdirs

        if self.storage_engine.configuration.categories_storage.has_single_file():
            for filename in dirs:
                if cat_ext is not None:
                    if filename.endswith(cat_ext):
                        self._load_file_contents(parser, filename)
                else:
                    self._load_file_contents(parser, filename)
        else:
            for cat_dir in dirs:
                if subdirs is False:
                    paths = os.listdir(cat_dir)
                    for filename in paths:
                        if filename.endswith(cat_ext):
                            self._load_file_contents(parser, os.path.join(cat_dir, filename))
                else:
                    for dirpath, _, filenames in os.walk(cat_dir):
                        for filename in [f for f in filenames if f.endswith(cat_ext)]:
                            self._load_file_contents(parser, os.path.join(dirpath, filename))

    def load(self, parser, category_fullname):
        self._load_file_contents(parser, category_fullname)

    def _load_file_contents(self, parser, filename):
        YLogger.debug(self, "Loading file contents from [%s]", filename)
        try:
            parser.parse_from_file(filename, userid="*")
        except Exception as excep:
            YLogger.exception_nostack(self, "Failed to load cat [%s]", excep, filename)
