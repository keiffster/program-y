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
from programy.storage.entities.license import LicenseStore
from programy.storage.stores.sql.dao.license import LicenseKey


class SQLLicenseKeysStore(SQLStore, LicenseStore):

    def __init__(self, storage_engine):
        SQLStore.__init__(self, storage_engine)

    def _get_all(self):
        return self._storage_engine.session.query(LicenseKey)

    def _get_entity(self, name, key):
        return LicenseKey(name=name, key=key)

    def empty(self):
        self.get_all().delete()

    def empty_licensekeys(self):
        self.get_all().delete()

    def add_licensekey(self, name, key):
        licensekey = self._get_entity(name=name, key=key)
        self._storage_engine.session.add(licensekey)
        return licensekey

    def add_licensekeys(self, licensekeys):
        prop_list = []
        for name, key in licensekeys.items():
            prop_list.append(self._get_entity(name=name, key=key))
        self._storage_engine.session.add_all(prop_list)

    def get_licensekeys(self):
        db_licensekeys = self._get_all()
        licensekeys = {}
        for licensekey in db_licensekeys:
            licensekeys[licensekey.name] = licensekey.key
        return licensekeys

    def load(self, licensekey_collection):
        self.load_all(licensekey_collection)

    def load_all(self, licensekey_collection):
        licensekey_collection.empty()
        db_licensekeys = self._get_all()
        for db_licensekey in db_licensekeys:
            licensekey_collection.add_licensekey(db_licensekey.key,  db_licensekey.key)



