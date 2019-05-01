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
from programy.storage.entities.conversation import ConversationStore
import json


class FileConversationStore(FileStore, ConversationStore):

    def __init__(self, storage_engine):
        FileStore.__init__(self, storage_engine)

    def empty(self):
        if os.path.exists(self._storage_engine.configuration.conversation_storage.dirs[0]) is True:
            shutil.rmtree(self._storage_engine.configuration.conversation_storage.dirs[0])

    def _conversations_filename(self, storage_dir, clientid, userid, ext="conv"):
        return "%s%s%s_%s.%s"%(storage_dir, os.sep, clientid, userid, ext)

    def store_conversation(self, client_context, conversation):
        self._ensure_dir_exists(self._storage_engine.configuration.conversation_storage.dirs[0])

        conversation_filepath = self._conversations_filename(self._storage_engine.configuration.conversation_storage.dirs[0], client_context.client.id, client_context.userid)

        YLogger.debug(self, "Writing conversation to [%s]", conversation_filepath)

        convo_json = conversation.to_json ()
        json_text = json.dumps(convo_json, indent=4)

        try:
            with open(conversation_filepath, "w+") as convo_file:
                convo_file.write(json_text)

        except Exception as excep:
            YLogger.exception_nostack(self, "Failed to write conversation file [%s]", excep, conversation_filepath)

    def load_conversation(self, client_context, conversation):
        conversation_filepath = self._conversations_filename(self._storage_engine.configuration.conversation_storage.dirs[0], client_context.client.id, client_context.userid)

        if self._file_exists(conversation_filepath):
            try:
                with open(conversation_filepath, "r+") as convo_file:
                    json_text = convo_file.read()
                    json_data = json.loads(json_text)
                    conversation.from_json(client_context, json_data)

            except Exception as excep:
                YLogger.exception_nostack(self, "Failed to read conversation file [%s]", excep, conversation_filepath)
