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
from programy.utils.logging.ylogger import YLogger
from programy.storage.stores.file.store.filestore import FileStore
from programy.storage.entities.oobs import OOBsStore
from programy.utils.classes.loader import ClassLoader


class FileOOBStore(FileStore, OOBsStore):

    def __init__(self, storage_engine):
        FileStore.__init__(self, storage_engine)
        OOBsStore.__init__(self)

    def _get_storage_path(self):
        return self.storage_engine.configuration.oobs_storage.file

    def get_storage(self):
        return self.storage_engine.configuration.oobs_storage

    def _load_file_contents(self, collection, filename):
        YLogger.debug(self, "Loading oobs from file [%s]", filename)
        count = 0
        try:
            with open(filename, "r", encoding="utf-8") as file:
                for line in file:
                    line = line.strip()
                    if line:
                        if self._process_line(collection, line, filename) is True:
                            count += 1

        except Exception as error:
            YLogger.exception(self, "Error loading OOB config file [%s]", error, filename)

        return count

    def _process_line(self, oob_handler, line, filename):
        if self.valid_config_line(line, filename):

            splits = line.split("=")
            oob_name = splits[0].strip()
            if oob_name in oob_handler.oobs:
                YLogger.error(self, "OOB already exists in config [%s]", line)
                return False

            class_name = splits[1].strip()
            YLogger.debug(self, "Pre-instantiating OOB [%s]", class_name)
            try:
                oob_handler.add_oob(oob_name, ClassLoader.instantiate_class(class_name)())
                return True

            except Exception as e:
                YLogger.exception_nostack(self,
                                          "Failed pre-instantiating OOB [%s]" % e, class_name)

        return False

    def valid_config_line(self, line, filename):

        if not line:
            return False

        if line.startswith('#'):
            return False

        if "=" not in line:
            YLogger.error(self, "Config line missing '=' [%s] in [%s]", line, filename)
            return False

        return True
