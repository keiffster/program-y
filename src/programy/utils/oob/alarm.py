import logging

from programy.utils.oob.oob import OutOfBandProcessor
import xml.etree.ElementTree as ET

"""
<oob>
    <alarm><message><star/></message><get name="sraix"/></alarm>
</oob>
	
<oob>
    <alarm><hour>11</hour><minute>30</minute></alarm>
</oob>
"""

class AlarmOutOfBandProcessor(OutOfBandProcessor):

    def __init__(self):
        OutOfBandProcessor.__init__(self)
        self._hour = None
        self._min = None
        self._message = None

    def parse_oob_xml(self, oob: ET.Element):
        for child in oob:
            if child.tag == 'hour':
                self._hour = child.text
            elif child.tag == 'minute':
                self._min = child.text
            elif child.tag == 'message':
                self._message = child.text
            else:
                if logging.getLogger().isEnabledFor(logging.ERROR): logging.error ("Unknown child element [%s] in alarm oob"%(child.tag))

        if self._hour is not None and self._min is not None:
            return True
        if self._message is not None:
            return True

        if logging.getLogger().isEnabledFor(logging.ERROR): logging.error("Invalid alarm oob command, either hour,min or message ")
        return False

    def execute_oob_command(self, bot, clientid):
        if self._message is not None:
            if logging.getLogger().isEnabledFor(logging.INFO): logging.info("AlarmOutOfBandProcessor: Showing alarm=%s", self._message)
        elif self._hour is not None and self._min is not None:
            if logging.getLogger().isEnabledFor(logging.INFO): logging.info("AlarmOutOfBandProcessor: Setting alarm for %s:%s"%(self._hour, self._min))
        return "ALARM"
