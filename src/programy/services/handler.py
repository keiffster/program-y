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
from programy.utils.classes.loader import ClassLoader


class ServiceHandler:

    def __init__(self):
        self._services = {}
        self._client = None

    @property
    def services(self):
        return self._services

    def add_service(self, name, service_class):
        self._services[name] = service_class

    def empty(self):
        self._services.clear()

    def get_service(self, service):
        if service in self._services:
            return self._services[service]

        raise ValueError("No service named [%s]"%service)

    def load_services(self, client):
        YLogger.debug(self, "Loading services")
        self._client = client
        if client.storage_factory.entity_storage_engine_available(StorageFactory.SERVICES) is True:
            storage_engine = client.storage_factory.entity_storage_engine(StorageFactory.SERVICES)
            services_store = storage_engine.services_store()
            services_store.load_all(self)
        else:
            YLogger.error(None, "No storage engine available for services!")

    def load_service(self, configuration):
        # First instantiate the service object
        YLogger.debug(self, "Loading service: [%s]", configuration.name)
        self._services[configuration.name] = ClassLoader.instantiate_class(configuration.service_class)(configuration)
        self._services[configuration.name].initialise(self._client)

    def post_initialise(self, brain):
        for service in self._services.values():
            service.load_default_aiml(brain.aiml_parser)

        return True
