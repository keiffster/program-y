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
import yaml
from programy.utils.logging.ylogger import YLogger
from programy.utils.classes.loader import ClassLoader
from programy.storage.stores.sql.store.sqlstore import SQLStore
from programy.storage.entities.services import ServicesStore
from programy.storage.stores.sql.dao.service import Service
from programy.storage.entities.store import Store
from programy.services.config import ServiceConfiguration
from programy.utils.console.console import outputLog


class SQLServicesStore(SQLStore, ServicesStore):

    def __init__(self, storage_engine):
        SQLStore.__init__(self, storage_engine)
        ServicesStore.__init__(self)

    def _get_all(self):
        return self._storage_engine.session.query(Service)

    def empty(self):
        self._get_all().delete()

    def get_all_services(self):
        return self._storage_engine.session.query(Service)

    def _get_entity(self, service_data):
        name = service_data.get('name')
        category = service_data.get('category')
        service_class = service_data.get('service_class')

        type = 'generic'
        rest_timeout = None
        rest_retries = None
        if 'rest' in service_data:
            type = 'rest'
            rest_data = service_data.get('rest')
            if rest_data is not None:
                rest_timeout = rest_data.get('timeout')
                rest_retries = rest_data.get('retries')

        return Service(type=type, name=name, category=category, service_class=service_class,
                       rest_timeout=rest_timeout, rest_retries=rest_retries)

    def load(self, handler, name=None):
        services = self.get_all_services()
        for service in services:
            try:
                configuration = ServiceConfiguration.from_sql(service)
                handler.add_service(service.name, ClassLoader.instantiate_class(service.service_class)(configuration))

            except Exception as e:
                YLogger.exception(self, "Failed pre-instantiating Service [%s]", e, service.service_class)

    def upload_from_file(self, filename, fileformat=Store.TEXT_FORMAT, commit=True, verbose=False):
        try:
            if self._load_services_from_file(filename, verbose) is True:
                self.commit(commit)
                return 1, 1

        except Exception as error:
            YLogger.exception(self, "Failed to load services from [%s]", error, filename)

        return 0, 0

    def _load_services_from_file(self, filename, verbose):

        with open(filename, "r+") as file:
            yaml_data = yaml.load(file, Loader=yaml.FullLoader)

            service_data = yaml_data['service']
            service = self._get_entity(service_data)
            self.storage_engine.session.add(service)

            if verbose is True:
                outputLog(self, "[%s] = [%s]" % (service_data['name'], service_data['service_class']))

        return True

