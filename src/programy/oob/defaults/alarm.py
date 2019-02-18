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

from programy.oob.defaults.oob import OutOfBandProcessor


class AlarmOutOfBandProcessor(OutOfBandProcessor):
    """
    <oob>
        <alarm><message><star/></message><get name="sraix"/></alarm>
    </oob>

    <oob>
        <alarm><hour>11</hour><minute>30</minute></alarm>
    </oob>
    """

    def __init__(self):
        OutOfBandProcessor.__init__(self)
        self._hour = None
        self._min = None
        self._message = None

    def parse_oob_xml(self, oob):
        if oob is not None:
            for child in oob:
                if child.tag == 'hour':
                    self._hour = child.text
                elif child.tag == 'minute':
                    self._min = child.text
                elif child.tag == 'message':
                    self._message = child.text
                else:
                    YLogger.error(self, "Unknown child element [%s] in alarm oob", child.tag)

            if self._hour is not None and self._min is not None:
                return True
            if self._message is not None:
                return True

        YLogger.error(self, "Invalid alarm oob command, either hour,min or message ")
        return False

    def execute_oob_command(self, client_context):
        if self._message is not None:
            YLogger.info(client_context, "AlarmOutOfBandProcessor: Showing alarm=%s", self._message)
        elif self._hour is not None and self._min is not None:
            YLogger.info(client_context, "AlarmOutOfBandProcessor: Setting alarm for %s:%s", self._hour, self._min)
        return "ALARM"
