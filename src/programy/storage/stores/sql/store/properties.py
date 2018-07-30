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


class SQLPropertyStore(SQLStore, PropertyStore):

    def __init__(self, storage_engine):
        SQLStore.__init__(self, storage_engine)

    def empty(self):
        self._storage_engine.session.query(Property).delete()

    def empty_properties(self):
        self._storage_engine.session.query(Property).delete()

    def add_property(self, name, value):
        property = Property(name=name, value=value)
        self._storage_engine.session.add(property)
        return property

    def add_properties(self, properties):
        prop_list = []
        for name, value in properties.items():
            prop_list.append(Property(name=name, value=value))
        self._storage_engine.session.add_all(prop_list)

    def get_properties(self):
        db_properties = self._storage_engine.session.query(Property)
        properties = {}
        for property in db_properties:
            properties[property.name] = property.value
        return properties
