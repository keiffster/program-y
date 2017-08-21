import logging

from programy.utils.oob.oob import OutOfBandProcessor
import xml.etree.ElementTree as ET

"""
<oob>
    <sms>
        <recipient><get name="contacturi"/></recipient>
        <message><get name="messagebody"/></message>
    </sms>
</oob>
"""

class SMSOutOfBandProcessor(OutOfBandProcessor):

    def __init__(self):
        OutOfBandProcessor.__init__(self)
        self._recipient = None
        self._message = None

    def parse_oob_xml(self, oob: ET.Element):
        for child in oob:
            if child.tag == 'recipient':
                self._recipient = child.text
            elif child.tag == 'message':
                self._message = child.text
            else:
                if logging.getLogger().isEnabledFor(logging.ERROR): logging.error ("Unknown child element [%s] in sms oob"%(child.tag))

        if self._recipient is not None and \
            self._message is not None :
            return True

        if logging.getLogger().isEnabledFor(logging.ERROR): logging.error("Invalid sms oob command")
        return False

    def execute_oob_command(self, bot, clientid):
        if logging.getLogger().isEnabledFor(logging.INFO): logging.info("SMSOutOfBandProcessor: Messaging=%s", self._recipient)
        return "SMS"
