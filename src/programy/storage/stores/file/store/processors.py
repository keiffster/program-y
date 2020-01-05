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
from programy.utils.classes.loader import ClassLoader
from programy.storage.stores.file.store.filestore import FileStore
from programy.storage.entities.processors import ProcessorStore


class FileProcessorsStore(FileStore, ProcessorStore):

    def __init__(self, storage_engine):
        FileStore.__init__(self, storage_engine)
        ProcessorStore.__init__(self)

    def _get_storage_path(self):
        raise NotImplementedError()  # pragma: no cover

    def get_storage(self):
        raise NotImplementedError()  # pragma: no cover

    def _process_line(self, line, collection, count):
        line = line.strip()
        if len(line) > 0:
            if line[0] != '#':
                try:
                    new_class = ClassLoader.instantiate_class(line)
                    collection.add_processor(new_class())
                    count += 1

                except Exception as error:
                    YLogger.exception(self, "Failed to load processor from file [%s]", error, line)

        return count

    def _load_file_contents(self, collection, filename):
        YLogger.debug(self, "Loading processors from file [%s]", filename)
        count = 0
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                count = self._process_line(line, collection, count)
        return count


class FilePreProcessorsStore(FileProcessorsStore):

    def __init__(self, storage_engine):
        FileProcessorsStore.__init__(self, storage_engine)

    def _get_storage_path(self):
        return self.storage_engine.configuration.preprocessors_storage.file

    def get_storage(self):
        return self.storage_engine.configuration.preprocessors_storage


class FilePostProcessorsStore(FileProcessorsStore):

    def __init__(self, storage_engine):
        FileProcessorsStore.__init__(self, storage_engine)

    def _get_storage_path(self):
        return self.storage_engine.configuration.postprocessors_storage.file

    def get_storage(self):
        return self.storage_engine.configuration.postprocessors_storage


class FilePostQuestionProcessorsStore(FileProcessorsStore):

    def __init__(self, storage_engine):
        FileProcessorsStore.__init__(self, storage_engine)

    def _get_storage_path(self):
        return self.storage_engine.configuration.postquestionprocessors_storage.file

    def get_storage(self):
        return self.storage_engine.configuration.postquestionprocessors_storage
