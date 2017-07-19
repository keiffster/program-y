
from abc import ABCMeta, abstractmethod
import xml.etree.ElementTree as ET

class OutOfBoundsProcessor(object):

    def __init__(self):
        return

    @abstractmethod
    def process_out_of_bounds(self, bot, clientid, oob):
        """
        Never Implemented
        """
        raise NotImplemented()

    def to_xml(self, oob):
        return ET.froomstring(oob)

