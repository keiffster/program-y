import logging

from programy.utils.oob.oob import OutOfBandProcessor

class DefaultOutOfBandProcessor(OutOfBandProcessor):

    def __init__(self):
        OutOfBandProcessor.__init__(self)

    def execute_oob_command(bot, clientid):
        logging.info("Default OOB Processing....")
        return ""
