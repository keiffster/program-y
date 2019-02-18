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
import xml.etree.ElementTree as ET

from programy.oob.defaults.oob import OutOfBandProcessor


class SMSOutOfBandProcessor(OutOfBandProcessor):
    """
    <oob>
        <sms>
            <recipient><get name="contacturi"/></recipient>
            <message><get name="messagebody"/></message>
        </sms>
    </oob>
    """
    def __init__(self):
        OutOfBandProcessor.__init__(self)
        self._recipient = None
        self._message = None

    def parse_oob_xml(self, oob: ET.Element):
        if oob is not None:
            for child in oob:
                if child.tag == 'recipient':
                    self._recipient = child.text
                elif child.tag == 'message':
                    self._message = child.text
                else:
                    YLogger.error(self, "Unknown child element [%s] in sms oob", child.tag)

            if self._recipient is not None and self._message is not None:
                return True

        YLogger.error(self, "Invalid sms oob command")
        return False

    def execute_oob_command(self, client_context):
        YLogger.info(client_context, "SMSOutOfBandProcessor: Messaging=%s", self._recipient)
        return "SMS"
