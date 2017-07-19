import logging

from programy.utils.oob.oob import OutOfBoundsProcessor

class DefaultOutOfBoundsProcessor(OutOfBoundsProcessor):

    def __init__(self):
        OutOfBoundsProcessor.__init__(self)

    def execute_oob_command(bot, clientid):
        logging.info("Default OOB Processing....")
        return ""
