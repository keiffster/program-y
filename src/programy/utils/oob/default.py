import logging
import xml.etree.ElementTree as ET

from programy.utils.oob.oob import OutOfBandProcessor

class DefaultOutOfBandProcessor(OutOfBandProcessor):

    def __init__(self):
        OutOfBandProcessor.__init__(self)

    def execute_oob_command(self, bot, clientid):
        logging.info("Default OOB Processing....")
        if self._xml is not None:
            return ET.tostring(self._xml, encoding='utf8', method='xml').decode('utf-8')
        else:
            return "DEFAULT"
