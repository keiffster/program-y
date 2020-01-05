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
from programy.utils.logging.ylogger import YLogger
from programy.storage.entities.store import Store
from programy.storage.stores.nosql.mongo.store.mongostore import MongoStore
from programy.storage.entities.license import LicenseStore
from programy.storage.stores.nosql.mongo.dao.license import LicenseKey
from programy.utils.console.console import outputLog


class MongoLicenseKeysStore(MongoStore, LicenseStore):
    LICENSEKEYS = "licensekeys"

    def __init__(self, storage_engine):
        MongoStore.__init__(self, storage_engine)
        LicenseStore.__init__(self)

    def collection_name(self):
        return MongoLicenseKeysStore.LICENSEKEYS

    def add_licensekey(self, key_name, key):
        licensekey = LicenseKey(name=key_name, key=key)
        return self.add_document(licensekey)

    def load(self, collector, name=None):
        del name
        self.load_all(collector)

    def load_all(self, collector):
        YLogger.info(self, "Loading license keys from Mongo")
        collection = self.collection()

        collector.empty()

        licensekeys = collection.find()
        for licensekey in licensekeys:
            collector.add_key(licensekey['name'], licensekey['key'])

    def _read_lines_from_file(self, filename, verbose):
        success = 0
        count = 0
        with open(filename, "r", encoding="utf-8") as license_file:
            for line in license_file:
                if self._process_line(line, verbose) is True:
                    success += 1
                count += 1
        return count, success

    def _process_line(self, line, verbose=False):
        line = line.strip()
        result = False
        if line.startswith('#') is False:
            splits = line.split("=")
            if len(splits) > 1:
                key_name = splits[0].strip()
                # If key has = signs in it, then combine all elements past the first
                key = "".join(splits[1:]).strip()
                result = self.add_licensekey(key_name, key)
                if verbose is True:
                    outputLog(self, "%s = %s" % (key_name, key))        # pragma: no cover

            else:
                YLogger.warning(self, "Invalid license key [%s]", line)

        return result

    def upload_from_file(self, filename, fileformat=Store.TEXT_FORMAT, commit=True, verbose=False):
        YLogger.info(self, "Uploading license keys to Mongo [%s]", filename)
        try:
            YLogger.info(self, "Loading license key file: [%s]", filename)
            return self._read_lines_from_file(filename, verbose)

        except Exception as excep:
            YLogger.exception(self, "Invalid license key file [%s]", excep, filename)

        return 0, 0

