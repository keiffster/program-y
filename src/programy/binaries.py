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
from programy.storage.factory import StorageFactory


class BinariesManager:

    def __init__(self, binaries_configuration):
        assert binaries_configuration is not None

        self._configuration = binaries_configuration

    def _load_from_storage(self, storage_factory):
        storage_engine = storage_factory.entity_storage_engine(StorageFactory.BINARIES)
        binaries_storage = storage_engine.binaries_store()
        return binaries_storage.load_binary()

    def load_binary(self, storage_factory):
        try:
            if storage_factory.entity_storage_engine_available(StorageFactory.BINARIES) is True:
                YLogger.info(self, "Loading binary brain from [%s]", StorageFactory.BINARIES)

                return self._load_from_storage(storage_factory)

        except Exception as excep:
            YLogger.exception(self, "Failed to load binary file", excep)
            if self._configuration.load_aiml_on_binary_fail is False:
                raise excep

        return None

    def _save_to_storage(self, storage_factory, aiml_parser):
        storage_engine = storage_factory.entity_storage_engine(StorageFactory.BINARIES)
        binaries_storage = storage_engine.binaries_store()
        binaries_storage.save_binary(aiml_parser)

    def save_binary(self, storage_factory, aiml_parser):
        try:
            if storage_factory.entity_storage_engine_available(StorageFactory.BINARIES) is True:
                YLogger.info(self, "Saving binary brain to [%s]", StorageFactory.BINARIES)

                self._save_to_storage(storage_factory, aiml_parser)
                return True

        except Exception as failure:
            YLogger.info(self, "Failed to save binary [%s]", failure)

        return False