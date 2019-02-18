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

from programy.storage.entities.store import Store

class SetsStore(Store):

    def add_to_set(self, name, value):
        raise NotImplementedError("add_to_set missing from Sets Store")

    def remove_from_set(self, name, value):
        raise NotImplementedError("remove_from_set missing from Sets Store")

    def load_all(self, set_collection):
        raise NotImplementedError("load_all missing from Sets Store")

    def load(self, set_collection):
        raise NotImplementedError("load missing from Sets Store")

    def split_into_fields(self, text):
        return [text]

    def process_line(self, name, text):
        if text:
            return self.add_to_set(name, text[0])
        return False

    def add_set_values(self, the_set, value):
        splits = value.split()
        key = splits[0].upper()
        if key not in the_set:
            the_set[key] = []
        the_set[key].append(splits)

