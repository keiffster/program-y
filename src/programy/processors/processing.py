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
from abc import ABCMeta, abstractmethod

from programy.utils.classes.loader import ClassLoader
from programy.storage.factory import StorageFactory


class ProcessorCollection(object):

    def __init__(self):
        ClassLoader.__init__(self)
        self._processors = []

    @property
    def processors(self):
        return self._processors

    def empty(self):
        self.processors.clear()

    def add_processor(self, processor):
        self._processors.append(processor)

    def process(self, client_context, word_string):
        for processor in self._processors:
            word_string = processor.process(client_context, word_string)
        return word_string

    def load(self, storage_factory):
        storage_name = self._get_storage_name()
        if storage_factory.entity_storage_engine_available(storage_name) is True:
            storage_engine = storage_factory.entity_storage_engine(storage_name)
            processor_store = self._get_store(storage_engine)
            processor_store.load(self)

    def _get_storage_name(self):
        raise NotImplementedError("Override this in derived class, return StorageFactory.XXX name")

    def _get_store(self, storage_engine):
        raise NotImplementedError("Override this in derived class, return Store from StorageEngine")


class PreProcessorCollection(ProcessorCollection):

    def __init__(self):
        ProcessorCollection.__init__(self)

    def _get_storage_name(self):
        return StorageFactory.PREPROCESSORS

    def _get_store(self, storage_engine):
        return storage_engine.preprocessors_store()


class PostProcessorCollection(ProcessorCollection):

    def __init__(self):
        ProcessorCollection.__init__(self)

    def _get_storage_name(self):
        return StorageFactory.POSTPROCESSORS

    def _get_store(self, storage_engine):
        return storage_engine.postprocessors_store()


##################################################################
#
class Processor:
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def process(self, client_context, word_string):
        pass


##################################################################
#
class PreProcessor(Processor):

    def __init__(self):
        Processor.__init__(self)

    @abstractmethod
    def process(self, client_context, word_string):
        pass


##################################################################
#
class PostProcessor(Processor):
    def __init__(self):
        Processor.__init__(self)

    @abstractmethod
    def process(self, client_context, word_string):
        pass
