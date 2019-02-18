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

from programy.storage.entities.store import Store
from programy.mappings.base import DoubleStringPatternSplitCollection

class LookupsStore(Store):

    def load_all(self, lookup_collection, subdir=True, set_ext=".txt"):
        raise NotImplementedError("load_all missing from Lookups Store")

    def load(self, lookup_collection):
        raise NotImplementedError("load missing from Lookups Store")

    def process_key_value(self, key, value, id=None):
        return DoubleStringPatternSplitCollection.process_key_value(key, value, id)

    def split_into_fields(self, text):
        return DoubleStringPatternSplitCollection.split_line_by_pattern(text, DoubleStringPatternSplitCollection.RE_OF_SPLIT_PATTERN)

