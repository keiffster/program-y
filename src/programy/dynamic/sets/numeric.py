from programy.dynamic.sets.set import DynamicSet


class IsNumeric(DynamicSet):

    def __init__(self, config):
        DynamicSet.__init__(self, config)

    def is_member(self, bot, clientid, value):
        if value is not None:
            return value.isnumeric()
        else:
            return False