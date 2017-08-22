import re

from programy.dynamic.sets.set import DynamicSet


class IsRomanNumeral(DynamicSet):

    def __init__(self, config):
        DynamicSet.__init__(self, config)

    def is_member(self, bot, clientid, value):
        if value is not None:
            match = re.match("^[IVXMC]*$", value)
            return match is not None
        return False