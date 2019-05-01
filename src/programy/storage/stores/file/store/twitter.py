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
from programy.storage.entities.twitter import TwitterStore


class FileTwitterStore(FileStore, TwitterStore):

    def __init__(self, storage_engine):
        FileStore.__init__(self, storage_engine)

    def empty(self):
        if os.path.exists(self.storage_engine.configuration.twitter_storage.dirs[0]) is True:
            shutil.rmtree(self.storage_engine.configuration.twitter_storage.dirs[0])

    def _twitter_filename(self, storage_dir, ext='ids'):
        return storage_dir + os.sep + "twitter." + ext

    def store_last_message_ids(self, last_direct_message_id, last_status_id):
        self._ensure_dir_exists(self.storage_engine.configuration.twitter_storage.dirs[0])
        twitter_ids_file = self._twitter_filename(self.storage_engine.configuration.twitter_storage.dirs[0])
        try:
            with open(twitter_ids_file, "w+", encoding="utf-8") as idfile:
                idfile.write("%s\n" % last_direct_message_id)
                idfile.write("%s\n" % last_status_id)

        except Exception as e:
            YLogger.exception_nostack(None, "Failed to store last message ids [%s]", e, twitter_ids_file)

    def load_last_message_ids(self):
        self._ensure_dir_exists(self.storage_engine.configuration.twitter_storage.dirs[0])
        last_direct_message_id = "-1"
        last_status_id = "-1"
        twitter_ids_file = self._twitter_filename(self.storage_engine.configuration.twitter_storage.dirs[0])
        try:
            with open(twitter_ids_file, "r", encoding="utf-8") as idfile:
                last_direct_message_id = idfile.readline().strip()
                last_status_id = idfile.readline().strip()

        except Exception as e:
            YLogger.exception_nostack(None, "Failed to load last message ids [%s]", e, twitter_ids_file)

        return last_direct_message_id, last_status_id

