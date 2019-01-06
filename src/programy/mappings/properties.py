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

from programy.mappings.base import DoubleStringCharSplitCollection
from programy.storage.factory import StorageFactory


class BasePropertiesCollection(DoubleStringCharSplitCollection):

    def __init__(self):
        DoubleStringCharSplitCollection.__init__(self)

    def get_split_char(self):
        return ":"

    def has_property(self, key):
        return self.has_key(key)

    def property(self, key):
        return self.value(key)

    def add_property(self, key, value):
        if self.has_property(key):
            self.add_value(key, value)
        else:
            self.pairs.append([key, value])

    def get_storage_name(self):
        raise NotImplementedError()

    def get_store(self, engine):
        raise NotImplementedError()

    def load(self, storage_factory):
        name = self.get_storage_name()
        if storage_factory.entity_storage_engine_available(name) is True:
            engine = storage_factory.entity_storage_engine(name)
            if engine:
                try:
                    store = self.get_store(engine)
                    store.load_all(self)
                except Exception as e:
                    YLogger.exception(self, "Failed to load %s from storage", e, name)

    def reload_file(self, storage_factory):
        self.load(storage_factory)


class PropertiesCollection(BasePropertiesCollection):

    def __init__(self):
        BasePropertiesCollection.__init__(self)

    def get_storage_name(self):
        return StorageFactory.PROPERTIES

    def get_store(self, engine):
        return engine.property_store()


class DefaultVariablesCollection(BasePropertiesCollection):

    def __init__(self):
        BasePropertiesCollection.__init__(self)

    def get_storage_name(self):
        return StorageFactory.DEFAULTS

    def get_store(self, engine):
        return engine.defaults_store()

    def has_variable(self, key):
        return self.has_property(key)

    def variable(self, key):
        return self.property(key)

    def add_variable(self, key, value):
        self.add_property(key, value)


class RegexTemplatesCollection(BasePropertiesCollection):

    def __init__(self):
        BasePropertiesCollection.__init__(self)

    def get_storage_name(self):
        return StorageFactory.REGEX_TEMPLATES

    def get_store(self, engine):
        return engine.regex_store()

    def has_regex(self, key):
        return self.has_property(key)

    def regex(self, key):
        return self.property(key)

    def add_regex(self, key, value):
        self.add_property(key, value)
