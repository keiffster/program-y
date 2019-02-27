"""
Copyright (c) 2016-2019 Keith Sterling http://www.keithsterling.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions
of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import re

from programy.utils.logging.ylogger import YLogger


class Substitutions(object):

    PATTERN = re.compile("(\$[A-Z]+)")

    def __init__(self):
        self._substitutes = {}

    def empty(self):
        self._substitutes.clear()

    def add_substitute(self, name, value):
        if name in self._substitutes:
            YLogger.warning(self, "Substitute [%s], already exists", name)
        self._substitutes[name] = value

    def has_substitute(self, name):
        return bool(name in self._substitutes)

    def get_substitute(self, name):
        if name in self._substitutes:
            return self._substitutes[name]
        else:
            raise ValueError("No substitute named [%s]"%name)

    def load_substitutions(self, substitutions):
        if substitutions is not None:
            try:
                with open(substitutions, "r") as subsfile:
                    for line in subsfile:
                        namevalue = line.strip().split(":")

                        if len(namevalue) > 1:
                            self.add_substitute(namevalue[0], ":".join(namevalue[1:]))

            except Exception as e:
                YLogger.error(None, "Failed to load substitutions file")

    def replace(self, string: str) -> str:
        splits = Substitutions.PATTERN.split(string)
        replaced = []
        for segment in splits:
            if self.has_substitute(segment):
                replaced.append(self.get_substitute(segment))

            else:
                replaced.append(segment)

        return "".join(replaced)