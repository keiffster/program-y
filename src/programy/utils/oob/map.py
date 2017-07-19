import logging
import xml.etree.ElementTree as ET

from programy.utils.oob.oob import OutOfBoundsProcessor

"""
Example: <oob><map>Kinghorn</map></oob>
"""
class MapOutOfBoundsProcessor(OutOfBoundsProcessor):

    def __init__(self):
        OutOfBoundsProcessor.__init__(self)
        self._location = None

    def parse_oob_xml(self, oob: ET.Element):
        if oob.text is not None:
            self._location = oob.text
            return True
        else:
            logging.error("Unvalid map oob command - missing location text!")
            return False

    def execute_oob_command(self, bot, clientid):
        logging.info("MapOutOfBoundsProcessor: Showing a map for location=%s", self._location)
        return ""
