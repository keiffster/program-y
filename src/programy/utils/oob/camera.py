import logging

from programy.utils.oob.oob import OutOfBandProcessor
import xml.etree.ElementTree as ET

"""
<oob>
    <camera>on|off</camera>
</oob>
"""

class CameraOutOfBandProcessor(OutOfBandProcessor):

    def __init__(self):
        OutOfBandProcessor.__init__(self)
        self._command = None

    def parse_oob_xml(self, oob):
        if oob.text is not None:
            self._command = oob.text
            return True
        else:
            logging.error("Invalid camera oob command - missing command")
            return False

    def execute_oob_command(self, bot, clientid):
        logging.info("CameraOutOfBandProcessor: Setting camera to=%s", self._command)
        return "CAMERA"
