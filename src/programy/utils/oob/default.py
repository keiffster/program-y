
from programy.utils.oob.oob import OutOfBoundsProcessor

class DefaultOutOfBoundsProcessor(OutOfBoundsProcessor):

    def __init__(self):
        OutOfBoundsProcessor.__init__(self)

    def process_out_of_bounds(self, bot, clientid, oob):
        return oob
