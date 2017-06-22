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
    def process_splits(self, splits):
        """
        Never Implemented
        """

    def load_from_filename(self, filename):
        count = 0
        with open(filename, "r+") as data_file:
            for line in data_file:
                line = line.strip()
                if line is not None and len(line) > 0:
                    splits = self.split_line(line)
                    if self.process_splits(splits) is True:
                        count += 1
        return count

    def load_from_text(self, text):
        count = 0
        lines = text.split("\n")
        for line in lines:
            line = line.strip()
            if line is not None and len(line) > 0:
                splits = self.split_line(line)
                if self.process_splits(splits) is True:
                    count += 1
        return count

class SingleStringCollection(BaseCollection):

    def __init__(self):
        BaseCollection.__init__(self)
        self._strings = []

    @property
    def strings(self):
        return self._strings

    def split_line(self, line):
        return [line.strip()]

    def process_splits(self, splits):
        self._strings.append(splits[0])
        return True


class DoubleStringCharSplitCollection(BaseCollection):

    def __init__(self):
        BaseCollection.__init__(self)
        self.pairs = []

    def set_value(self, key, value):
        for pair in self.pairs:
            if pair[0] == key:
                pair[1] = value

    def has_key(self, key):
        for pair in self.pairs:
            if pair[0] == key:
                return True
        return False

    def value(self, key):
        for pair in self.pairs:
            if pair[0] == key:
                return pair[1]
        return None

    def get_split_char(self):
        return ","

    def split_line(self, line):
        splits = self.split_line_by_char(line)
        if len(splits) > 2:
            return [splits[0], self.get_split_char().join(splits[1:])]
        else:
            return splits

    def split_line_by_char(self, line):
        splits = line.split(self.get_split_char())
        return splits

    def process_splits(self, splits):
        self.pairs.append([splits[0], splits[1]])
        return True

class DoubleStringPatternSplitCollection(BaseCollection):

    def __init__(self):
        BaseCollection.__init__(self)
        self.pairs = []

    def has_key(self, key):
        for pair in self.pairs:
            if pair[0] == key:
                return True
        return False

    def value(self, key):
        for pair in self.pairs:
            if pair[0] == key:
                return pair[1]
        return None

    def get_split_pattern(self):
        return r"\"(.*?)\",\"(.*?)\""

    def split_line(self, line):
        return self.split_line_by_pattern(line)

    def split_line_by_pattern(self, line):
        line = line.strip()
        if line is not None and len(line) > 0:
            pattern = re.compile(self.get_split_pattern())
            match = pattern.search(line)
            lhs = match.group(1)
            rhs = match.group(2)
            return [lhs, rhs]
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

    def process_splits(self, splits):
        pattern_text = self.normalise_pattern(splits[0])
        start = pattern_text.lstrip()
        middle = pattern_text
        end = pattern_text.rstrip()
        pattern = "(^%s|%s|%s$)" % (start, middle, end)
        replacement = splits[1]
        self.pairs.append([splits[0], pattern, replacement])
        return True

    def replace_by_pattern(self, replacable):
        alreadys = []
        for pair in self.pairs:
            try:
                pattern = re.compile(pair[1], re.IGNORECASE)
                if pattern.findall(replacable):
                    found = False
                    for already in alreadys:
                        stripped = pair[0].strip()
                        if stripped in already:
                            found = True
                    if found is not True:
                        replacable = pattern.sub(pair[2]+" ", replacable)
                        alreadys.append(pair[2])

            except Exception as excep:
                logging.error("Invalid regular expression [%s]", pair[1])
                logging.exception(excep)

        return re.sub(' +', ' ', replacable.strip())


class TripleStringCollection(BaseCollection):

    def __init__(self):
        BaseCollection.__init__(self)
        self.triples = {}

    @abstractmethod
    def split_line(self, line):
        """
        Never Implemented
        """

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

    def split_line_by_pattern(self, line):
        line = line.strip()
        if line is not None and len(line) > 0:
            pattern = re.compile(self.get_split_pattern())
            match = pattern.search(line)
            first = match.group(1)
            second = match.group(2)
            third = match.group(3)
            return [first, second, third]
        return None

    def process_splits(self, splits):
        first = splits[0]
        second = splits[1]
        third = splits[2]

        if first not in self.triples:
            self.triples[first] = {}

        if second not in self.triples[first]:
            self.triples[first][second] = third

        return True
