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
from abc import ABC
from zeep import Client
from programy.services.base import Service
from programy.services.base import ServiceException


class WSDLServiceException(ServiceException):

    def __init__(self, msg):
        ServiceException.__init__(self, msg)


class WSDLService(Service, ABC):

    def __init__(self, configuration):
        Service.__init__(self, configuration)

    def create_wsdl_client(self, wsdl):
        self._client = Client(wsdl)

    def _response_to_json(self, api, response):
        raise NotImplementedError()     # pragma: no cover

    def _add_base_payload(self, data, status, started, speed):
        if started is not None:
            data['response']['started'] = started.strftime("%d/%m/%Y, %H:%M:%S")
        if speed is not None:
            data['response']['speed'] = str(speed.microseconds/1000) + "ms"
        data['response']['status'] = status
        data['response']['service'] = self.name
        data['response']['category'] = self.category

    def _create_success_payload(self, api, started, speed, response):
        data = {}
        data['response'] = {}
        self._add_base_payload(data, "success", started, speed)
        data['response']['payload'] = self._response_to_json(api, response)
        data['response']['api'] = api
        return data

    def _create_failure_payload(self, api, started, speed):
        data = {}
        data['api'] = api
        data['response'] = {}
        data['response']['api'] = api
        self._add_base_payload(data, "failure", started, speed)
        data['response']['payload'] = {}
        data['response']['payload']['type'] = 'general'
        return data

    def _create_exception_failure_payload(self, api, started, speed, err):
        data = {}
        data['response'] = {}
        data['response']['api'] = api
        self._add_base_payload(data, "failure", started, speed)
        data['response']['payload'] = {}
        data['response']['payload']['type'] = 'general'
        data['response']['payload']['error'] = str(err)
        return data

