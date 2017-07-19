import logging

from programy.utils.oob.oob import OutOfBoundsProcessor
import xml.etree.ElementTree as ET

"""
<oob><sms><recipient><get name="contacturi"/></recipient><message><get name="messagebody"/></message></sms></oob>
sms
	recipient
	message

"""

class SMSOutOfBoundsProcessor(OutOfBoundsProcessor):

    def __init__(self):
        OutOfBoundsProcessor.__init__(self)
        self._recipient = None
        self._description = None

    def parse_oob_xml(self, oob: ET.Element):
        for child in oob:
            if child.tag == 'recipient':
                self._recipient = child.text
            elif child.tag == 'message':
                self._message = child.text
            else:
                logging.error ("Unknown child element [%s] in sms oob"%(child.tag))

            if self._recipient is not None and \
                self._description is not None :
                return True

            logging.error("Invalid sms oob command")
            return False

    def execute_oob_command(self, bot, clientid):
        logging.info("SMSOutOfBoundsProcessor: Messaging=%s", self._recipient)
        return ""
