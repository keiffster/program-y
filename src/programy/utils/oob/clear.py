import logging
import xml.etree.ElementTree as ET

from programy.utils.oob.oob import OutOfBandProcessor

"""
<oob>
    <clear>log</clear>
</oob>
"""

class ClearOutOfBandProcessor(OutOfBandProcessor):

    def __init__(self):
        OutOfBandProcessor.__init__(self)
        self._command = None

    def parse_oob_xml(self, oob):
        if oob.text is not None:
            self._command = oob.text
            return True
        else:
            logging.error("Unvalid clear oob command - missing command")
            return False

    def execute_oob_command(self, bot, clientid):
        logging.info("ClearOutOfBandProcessor: Clearing=%s", self._command)
        return "CLEAR"
