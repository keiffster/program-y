from programy.dynamic.variables.variable import DynamicVariable

from programy.utils.text.dateformat import DateFormatter

class GetTime(DynamicVariable):

    def __init__(self, config):
        DynamicVariable.__init__(self, config)

    def get_value(self, bot, clientid, value=None):
        formatter = DateFormatter()
        return formatter.time_representation()


