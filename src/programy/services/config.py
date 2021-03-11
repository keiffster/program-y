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


class ServiceConfiguration:

    def __init__(self, service_type):
        self._service_type = service_type
        self._name = None
        self._category = None
        self._storage = None
        self._service_class = None
        self._default_response = None
        self._default_srai = None
        self._success_prefix = None
        self._default_aiml = None
        self._load_default_aiml = True
        self._url = None

    @staticmethod
    def from_data(service_type, name, category, storage=None, service_class=None, default_response=None, default_srai=None,
                  success_prefix=None, default_aiml=None, load_default_aiml=True, url=None):

        if service_type == 'rest':
            config = ServiceRESTConfiguration()

        elif service_type == 'wsdl':
            config = ServiceWSDLConfiguration()

        elif service_type == 'library':
            config = ServiceLibraryConfiguration()

        else:
            config = ServiceConfiguration(service_type=service_type)

        config._name = name
        config._category = category

        config._storage = storage

        config._service_class = service_class

        config._default_response = default_response
        config._default_srai = default_srai
        config._success_prefix = success_prefix

        config._default_aiml = default_aiml
        config._load_default_aiml = load_default_aiml

        config._url = url

        return config

    @property
    def service_type(self):
        return self._service_type

    @property
    def name(self):
        return self._name

    @property
    def category(self):
        return self._category

    @property
    def service_class(self):
        return self._service_class

    @property
    def storage(self):
        return self._storage

    @property
    def default_aiml(self):
        return self._default_aiml

    @property
    def load_default_aiml(self):
        return self._load_default_aiml

    @property
    def default_response(self):
        return self._default_response

    @property
    def default_srai(self):
        return self._default_srai

    @property
    def success_prefix(self):
        return self._success_prefix

    @property
    def url(self):
        return self._url

    @staticmethod
    def new_from_yaml(yaml_data, filename):

        if 'service' not in yaml_data:
            raise ValueError("'service' missing from service yaml")

        service_data = yaml_data['service']

        if 'type' in service_data:
            service_type = service_data.get('type')
            if service_type == 'rest':
                config = ServiceRESTConfiguration()

            elif service_type == 'wsdl':
                config = ServiceWSDLConfiguration()

            elif service_type == 'library':
                config = ServiceWSDLConfiguration()

            else:
                raise ValueError("Unknown service type [%s]"%service_type)

        else:
            config = ServiceConfiguration(service_type='generic')

        config.from_yaml(service_data, filename)
        return config

    def from_yaml(self, service_data, filename):

        self._name = service_data.get('name', None)
        self._category = service_data.get('category', None)

        self._storage = filename

        self._service_class = service_data.get('service_class', None)

        self._default_response = service_data.get('default_response', None)
        self._default_srai = service_data.get('default_srai', None)
        self._success_prefix = service_data.get('success_prefix', None)

        self._default_aiml = service_data.get('default_aiml', None)
        self._load_default_aiml = service_data.get('load_default_aiml', True)

        self._url = service_data.get('url', None)

    @staticmethod
    def from_sql(dao):

        if dao.type == 'rest':
            config = ServiceRESTConfiguration()

            config._retries = dao.rest_retries
            if config._retries is None:
                config._retries = ServiceRESTConfiguration.DEFAULT_RETRIES

            config._timeout = dao.rest_timeout
            if config._timeout is None:
                config._timeout = ServiceRESTConfiguration.DEFAULT_TIMEOUT

        elif dao.type == 'library':
            config = ServiceLibraryConfiguration()

        else:
            config = ServiceConfiguration(service_type=dao.type)

        config._name = dao.name
        config._category = dao.category

        config._storage = "sql"

        config._service_class = dao.service_class

        config._default_response = dao.default_response
        config._default_srai = dao.default_srai
        config._success_prefix = dao.success_prefix

        config._default_aiml = dao.default_aiml
        config._load_default_aiml = dao.load_default_aiml

        config._url = dao.url

        return config

    @staticmethod
    def from_mongo(dao):

        if dao.get('type') == 'rest':
            config = ServiceRESTConfiguration()
            rest_data = dao.get("rest", None)

            if rest_data is not None:
                config._retries = rest_data.get('retries', None)
                config._timeout = rest_data.get('timeout', None)

            if config._retries is None:
                config._retries = ServiceRESTConfiguration.DEFAULT_RETRIES

            if config._timeout is None:
                config._timeout = ServiceRESTConfiguration.DEFAULT_TIMEOUT

        elif dao.get('type')== 'library':
            config = ServiceLibraryConfiguration()

        else:
            config = ServiceConfiguration(service_type=dao.get('type'))

        config._name = dao.get('name', None)
        config._category = dao.get('category', None)

        config._storage = "mongo"

        config._service_class = dao.get('service_class', None)

        config._default_response = dao.get('default_response', None)
        config._default_srai = dao.get('default_srai', None)
        config._success_prefix = dao.get('success_prefix', None)

        config._default_aiml = dao.get('default_aiml', None)
        config._load_default_aiml = dao.get('load_default_aiml', True)

        config._url = dao.get('url', None)

        return config


class ServiceLibraryConfiguration(ServiceConfiguration):

    def __init__(self):
        ServiceConfiguration.__init__(self, service_type='library')


class ServiceRESTConfiguration(ServiceConfiguration):

    DEFAULT_RETRIES = [100, 500, 1000, 2000, 5000, 10000]
    DEFAULT_TIMEOUT = 3000

    def __init__(self):
        ServiceConfiguration.__init__(self, service_type='rest')
        self._retries = ServiceRESTConfiguration.DEFAULT_RETRIES
        self._timeout = ServiceRESTConfiguration.DEFAULT_TIMEOUT

    @property
    def retries(self):
        return self._retries

    @property
    def timeout(self):
        return self._timeout

    def from_yaml(self, service_data, filename):

        super(ServiceRESTConfiguration, self).from_yaml(service_data, filename)

        rest_data = service_data.get("rest", None)

        if rest_data is not None:

            self._retries = rest_data.get('retries', None)
            if self._retries is None:
                self._retries = ServiceRESTConfiguration.DEFAULT_RETRIES

            self._timeout = rest_data.get('timeout', None)
            if self._timeout is None:
                self._timeout = ServiceRESTConfiguration.DEFAULT_TIMEOUT


class ServiceWSDLConfiguration(ServiceConfiguration):

    def __init__(self):
        ServiceConfiguration.__init__(self, service_type='wsdl')
        self._wsdl_file = None
        self._station_codes_file = None

    @property
    def wsdl_file(self):
        return self._wsdl_file

    @property
    def station_codes_file(self):
        return self._station_codes_file

    def from_yaml(self, service_data, filename):

        super(ServiceWSDLConfiguration, self).from_yaml(service_data, filename)

        self._station_codes_file = service_data.get("station_codes_file", None)

        wsdl_data = service_data.get("wsdl", None)
        if wsdl_data is not None:
            self._wsdl_file = wsdl_data.get('wsdl_file', None)

