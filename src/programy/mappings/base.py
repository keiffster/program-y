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
import re


class BaseCollection(object):
    pass


class SingleStringCollection(BaseCollection):

    def __init__(self):
        BaseCollection.__init__(self)
        self._strings = []

    def empty(self):
        self._strings.clear()

    @property
    def strings(self):
        return self._strings

    def load_from_text(self, text):
        lines = text.split("\n")
        count = 0
        for line in lines:
            line = line.strip()
            if len(line) > 0:
                self._strings.append(line)
                count += 1
        return count


class DoubleStringCharSplitCollection(BaseCollection):

    def __init__(self):
        BaseCollection.__init__(self)
        self._pairs = []

    def empty(self):
        self._pairs.clear()

    def remove(self, name=None):
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
        return ','

    def load_from_text(self, text):
        lines = text.split("\n")
        count = 0
        for line in lines:
            line = line.strip()
            kvp = line.split(self.get_split_char())
            if len(kvp) > 1:
                key = kvp[0]
                value = self.get_split_char().join(kvp[1:])
                count += 1
                self.add_value(key, value)
        return count


class DoubleStringPatternSplitCollection(BaseCollection):
    RE_OF_SPLIT_PATTERN = re.compile('\"(.*?)\",\"(.*?)\"')

    def __init__(self):
        BaseCollection.__init__(self)
        self._pairs = {}

    @property
    def pairs(self):
        return self._pairs

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

    def add_to_lookup(self, index, pattern):
        if index in self._pairs:
            YLogger.error(self, "%s = %s already exists in collection", index, pattern)
        self._pairs[index] = pattern

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

                        to_replace = pair[1]
                        to_replace = self.match_case(replacable, to_replace)

                        if pair[1].endswith("."):
                            replacable = pattern.sub(to_replace, replacable)
                        else:
                            replacable = pattern.sub(to_replace+" ", replacable)
                        alreadys.append(pair[1])

            except Exception as excep:
                YLogger.exception(self, "Invalid regular expression [%s]", excep, str(pair[0]))

        return re.sub(' +', ' ', replacable.strip())

    def match_case(self, replacable, to_replace):
        count = 0
        length = len(replacable)

        for i in range(length):
            if replacable[i].isupper():
                count += 1

        if count == length:
            return to_replace.upper()

        if float(count) > float(length)/3.0:
            return to_replace.upper()

        return to_replace.lower()

    def load_from_text(self, text):
        lines = text.split("\n")
        count = 0
        for line in lines:
            line = line.strip()
            split = self.split_line_by_pattern(line, DoubleStringPatternSplitCollection.RE_OF_SPLIT_PATTERN)
            if split is not None:
                key, value = self.process_key_value(split[0], split[1])
                self.add_to_lookup(key, value)
                count += 1
        return count

    @staticmethod
    def split_line_by_pattern(line, pattern):
        line = line.strip()
        if line is not None and line:
            match = pattern.search(line)
            if match is not None:
                lhs = match.group(1)
                rhs = match.group(2)
                return [lhs, rhs]
            print("Pattern is bad [%s]", line)
        return None

    @staticmethod
    def normalise_pattern(pattern):
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

    @staticmethod
    def process_key_value(key, value, id=None):
        pattern_text = DoubleStringPatternSplitCollection.normalise_pattern(key)
        start = pattern_text.lstrip()
        middle = pattern_text
        end = pattern_text.rstrip()
        pattern = "(^%s|%s|%s$)" % (start, middle, end)
        replacement = value.upper()
        return key, [re.compile(pattern, re.IGNORECASE), replacement]
