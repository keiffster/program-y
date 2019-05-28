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


class OpenChatBot(object):

    def __init__(self, name, url, methods, authorization=None, api_key=None):
        self._name = name
        self._url = url
        self._methods = methods
        self._authorization = authorization
        self._api_key = api_key

    @property
    def name(self):
        return self._name

    @property
    def url(self):
        return self._url

    @property
    def methods(self):
        return self._methods

    @property
    def authorization(self):
        return self._authorization

    @property
    def api_key(self):
        return self._api_key

    @staticmethod
    def uri(host, port, endpoint):
        if endpoint.startswith('/') is False:
            endpoint = "/" + endpoint

        if port == 0:
            return "%s%s"%(host, endpoint)
        else:
            return "%s:%d%s"%(host, port, endpoint)

    @staticmethod
    def create(name, payload):

        if 'openchatbot' not in payload:
            return None
        openchatbot = payload['openchatbot']

        if 'host' not in openchatbot:
            return None
        host = openchatbot['host']

        if 'port' not in openchatbot:
            port = 0
        else:
            port = openchatbot['port']

        if 'endpoint' not in openchatbot:
            return None
        endpoint = openchatbot['endpoint']

        uri = OpenChatBot.uri(host, port, endpoint)

        if 'methods' not in openchatbot:
            return None
        methods = openchatbot['methods']

        return OpenChatBot(name, uri, methods)
