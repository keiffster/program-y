"""
Copyright (c) 2016-2019 Keith Sterling http://www.keithsterling.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from programy.utils.logging.ylogger import YLogger

from programy.dynamic.maps.map import DynamicMap


class SingularMap(DynamicMap):

    NAME = "SINGULAR"
    STATICS = {"MICE": "MOUSE"}

    def __init__(self, config):
        DynamicMap.__init__(self, config)

    @staticmethod
    def static_map(value):
        if value in SingularMap.STATICS:
            return SingularMap.STATICS[value]
        return None

    def map_value(self, client_context, input_value):
        singular_value = SingularMap.static_map(input_value)
        if singular_value is None:
            if input_value.endswith('IES'):
                singular_value = input_value[:-3] + "Y"
            elif input_value.endswith('S'):
                singular_value = input_value[:-1]
            else:
                singular_value = input_value

        YLogger.debug(client_context, "SingleMap converted %s to %s", input_value, singular_value)
        return singular_value
