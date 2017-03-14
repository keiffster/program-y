"""
Copyright (c) 2016 Keith Sterling

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

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
