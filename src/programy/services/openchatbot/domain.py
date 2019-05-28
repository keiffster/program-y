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
from programy.config.brain.openchatbots import BrainOpenChatBotsConfiguration


class HTTPRequests(object):

    def get(self, url):
        return requests.get(url)


class OpenChatBotDomainHandler(object):

    config_file_name = "openchatbot-configuration"
    wellknown_folder = ".well-known"
    default_domain = ["com"]

    def __init__(self, configuration: BrainOpenChatBotsConfiguration, http_requests=None):
        self._config = configuration

        if http_requests is None:
            self._http_requests = HTTPRequests()
        else:
            self._http_requests = http_requests
        self._cached = {}

    def _create_query_url(self, domain, protocol, ext):
        return "%s://%s.%s/%s/%s"%(protocol, domain, ext,
                                   OpenChatBotDomainHandler.wellknown_folder,
                                   OpenChatBotDomainHandler.config_file_name)

    def _try_connection(self, domain, protocol, ext):
        url = self._create_query_url(domain, protocol, ext)

        YLogger.debug(None, "Trying [%s]", url)
        reply = self._http_requests.get(url)

        if reply.status_code == 200:
            domaincb = OpenChatBot.create(domain, reply.json())
            self.cache_domain(domain, domaincb)
            return domaincb

        return None

    def get_extensions(self):
        return OpenChatBotDomainHandler.default_domain + self._config.domains

    def get_cached(self, domain):
        if domain.upper() in self._cached:
            YLogger.info(None, "Returning cached domain chatbot [%s]", domain)
            return self._cached[domain.upper()]
        return None

    def cache_domain(self, domain, domaincb):
        self._cached[domain.upper()] = domaincb

    def get_endpoint(self, domain):

        domaincb = self.get_cached(domain)
        if domaincb is not None:
            return domaincb

        extensions = self.get_extensions()

        # Either http, https, or both
        for protocol in self._config.protocols:
            # always com, then anything in config.domains, e.g co.uk, org, fr, de etc
            for ext in extensions:
                try:
                    domaincb = self._try_connection(domain, protocol, ext)
                    if domaincb is not None:
                        return domaincb

                except Exception as excep:
                    YLogger.exception_nostack(None, "Failed to get endpoint for domain [%s]", excep, domain)

        return None

