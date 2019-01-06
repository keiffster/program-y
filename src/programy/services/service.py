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
from abc import ABCMeta, abstractmethod
from programy.utils.classes.loader import ClassLoader
from programy.config.brain.service import BrainServiceConfiguration


class Service(object):
    __metaclass__ = ABCMeta

    def __init__(self, config: BrainServiceConfiguration):
        self._config = config

    @property
    def configuration(self):
        return self._config

    def load_additional_config(self, service_config):
        pass

    @abstractmethod
    def ask_question(self, client_context, question: str):
        """
        Never knowingly Implemented
        """


class ServiceFactory(object):

    services = {}

    @classmethod
    def preload_services(cls, services_config):
        loader = ClassLoader()
        for service_name in services_config.services():
            name = service_name.upper()
            service_config = services_config.service(service_name)
            YLogger.debug(None, "Preloading service [%s] -> [%s]", name, service_config.classname)
            meta_class = loader.instantiate_class(service_config.classname)
            new_class = meta_class(service_config)
            ServiceFactory.services[name] = new_class

    @classmethod
    def service_exists(cls, name):
        return bool(name.upper() in ServiceFactory.services)\

    @classmethod
    def get_service(cls, service):
        name = service.upper()
        if name in ServiceFactory.services:
            return ServiceFactory.services[name]
        else:
            raise Exception("Unknown service [%s]" % name)
