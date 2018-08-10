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
from programy.utils.classes.loader import ClassLoader

from programy.storage.stores.sql.store.sqlstore import SQLStore
from programy.storage.entities.processors import ProcessorStore
from programy.storage.stores.sql.dao.processor import PreProcessor
from programy.storage.stores.sql.dao.processor import PostProcessor


class SQLProcessorsStore(SQLStore, ProcessorStore):

    def _get_storage_class(self):
        pass

    def load(self, processor_factory):
        processors = self.get_all_processors()
        for processor in processors:
            try:
                processor_factory.add_processor(processor.name, ClassLoader.instantiate_class(processor.processor_class))
            except Exception as e:
                YLogger.exception(self, "Failed pre-instantiating %s Processor [%s]"%(processor_factory.type, processor.processor_class), e)


class SQLPreProcessorsStore(SQLProcessorsStore, ProcessorStore):

    def empty(self):
        self._storage_engine.session.query(PreProcessor).delete()

    def get_all_processors(self):
        return self._storage_engine.session.query(PreProcessor)


class SQLPostProcessorsStore(SQLProcessorsStore, ProcessorStore):

    def empty(self):
        self._storage_engine.session.query(PostProcessor).delete()

    def get_all_processors(self):
        return self._storage_engine.session.query(PostProcessor)

