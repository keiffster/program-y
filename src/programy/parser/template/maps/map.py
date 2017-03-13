
from abc import ABCMeta, abstractmethod

class TemplateMap(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_name(self):
        """
        Never Implemented
        """

    @abstractmethod
    def map(self, value):
        """
        Never Implemented
        """

