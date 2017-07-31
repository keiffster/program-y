import logging
import xml.etree.ElementTree as ET

from programy.utils.oob.oob import OutOfBandProcessor

"""
<oob><url>http://<star/>.com</url></oob>
url
	<url>

"""

class URLOutOfBandProcessor(OutOfBandProcessor):

    def __init__(self):
        OutOfBandProcessor.__init__(self)
        self._url = None

    def parse_oob_xml(self, oob: ET.Element):
        if oob.text is not None:
            self._url = oob.text
            return True
        else:
            logging.error("Unvalid url oob command - missing url!")
            return False

            return self.execute_oob_command(bot, clientid)

    def execute_oob_command(self, bot, clientid):
        logging.info("URLOutOfBandProcessor: Loading=%s", self._url)
        return ""
