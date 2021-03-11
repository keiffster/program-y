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
import os
from datetime import datetime
try:
    import wikipedia

except ModuleNotFoundError as error:
    print("First use 'pip install wikipedia' before using this service")

from programy.utils.logging.ylogger import YLogger
from programy.services.base import ServiceQuery
from programy.services.library.base import PythonAPIService


class WikipediaSearchQuery(ServiceQuery):

    @staticmethod
    def create(service):
        return WikipediaSearchQuery(service)

    def parse_matched(self, matched):
        if len(matched) == 1:
            self._title = matched[0]

        else:
            raise ValueError("title missing")

    def __init__(self, service):
        ServiceQuery.__init__(self, service)
        self._title = None

    def execute(self):
        return self._service.search(self._title)

    def aiml_response(self, response):
        result = "SEARCH <ul>" + "".join("<li>"+x+"</li>" for x in response['response']['payload']['search']) + "</ul>"
        YLogger.debug(self, result)
        return result


class WikipediaSummaryQuery(ServiceQuery):

    @staticmethod
    def create(service):
        return WikipediaSummaryQuery(service)

    def parse_matched(self, matched):
        if len(matched) == 1:
            self._query = matched[0]

        else:
            raise ValueError("title missing")

    def __init__(self, service):
        ServiceQuery.__init__(self, service)
        self._query = None

    def execute(self):
        return self._service.summary(self._query)

    def aiml_response(self, response):
        result = "SUMMARY {0}".format(response['response']['payload']['summary'])
        YLogger.debug(self, result)
        return result


class WikipediaService(PythonAPIService):

    PATTERNS = [
        [r"SEARCH\s(\w+)", WikipediaSearchQuery],
        [r"SUMMARY\s(.+)", WikipediaSummaryQuery]
    ]

    def __init__(self, configuration):
        PythonAPIService.__init__(self, configuration)

    def get_default_aiml_file(self):
        return os.path.dirname(__file__) + os.sep + "wikipedia.aiml"

    @staticmethod
    def get_default_conf_file():
        return os.path.dirname(__file__) + os.sep + "wikipedia.conf"

    def _response_to_json(self, api, response):
        return response

    # Provide a summary of a single article
    def summary(self, title, sentences=0, chars=0, auto_suggest=True, redirect=True):
        started = datetime.now()
        speed = None
        try:
            data = wikipedia.summary(title, sentences, chars, auto_suggest, redirect)
            speed = started - datetime.now()

            if data is not None:
                result = {"summary": data}
                return self._create_success_payload("summary", started, speed, result)

            return self._create_failure_payload("summary", started, speed)

        except Exception as error:
            return self._create_exception_failure_payload("summary", started, speed, error)

    # Provide a list of articles matching the query
    # Use summary to return the neccassary action
    def search(self, query, results=10, suggestion=False):
        started = datetime.now()
        speed = None
        try:
            data = wikipedia.search(query, results, suggestion)
            speed = started - datetime.now()

            if data is not None:
                result = {"search": data}
                return self._create_success_payload("search", started, speed, result)

            return self._create_failure_payload("search", started, speed)

        except Exception as error:
            return self._create_exception_failure_payload("search", started, speed, error)

    def patterns(self) -> list:
        return WikipediaService.PATTERNS
