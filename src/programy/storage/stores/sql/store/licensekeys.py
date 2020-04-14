"""
Copyright (c) 2016-2020 Keith Sterling http://www.keithsterling.com

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
import os
from programy.utils.logging.ylogger import YLogger
from programy.storage.stores.sql.store.sqlstore import SQLStore
from programy.storage.entities.license import LicenseStore
from programy.storage.stores.sql.dao.license import LicenseKey
from programy.storage.entities.store import Store
from programy.utils.console.console import outputLog


class SQLLicenseKeysStore(SQLStore, LicenseStore):

    def __init__(self, storage_engine):
        SQLStore.__init__(self, storage_engine)
        LicenseStore.__init__(self)

    def _get_all(self):
        return self._storage_engine.session.query(LicenseKey)

    def _get_entity(self, name, key):
        return LicenseKey(name=name, key=key)

    def empty(self):
        self._get_all().delete()

    def add_licensekey(self, name, key):
        licensekey = self._get_entity(name=name, key=key)
        self._storage_engine.session.add(licensekey)
        return True

    def load(self, collector, name=None):
        del name
        self.load_all(collector)

    def load_all(self, collector):
        collector.empty()
        db_licensekeys = self._get_all()
        for db_licensekey in db_licensekeys:
            collector.add_key(db_licensekey.name, db_licensekey.key)

    def _read_lines_from_file(self, filename, verbose):
        count = 0
        success = 0
        with open(filename, "r") as key_file:
            for line in key_file:
                if self._process_license_key_line(line, verbose) is True:
                    success += 1
                count += 1

        return count, success

    def upload_from_file(self, filename, fileformat=Store.TEXT_FORMAT, commit=True, verbose=False):
        try:
            count, success = self._read_lines_from_file(filename, verbose)
            self.commit(commit)
            return count, success

        except Exception as e:
            YLogger.exception(None, "Failed to upload license keys from file [%s]", e, filename)

        return 0, 0

    def _process_license_key_line(self, line, verbose=False):
        line = line.strip()
        result = False
        if line and line.startswith('#') is False:
            splits = line.split("=")
            if len(splits) > 1:
                key_name = splits[0].strip()
                # If key has = signs in it, then combine all elements past the first
                key = "".join(splits[1:]).strip()
                result = self.add_licensekey(key_name, key)
                if verbose is True:
                    outputLog(self, "[%s] = [%s]" % (key_name, key))        # pragma: no cover

            else:
                YLogger.warning(self, "Invalid license key [%s]", line)

        return result
