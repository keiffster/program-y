
from abc import ABCMeta, abstractmethod

class OutOfBoundsProcessor(object):

    def __init__(self):
        return

    @abstractmethod
    def process_out_of_bounds(self, bot, clientid, oob):
        """
        Never Implemented
        """
        raise NotImplemented()
