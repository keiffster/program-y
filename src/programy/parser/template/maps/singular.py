import logging

from programy.parser.template.maps.map import TemplateMap

class SingularMap(TemplateMap):

    NAME = "singular"
    STATICS = {"MICE": "MOUSE"
              }

    def __init__(self):
        TemplateMap.__init__(self)

    def get_name(self):
        return SingularMap.NAME

    def static_map(self, value):
        if value in SingularMap.STATICS:
            return SingularMap.STATICS[value]
        return None

    def map(self, value):
        plural_value = self.static_map(value)
        if plural_value is not None:
            return plural_value

        if value.endswith('IES'):
            return value[:-3] + "Y"
        elif value.endswith('S'):
            return value[:-1]
        else:
            return value
