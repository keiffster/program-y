import logging

from programy.utils.oob.oob import OutOfBandProcessor
import xml.etree.ElementTree as ET

"""
<oob>
    <dialog><title>Which contact?</title><list><get name="contactlist"/></list></dialog>
</oob>
"""

class DialogOutOfBandProcessor(OutOfBandProcessor):

    def __init__(self):
        OutOfBandProcessor.__init__(self)
        self._title = None
        self._list = None

    def parse_oob_xml(self, oob: ET.Element):
        for child in oob:
            if child.tag == 'title':
                self._title = child.text
            elif child.tag == 'list':
                self._list = child.text
            else:
                if logging.getLogger().isEnabledFor(logging.ERROR): logging.error ("Unknown child element [%s] in dialog oob"%(child.tag))

        if self._title is not None and \
            self._list is not None:
            return True

        if logging.getLogger().isEnabledFor(logging.ERROR): logging.error("Invalid dialog oob command")
        return False

    def execute_oob_command(self, bot, clientid):
        if logging.getLogger().isEnabledFor(logging.INFO): logging.info("DialogOutOfBandProcessor: Dialog=%s", self._title)
        return "DIALOG"
