import logging
import xml.etree.ElementTree as ET

from programy.utils.oob.oob import OutOfBandProcessor

"""
<oob>
    <dial>07777777777</dial>
</oob>
"""
class DialOutOfBandProcessor(OutOfBandProcessor):

    def __init__(self):
        OutOfBandProcessor.__init__(self)
        self._number = None

    def parse_oob_xml(self, oob: ET.Element):
        if oob.text is not None:
            self._number = oob.text
            return True
        else:
            logging.error("Unvalid dial oob command - missing dial text!")
            return False

    def execute_oob_command(self, bot, clientid):
        logging.info("DialOutOfBandProcessor: Dialing=%s", self._number)
        return "DIAL"
