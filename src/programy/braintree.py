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
from programy.config.brain.braintree import BrainBraintreeConfiguration

class BraintreeManager(object):

    def __init__(self, braintree_configuration, admin_user="system"):

        assert (braintree_configuration is not None)
        assert (isinstance(braintree_configuration, BrainBraintreeConfiguration))

        self._configuration = braintree_configuration
        self._save_as_user = self._configuration.save_as_user

    def dump_brain_tree(self, client_context):

        if self._configuration.create is True:
            YLogger.debug(self, "Dumping AIML Graph as tree to [%s]", self._configuration.file)

            if client_context.client.storage_factory.entity_storage_engine_available(StorageFactory.BRAINTREE) is True:
                storage_engine = client_context.client.storage_factory.entity_storage_engine(StorageFactory.BRAINTREE)
                braintree_storage = storage_engine.braintree_storage()
                braintree_storage.save_braintree(client_context)
