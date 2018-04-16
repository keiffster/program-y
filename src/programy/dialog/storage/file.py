"""
Copyright (c) 2016-2018 Keith Sterling http://www.keithsterling.com

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
import time
from os import listdir
from os.path import isfile, join

from programy.dialog.storage.base import ConversationStorage


class ConversationFileStorage(ConversationStorage):

    def __init__(self, config):
        ConversationStorage.__init__(self, config)
        self._last_modified = None

    def empty(self):
        YLogger.debug(self, "Emptying Conversation Folder")
        try:
            if self._config._dir is not None:
                if os.path.exists(self._config._dir):
                    convo_files = [f for f in listdir(self._config._dir) if isfile(join(self._config._dir, f))]
                    for file in convo_files:
                        fullpath = self._config._dir + os.sep + file
                        YLogger.debug(self, "Removing conversation file: [%s]", fullpath)
                        os.remove(fullpath)
        except Exception as e:
            YLogger.exception(self, "Failed emptying conversation directory [%s]"%self._config._dir, e)

    def create_filename(self, clientid):
        return self._config._dir + os.sep + clientid + ".convo"

    # TODO clientid could be replaced with context
    def save_conversation(self, conversation, clientid):
        YLogger.debug(self, "Saving conversation to file")
        try:
            if self._config._dir is not None:
                if os.path.exists(self._config._dir):
                    filename = self.create_filename(clientid)
                    with open(filename, "w+", encoding="utf-8") as convo_file:
                        for name, value in conversation._properties.items():
                            convo_file.write("%s:%s\n"%(name, value))
                        convo_file.write("\n")
        except Exception as e:
            YLogger.exception(self, "Failed to save conversation for clientid [%s]"% clientid, e)

    def load_conversation(self, conversation, clientid, restore_last_topic=False):
        try:
            if self._config._dir is not None:
                if os.path.exists(self._config._dir):
                    filename = self.create_filename(clientid)
                    if os.path.exists(filename):

                        should_open = True
                        last_modified = time.ctime(os.path.getmtime(filename))
                        if self._last_modified is not None:
                            if self._last_modified >= last_modified:
                                should_open = False
                        self._last_modified = last_modified

                        if should_open is True:
                            YLogger.debug(self, "Loading Conversation from file")

                            with open(filename, "r", encoding="utf-8") as convo_file:
                                for line in convo_file:
                                    if ':' in line:
                                        splits = line.split(":")
                                        name = splits[0].strip()
                                        value = splits[1].strip()
                                        if name == "topic":
                                            if restore_last_topic is True:
                                                YLogger.debug(self, "Loading stored property [%s]=[%s] for %s", name, value, clientid)
                                                conversation._properties[name] = value
                                        else:
                                            YLogger.debug(self, "Loading stored property [%s]=[%s] for %s", name, value, clientid)
                                            conversation._properties[name] = value

        except Exception as e:
            YLogger.exception(self, "Failed to load conversation for clientid [%s]"%clientid, e)

    def remove_conversation(self, clientid):
        filename = self.create_filename(clientid)
        if os.path.exists(filename):
            YLogger.debug(self, "Removing conversation for %s", clientid)
            os.path.remove(filename)