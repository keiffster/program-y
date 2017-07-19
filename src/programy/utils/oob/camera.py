import logging

from programy.utils.oob.oob import OutOfBoundsProcessor
import xml.etree.ElementTree as ET

"""
Example: <oob><camera>on|off</camera></oob>
"""

class CameraOutOfBoundsProcessor(OutOfBoundsProcessor):

    def __init__(self):
        OutOfBoundsProcessor.__init__(self)
        self._command = None

    def parse_oob_xml(self, oob):
        if oob.text is not None:
            self._command = oob.text
            return True
        else:
            logging.error("Unvalid camera oob command - missing command")
            return False

    def execute_oob_command(self, bot, clientid):
        logging.info("CameraOutOfBoundsProcessor: Setting camera to=%s", self._command)
        return ""
