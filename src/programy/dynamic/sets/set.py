from abc import ABCMeta, abstractmethod

class DynamicSet(object):
    __metaclass__ = ABCMeta

    def __init__(self, config):
        self._config = config

    @property
    def config(self):
        return self._config

    @abstractmethod
    def is_member(self, bot, clientid, value):
        raise NotImplemented()