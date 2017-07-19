import logging
import xml.etree.ElementTree as ET

from programy.utils.oob.oob import OutOfBoundsProcessor

"""
Example: <oob><schedule><title><star/></title><description><lowercase><star index="2"/></lowercase></description><get name="sraix"/></schedule></oob>
"""
class ScheduleOutOfBoundsProcessor(OutOfBoundsProcessor):

    def __init__(self):
        OutOfBoundsProcessor.__init__(self)
        self._title = None
        self._description = None

    def parse_oob_xml(self, oob: ET.Element):
        for child in oob:
            if child.tag == 'title':
                self._title = child.text
            elif child.tag == 'description':
                self._description = child.text
            else:
                logging.error ("Unknown child element [%s] in schedule oob"%(child.tag))

            if self._title is not None and \
                self._description is not None:
                return True

            logging.error("Invalid email schedule command")
            return False

    def execute_oob_command(self, bot, clientid):
        logging.info("ScheduleOutOfBoundsProcessor: Scheduling=%s", self._title)
        return ""
