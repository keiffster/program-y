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
from programy.storage.entities.defaults import DefaultStore
from programy.storage.stores.sql.dao.defaults import Defaults


class SQLDefaultsStore(SQLStore, DefaultStore):

    def __init__(self, storage_engine):
        SQLStore.__init__(self, storage_engine)

    def empty(self):
        self._storage_engine.session.query(Defaults).delete()

    def empty_defaults(self):
        self._storage_engine.session.query(Defaults).delete()

    def add_default(self, name, value):
        defaults = Defaults(name=name, value=value)
        self._storage_engine.session.add(defaults)
        return defaults

    def add_defaults(self, defaults):
        def_list = []
        for name, value in defaults.items():
            def_list.append(Defaults(name=name, value=value))
        self._storage_engine.session.add_all(def_list)

    def get_default_values(self):
        db_defaults = self._storage_engine.session.query(Defaults)
        defaults = {}
        for default in db_defaults:
            defaults[default.name] = default.value
        return defaults
