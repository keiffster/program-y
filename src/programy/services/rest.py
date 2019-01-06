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
import requests

from programy.services.service import Service
from programy.config.brain.service import BrainServiceConfiguration


class RestAPI(object):

    def get(self, url):
        return requests.get(url)

    def post(self, url, data):
        return requests.post(url, data=data)


class GenericRESTService(Service):

    def __init__(self, config: BrainServiceConfiguration, api=None):
        Service.__init__(self, config)

        if api is None:
            self.api = RestAPI()
        else:
            self.api = api

        if config.method is None:
            self.method = "GET"
        else:
            self.method = config.method

        if config.host is None:
            raise Exception("Undefined host parameter")
        self.host = config.host

        self.port = None
        if config.port is not None:
           self.port = config.port

        self.url = None
        if config.url is not None:
           self.url = config.url

    def _format_url(self):
        if self.port is not None:
            host_port = "http://%s:%s"%(self.host, self.port)
        else:
            host_port = "http://%s"%self.host

        if self.url is not None:
            return "%s%s"%(host_port, self.url)
        else:
            return host_port

    def _format_payload(self, client_context, question):
        return {}

    def _format_get_url(self, url, client_context, question):
        return url

    def _parse_response(self, text):
        return text

    def ask_question(self, client_context, question: str):

        try:
            url = self._format_url()

            if self.method == 'GET':
                full_url = self._format_get_url(url, client_context, question)
                response = self.api.get(full_url)
            elif self.method == 'POST':
                payload = self._format_payload(client_context, question)
                response = self.api.post(url, data=payload)
            else:
                raise Exception("Unsupported REST method [%s]"%self.method)

            if response.status_code != 200:
                YLogger.error(client_context, "[%s] return status code [%d]", self.host, response.status_code)
            else:
                return self._parse_response(response.text)

        except Exception as excep:
            YLogger.exception(client_context, "Failed to resolve", excep)

        return ""
