import logging

from programy.parser.template.maps.map import TemplateMap


class PluralMap(TemplateMap):

    NAME = "plural"
    STATICS = {"MOUSE": "MICE"
              }

    def __init__(self):
        TemplateMap.__init__(self)

    def get_name(self):
        return PluralMap.NAME

    def static_map(self, value):
        if value in PluralMap.STATICS:
            return PluralMap.STATICS[value]
        return None

    def map(self, value):
        plural_value = self.static_map(value)
        if plural_value is not None:
            return plural_value

        if value.endswith('Y'):
            return value[:-1] + 'IES'

        return value + 'S'

