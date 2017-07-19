import logging
import xml.etree.ElementTree as ET

from programy.utils.oob.oob import OutOfBoundsProcessor

"""
<oob>
    <email>
        <to>recipient</to>
        <subject>subject text</subject>
        <body>body text</body>
    </email>
</oob>
"""

class EmailOutOfBoundsProcessor(OutOfBoundsProcessor):

    def __init__(self):
        OutOfBoundsProcessor.__init__(self)
        self._to = None
        self._subject = None
        self._body = None

    def parse_oob_xml(self, oob: ET.Element):
        for child in oob:
            if child.tag == 'to':
                self._to = child.text
            elif child.tag == 'subject':
                self._subject = child.text
            elif child.tag == 'body':
                self._body = child.text
            else:
                logging.error ("Unknown child element [%s] in email oob"%(child.tag))

            if self._to is not None and \
                self._subject is not None and \
                self.body is not None:
                return True

            logging.error("Invalid email oob command")
            return False

    def execute_oob_command(self, bot, clientid):
        logging.info("EmailOutOfBoundsProcessor: Emailing=%s", self._to)
        return ""
