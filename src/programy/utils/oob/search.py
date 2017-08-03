import logging
import xml.etree.ElementTree as ET

from programy.utils.oob.oob import OutOfBandProcessor

"""
<oob>
    <search>VIDEO <star/></search>
</oob>
"""
class SearchOutOfBandProcessor(OutOfBandProcessor):

    def __init__(self):
        OutOfBandProcessor.__init__(self)
        self._search = None

    def parse_oob_xml(self, oob: ET.Element):
        if oob.text is not None:
            self._search = oob.text
            return True
        else:
            logging.error("Unvalid search oob command - missing search query!")
            return False

    def execute_oob_command(self, bot, clientid):
        logging.info("SearchOutOfBandProcessor: Searching=%s", self._search)
        return "SEARCH"
