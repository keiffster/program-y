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
from programy.utils.classes.loader import ClassLoader

from programy.storage.entities.store import Store
from programy.storage.stores.nosql.mongo.store.mongostore import MongoStore
from programy.storage.entities.processors import ProcessorStore
from programy.storage.stores.nosql.mongo.dao.processor import PreProcessor
from programy.storage.stores.nosql.mongo.dao.processor import PostProcessor


class MongoProcessorStore(MongoStore, ProcessorStore):

    def __init__(self, storage_engine):
        MongoStore.__init__(self, storage_engine)

    def load(self, processor_factory):
        YLogger.info(self, "Loading %s nodes from Mongo", self.collection_name())

        nodes = self.get_all_nodes()
        for node in nodes:
            try:
                processor_factory.add_processor(ClassLoader.instantiate_class(node['classname'])())

            except Exception as e:
                YLogger.exception(self, "Failed pre-instantiating Processor [%s]", e, node.node_class)

    def get_all_nodes(self):
        collection = self.collection()
        return collection.find()

    def upload_from_file(self, filename, format=Store.TEXT_FORMAT, commit=True, verbose=False):

        YLogger.info(self, "Uploading %s nodes to Mongo from [%s]", self.collection_name(), filename)
        count = 0
        success = 0
        try:
            with open(filename, "r", encoding="utf-8") as file:
                for line in file:
                    if self.process_config_line(line, verbose) is True:
                        success += 1
                    count += 1

        except FileNotFoundError:
            YLogger.error(self, "File not found [%s]", filename)

        if commit is True:
            self.commit()

        return count, success

    def process_config_line(self, line, verbose=False):
        line = line.strip()
        if line:
            if line.startswith('#') is False:
                class_name = line.strip()
                node = self._get_entity(class_name)
                self.add_document(node)
                if verbose is True:
                    YLogger.debug(self, "Uploading %s node [%s] to Mongo", self.collection_name(), class_name)
                return True
        return False

    def _get_entity(self, name, classname):
        raise NotImplementedError()


class MongoPreProcessorStore(MongoProcessorStore):

    PREPROCESSORS = 'preprocessors'

    def __init__(self, storage_engine):
        MongoProcessorStore.__init__(self, storage_engine)

    def collection_name(self):
        return MongoPreProcessorStore.PREPROCESSORS

    def _get_entity(self, classname):
        return PreProcessor(classname)


class MongoPostProcessorStore(MongoProcessorStore):

    POSTPROCESSORS = 'postprocessors'

    def __init__(self, storage_engine):
        MongoProcessorStore.__init__(self, storage_engine)

    def collection_name(self):
        return MongoPostProcessorStore.POSTPROCESSORS

    def _get_entity(self, classname):
        return PostProcessor(classname)
