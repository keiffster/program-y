import logging
import xml.etree.ElementTree as ET

from programy.utils.oob.oob import OutOfBoundsProcessor

"""
Example: <oob><wifi>on|off</wifi></oob>
"""

class WifiOutOfBoundsProcessor(OutOfBoundsProcessor):

    def __init__(self):
        OutOfBoundsProcessor.__init__(self)
        self._command = None

    def parse_oob_xml(self, oob: ET.Element):
        if oob.text is not None:
            self._command = oob.text
            return True
        else:
            logging.error("Unvalid camera oob command - missing command")
            return False

    def execute_oob_command(self, bot, clientid):
        logging.info("WifiOutOfBoundsProcessor: Setting camera to=%s", self._command)
        return ""
