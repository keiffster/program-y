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

from programy.services.openchatbot.openchatbot import OpenChatBot


class HTTPRequests(object):

    def get(self, url):
        return requests.get(url)


class OpenChatBotDomainHandler(object):

    config_file_name = "openchatbot-configuration"
    wellknown_folder = ".well-known"
    search_domains = ["co", "co.uk", "uk", "fr", "es", "net", "info", "org"]
    default_domain = "com"

    def __init__(self, scan_alternatives=True, http_requests=None):
        self._scan_alternatives = scan_alternatives
        if http_requests is None:
            self._http_requests = HTTPRequests()
        else:
            self._http_requests = http_requests
        self._cached = {}

    @staticmethod
    def _get_protocol(https):
        if https is True:
            return "https"
        else:
            return "http"

    def _create_query_url(self, domain, https, ext=default_domain):

        return "%s://%s.%s/%s/%s"%(self._get_protocol(https), domain, ext,
                                   OpenChatBotDomainHandler.wellknown_folder,
                                   OpenChatBotDomainHandler.config_file_name)

    def get_endpoint(self, domain, https=False):

        if domain.upper() in self._cached:
            YLogger.info(None, "Returning cached domain chatbot [%s]", domain)
            return self._cached[domain.upper()]

        extensions = [OpenChatBotDomainHandler.default_domain]
        if self._scan_alternatives is True:
            extensions = extensions + OpenChatBotDomainHandler.search_domains

        for ext in extensions:
            try:
                url = self._create_query_url(domain, https, ext)

                YLogger.debug(None, "Trying [%s]", url)
                reply = self._http_requests.get(url)

                if reply.status_code == 200:
                    domaincb = OpenChatBot.create(domain, reply.json())
                    self._cached[domain.upper()] = domaincb
                    return domaincb

            except Exception as excep:
                YLogger.exception_nostack(None, "Failed to get endpoint for domain [%s]", excep, domain)

        return None

