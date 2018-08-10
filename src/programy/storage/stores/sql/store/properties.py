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

from programy.storage.stores.sql.store.sqlstore import SQLStore
from programy.storage.entities.property import PropertyStore
from programy.storage.stores.sql.dao.property import Property
from programy.storage.stores.sql.dao.property import DefaultVariable
from programy.storage.stores.sql.dao.property import Regex


class SQLBasePropertyStore(SQLStore, PropertyStore):

    def __init__(self, storage_engine):
        SQLStore.__init__(self, storage_engine)

    def empty(self):
        self.get_all().delete()

    def empty_properties(self):
        self.get_all().delete()

    def add_property(self, name, value):
        property = self._get_entity(name=name, value=value)
        self._storage_engine.session.add(property)
        return property

    def add_properties(self, properties):
        prop_list = []
        for name, value in properties.items():
            prop_list.append(self._get_entity(name=name, value=value))
        self._storage_engine.session.add_all(prop_list)

    def get_properties(self):
        db_properties = self._get_all()
        properties = {}
        for property in db_properties:
            properties[property.name] = property.value
        return properties

    def load(self, property_collection):
        self.load_all(property_collection)

    def load_all(self, property_collection):
        property_collection.empty()
        db_propertys = self._get_all()
        for db_property in db_propertys:
            property_collection.add_property(db_property.key,  db_property.value)


class SQLPropertyStore(SQLBasePropertyStore, PropertyStore):

    def __init__(self, storage_engine):
        SQLBasePropertyStore.__init__(self, storage_engine)

    def _get_all(self):
        return self._storage_engine.session.query(Property)

    def _get_entity(self, name, value):
        return Property(name=name, value=value)


class SQLDefaultVariableStore(SQLBasePropertyStore, PropertyStore):

    def __init__(self, storage_engine):
        SQLBasePropertyStore.__init__(self, storage_engine)

    def _get_all(self):
        return self._storage_engine.session.query(DefaultVariable)

    def add_default(self, name, value):
        return self.add_property(name, value)

    def add_defaults(self, defaults):
        self.add_properties(defaults)

    def get_default_values(self):
        return self.get_properties()


class SQLRegexStore(SQLBasePropertyStore, PropertyStore):

    def __init__(self, storage_engine):
        SQLBasePropertyStore.__init__(self, storage_engine)

    def _get_all(self):
        return self._storage_engine.session.query(Regex)
