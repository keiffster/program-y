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
from programy.storage.factory import StorageFactory

class BinariesManager(object):

    def __init__(self, binaries_configuration):

        assert (binaries_configuration is not None)

        self._configuration = binaries_configuration

    def load_binary(self, storage_factory):
        YLogger.info(self, "Loading binary brain from [%s]", StorageFactory.BINARIES)
        try:

            storage_engine = storage_factory.entity_storage_engine(self._configuration.storage)
            binaries_storage = storage_engine.binaries_storage()
            self._aiml_parser = binaries_storage.load_binary()

            return False   # Tell caller, load succeeded and skip aiml load

        except Exception as excep:
            YLogger.exception(self, "Failed to load binary file", excep)
            if self._configuration.load_aiml_on_binary_fail is True:
                return True   # Tell caller, load failed and to load aiml directly
            else:
                raise excep

    def save_binary(self, storage_factory):
        try:
            if storage_factory.entity_storage_engine_available(StorageFactory.BINARIES) is True:
                YLogger.info(self, "Saving binary brain to [%s]", StorageFactory.BINARIES)

                storage_engine = storage_factory.entity_storage_engine(StorageFactory.BINARIES)
                binaries_storage = storage_engine.binaries_storage()
                binaries_storage.save_binary(self._aiml_parser)

        except Exception as failure:
            YLogger.info(self, "Failed to save binary [%s]", failure)

