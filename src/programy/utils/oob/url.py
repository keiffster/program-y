import logging
import xml.etree.ElementTree as ET

from programy.utils.oob.oob import OutOfBoundsProcessor

"""
<oob><url>http://<star/>.com</url></oob>
url
	<url>

"""

class URLOutOfBoundsProcessor(OutOfBoundsProcessor):

    def __init__(self):
        OutOfBoundsProcessor.__init__(self)
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
        logging.info("URLOutOfBoundsProcessor: Loading=%s", self._url)
        return ""
