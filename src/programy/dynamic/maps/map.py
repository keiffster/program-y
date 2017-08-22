from abc import ABCMeta, abstractmethod

class DynamicMap(object):
    __metaclass__ = ABCMeta

    def __init__(self, config):
        self._config = config

    @property
    def config(self):
        return self._config

    @abstractmethod
    def map_value(self, bot, clientid, value):
        raise NotImplemented()