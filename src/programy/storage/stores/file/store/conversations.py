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
import json
from programy.utils.logging.ylogger import YLogger
from programy.storage.stores.file.store.filestore import FileStore
from programy.storage.entities.conversation import ConversationStore


class FileConversationStore(FileStore, ConversationStore):

    def __init__(self, storage_engine):
        FileStore.__init__(self, storage_engine)
        ConversationStore.__init__(self)

    def _get_storage_path(self):
        return self.storage_engine.configuration.conversation_storage.file

    def get_storage(self):
        return self.storage_engine.configuration.conversation_storage

    def empty(self):
        if os.path.exists(self._storage_engine.configuration.conversation_storage.dirs[0]) is True:
            shutil.rmtree(self._storage_engine.configuration.conversation_storage.dirs[0])

    def _conversations_filename(self, storage_dir, clientid, userid, ext="conv"):
        return "%s%s%s_%s.%s" % (storage_dir, os.sep, clientid, userid, ext)

    def _write_file(self, conversation_filepath, json_text):
        with open(conversation_filepath, "w+") as convo_file:
            convo_file.write(json_text)

    def store_conversation(self, client_context, conversation, commit=True):
        self._ensure_dir_exists(self._storage_engine.configuration.conversation_storage.dirs[0])

        conversation_filepath = self._conversations_filename(
            self._storage_engine.configuration.conversation_storage.dirs[0], client_context.client.id,
            client_context.userid)

        YLogger.debug(self, "Writing conversation to [%s]", conversation_filepath)

        convo_json = conversation.to_json()
        json_text = json.dumps(convo_json, indent=4)

        try:
            self._write_file(conversation_filepath, json_text)

        except Exception as excep:
            YLogger.exception_nostack(self, "Failed to write conversation file [%s]", excep, conversation_filepath)

    def _read_file(self, conversation_filepath, conversation):
        with open(conversation_filepath, "r+") as convo_file:
            json_text = convo_file.read()
            json_data = json.loads(json_text)
            conversation.create_from_json(json_data)

    def load_conversation(self, client_context, conversation):
        conversation_filepath = self._conversations_filename(
            self._storage_engine.configuration.conversation_storage.dirs[0], client_context.client.id,
            client_context.userid)

        if self._file_exists(conversation_filepath):
            try:
                self._read_file(conversation_filepath, conversation)
                return True

            except Exception as excep:
                YLogger.exception_nostack(self, "Failed to read conversation file [%s]", excep, conversation_filepath)

        return False