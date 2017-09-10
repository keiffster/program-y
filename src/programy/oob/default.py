import logging

from programy.oob.oob import OutOfBandProcessor

# Default OOB Processor consumes XML and returns nothing

class DefaultOutOfBandProcessor(OutOfBandProcessor):

    def __init__(self):
        OutOfBandProcessor.__init__(self)

    def execute_oob_command(self, bot, clientid):
        if logging.getLogger().isEnabledFor(logging.INFO): logging.info("Default OOB Processing....")
        if self._xml is not None:
            return ""
        else:
            return ""
