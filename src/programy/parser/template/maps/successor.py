import logging

from programy.parser.template.maps.map import TemplateMap

class SuccessorMap(TemplateMap):

    NAME = "successor"

    def __init__(self):
        TemplateMap.__init__(self)

    def get_name(self):
        return SuccessorMap.NAME

    def map(self, value):
        int_value = int(value)
        str_value = str(int_value + 1)
        return str_value


