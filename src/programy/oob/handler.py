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
import re
import xml.etree.ElementTree as ET

from programy.utils.logging.ylogger import YLogger
from programy.utils.classes.loader import ClassLoader
from programy.config.brain.oobs import BrainOOBSConfiguration


class OOBHandler(object):

    def __init__(self, oob_configuration):

        assert (oob_configuration is not None)
        assert (isinstance(oob_configuration, BrainOOBSConfiguration))
        
        self._configuration = oob_configuration
        self._default_oob = None
        self._oob = {}

    @property
    def default_oob(self):
        return self._default_oob

    @property
    def oobs(self):
        return self._oob

    def load_oob_processors(self):
        if self._configuration is not None:
            if self._configuration.default() is not None:
                try:
                    YLogger.info(self, "Loading default oob")
                    classobject = ClassLoader.instantiate_class(self._configuration.default().classname)
                    self._default_oob = classobject()
                except Exception as excep:
                    YLogger.exception(self, "Failed to load OOB Processor", excep)

            for oob_name in  self._configuration.oobs():
                try:
                    YLogger.info(self, "Loading oob: %s", oob_name)
                    classobject = ClassLoader.instantiate_class(self._configuration.oob(oob_name).classname)
                    self._oob[oob_name] = classobject()
                except Exception as excep:
                    YLogger.exception(self, "Failed to load OOB", excep)

    def oob_in_response(self, response):
        return "<oob>" in response

    def handle(self, client_context, response):
        if "<oob>" in response:
            response, oob = self.strip_oob(response)
            if oob is not None:
                oob_response = self.process_oob(client_context, oob)
                response = response + " " + oob_response

        return response

    def strip_oob(self, response):
        match = re.compile(r"(.*)(<\s*oob\s*>.*<\/\s*oob\s*>)(.*)")
        groupings = match.match(response)
        if groupings is not None:
            front = groupings.group(1).strip()
            back = groupings.group(3).strip()
            response = ""
            if front != "":
                response = front + " "
            response += back
            oob = groupings.group(2)
            return response, oob
        return response, None

    def process_oob(self, client_context, oob_command):
        oob_content = ET.fromstring(oob_command)

        if oob_content.tag == 'oob':
            for child in oob_content.findall('./'):
                if child.tag in self._oob:
                    oob_class = self._oob[child.tag]
                    return oob_class.process_out_of_bounds(client_context, child)
                return self._default_oob.process_out_of_bounds(client_context, child)

        return ""


