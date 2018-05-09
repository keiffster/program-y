"""
Copyright (c) 2016-2018 Keith Sterling http://www.keithsterling.com

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
import re
from abc import ABCMeta, abstractmethod

class BaseCollection(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def split_line(self, line):
        """
        Never Implemented
        """

    @abstractmethod
    def process_splits(self, splits, id=None):
        """
        Never Implemented
        """

    def process_line(self, line, id=None):
        line = line.strip()
        if line is not None and line:
            if line.startswith("#") is False:
                splits = self.split_line(line)
                return self.process_splits(splits, id)
        return False

    def load_from_filename(self, filename, id=None):
        count = 0
        try:
            with open(filename, "r", encoding="utf-8") as data_file:
                for line in data_file:
                    if self.process_line(line, id):
                        count += 1
        except FileNotFoundError:
            YLogger.error(self, "File not found [%s]", filename)

        return count

    def load_from_text(self, text):
        count = 0
        lines = text.split("\n")
        for line in lines:
            if self.process_line(line):
                count += 1
        return count


class SingleStringCollection(BaseCollection):

    def __init__(self):
        BaseCollection.__init__(self)
        self._strings = []

    def empty(self):
        self._strings.clear()

    @property
    def strings(self):
        return self._strings

    def split_line(self, line):
        return [line.strip()]

    def process_splits(self, splits, id=None):
        self._strings.append(splits[0])
        return True


class DoubleStringCharSplitCollection(BaseCollection):

    def __init__(self):
        BaseCollection.__init__(self)
        self._pairs = []

    def empty(self):
        self._pairs.clear()

    @property
    def pairs(self):
        return self._pairs

    def add_value(self, key, value):
        key = key.strip()
        value = value.strip()
        self._pairs.append([key, value])

    def set_value(self, key, value):
        key = key.strip()
        value = value.strip()
        for pair in self._pairs:
            if pair[0] == key:
                pair[1] = value

    def has_key(self, key):
        for pair in self._pairs:
            if pair[0] == key:
                return True
        return False

    def value(self, key):
        for pair in self._pairs:
            if pair[0] == key:
                return pair[1]
        return None

    def get_split_char(self):
        return ","

    def split_line(self, line):
        splits = self.split_line_by_char(line)
        if len(splits) > 2:
            return [splits[0], self.get_split_char().join(splits[1:])]
        return splits

    def split_line_by_char(self, line):
        splits = line.split(self.get_split_char())
        return splits

    def process_splits(self, splits, id=None):
        self.add_value(splits[0], splits[1])
        return True


class DoubleStringPatternSplitCollection(BaseCollection):
    RE_OF_SPLIT_PATTERN = re.compile("\"(.*?)\",\"(.*?)\"")

    def __init__(self):
        BaseCollection.__init__(self)
        self._pairs = {}

    def empty(self):
        self._pairs.clear()

    def has_key(self, key):
        for pair in self._pairs.items():
            if pair[0] == key:
                return True
        return False

    def value(self, key):
        if self.has_key(key):
            return self._pairs[key]
        else:
            return None

    def get_split_pattern(self):
        return DoubleStringPatternSplitCollection.RE_OF_SPLIT_PATTERN

    def split_line(self, line):
        return self.split_line_by_pattern(line)

    def split_line_by_pattern(self, line):
        line = line.strip()
        if line is not None and line:
            pattern = self.get_split_pattern()
            match = pattern.search(line)
            if match is not None:
                lhs = match.group(1)
                rhs = match.group(2)
                return [lhs, rhs]
            YLogger.error(self, "Pattern is bad [%s]", line)
        return None

    def normalise_pattern(self, pattern):
        pattern = pattern.replace("(", r"\(")
        pattern = pattern.replace(")", r"\)")
        pattern = pattern.replace("[", r"\[")
        pattern = pattern.replace("]", r"\]")
        pattern = pattern.replace("{", r"\{")
        pattern = pattern.replace("}", r"\}")
        pattern = pattern.replace("|", r"\|")
        pattern = pattern.replace("^", r"\^")
        pattern = pattern.replace("$", r"\$")
        pattern = pattern.replace("+", r"\+")
        pattern = pattern.replace(".", r"\.")
        pattern = pattern.replace("*", r"\*")
        return pattern

    def process_splits(self, splits, id=None):
        if splits is not None and len(splits) > 0:
            pattern_text = self.normalise_pattern(splits[0])
            start = pattern_text.lstrip()
            middle = pattern_text
            end = pattern_text.rstrip()
            pattern = "(^%s|%s|%s$)" % (start, middle, end)
            replacement = splits[1]
            self._pairs[splits[0]] = [re.compile(pattern, re.IGNORECASE), replacement]
            return True
        return False

    def replace_by_pattern(self, replacable):
        alreadys = []
        for key, pair in self._pairs.items():
            try:
                pattern = pair[0]
                if pattern.findall(replacable):
                    found = False
                    for already in alreadys:
                        stripped = key.strip()
                        if stripped in already:
                            found = True
                    if found is not True:
                        if pair[1].endswith("."):
                            replacable = pattern.sub(pair[1], replacable)
                        else:
                            replacable = pattern.sub(pair[1]+" ", replacable)
                        alreadys.append(pair[1])

            except Exception as excep:
                YLogger.exception(self, "Invalid regular expression [%s]"%str(pair[0]), excep)

        return re.sub(' +', ' ', replacable.strip())


class TripleStringCollection(BaseCollection):

    def __init__(self):
        BaseCollection.__init__(self)
        self.triples = {}

    def empty(self):
        self._triples.clear()

    def split_line(self, line):
        splits = self.split_line_by_char(line)
        if len(splits) > 3:
            return [splits[0], splits[1], self.get_split_char().join(splits[2:])]
        return splits

    def get_split_char(self):
        return ":"

    def get_split_pattern(self):
        return ".*"

    def has_primary(self, key):
        if key in self.triples:
            return True
        return False

    def has_secondary(self, primary, key):
        if self.has_primary(primary):
            if key in self.triples[primary]:
                return True
        return False

    def value(self, primary, secondary):
        if self.has_primary(primary):
            if self.has_secondary(primary, secondary):
                return self.triples[primary][secondary]
        return None

    def split_line_by_char(self, line):
        splits = line.split(self.get_split_char())
        return splits

    def process_splits(self, splits, id=None):
        first = splits[0]
        second = splits[1]
        third = splits[2]

        if first not in self.triples:
            self.triples[first] = {}

        if second not in self.triples[first]:
            self.triples[first][second] = third

        return True
