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

# Force python XML parser not faster C accelerators
# because we can't hook the C implementation
import sys  # pylint: disable=wrong-import-position

sys.modules['_elementtree'] = None
import xml.etree.ElementTree as ET  # pylint: disable=wrong-import-position


class LineNumberingParser(ET.XMLParser):
    def _end(self, *args, **kwargs):  # pylint: disable=arguments-differ
        element = super(self.__class__, self)._end(*args, **kwargs)  # pylint: disable=attribute-error, bad-super-call
        element._end_line_number = self.parser.CurrentLineNumber  # pylint: disable=protected-access
        element._end_column_number = self.parser.CurrentColumnNumber  # pylint: disable=protected-access
        element._end_byte_index = self.parser.CurrentByteIndex  # pylint: disable=protected-access
        return element

    def _start(self, *args, **kwargs):  # pylint: disable=arguments-differ
        # Here we assume the default XML parser which is expat
        # and copy its element position attributes into output Elements
        element = super(self.__class__, self)._start(*args, **kwargs)  # pylint: disable=attribute-error, bad-super-call
        element._start_line_number = self.parser.CurrentLineNumber  # pylint: disable=protected-access
        element._start_column_number = self.parser.CurrentColumnNumber  # pylint: disable=protected-access
        element._start_byte_index = self.parser.CurrentByteIndex  # pylint: disable=protected-access
        return element
