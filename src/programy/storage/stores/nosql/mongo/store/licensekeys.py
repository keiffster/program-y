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
from programy.storage.entities.store import Store
from programy.storage.stores.nosql.mongo.store.mongostore import MongoStore
from programy.storage.entities.license import LicenseStore
from programy.storage.stores.nosql.mongo.dao.license import LicenseKey


class MongoLicenseKeysStore(MongoStore, LicenseStore):

    LICENSEKEYS = "licensekeys"

    def __init__(self, storage_engine):
        MongoStore.__init__(self, storage_engine)

    def collection_name(self):
        return MongoLicenseKeysStore.LICENSEKEYS

    def load(self, license_collection):
        YLogger.info(self, "Loading license keys from Mongo")
        collection = self.collection()

        license_collection.empty()

        licensekeys = collection.find()
        for licensekey in licensekeys:
            license_collection.add_key(licensekey['name'], licensekey['key'])

    def upload_from_file(self, filename, format=Store.TEXT_FORMAT, commit=True, verbose=False):
        YLogger.info(self, "Uploading license keys to Mongo [%s]", filename)
        success = 0
        count = 0
        try:
            YLogger.info(self, "Loading license key file: [%s]", filename)
            with open(filename, "r", encoding="utf-8") as license_file:
                for line in license_file:
                    if self._process_license_key_line(line, verbose) is True:
                        success += 1
                    count += 1

            if commit is True:
                self.commit()

        except Exception as excep:
            YLogger.exception(self, "Invalid license key file [%s]", excep, filename)

        return count, success

    def _process_license_key_line(self, line, verbose=False):
        line = line.strip()
        if line:
            if line.startswith('#') is False:
                splits = line.split("=")
                if len(splits) > 1:
                    key_name = splits[0].strip()
                    # If key has = signs in it, then combine all elements past the first
                    key = "".join(splits[1:]).strip()
                    if verbose is True:
                        print(key_name, "=", key)

                    licensekey = LicenseKey(name=key_name, key=key)
                    self.add_document(licensekey)
                    return True
                else:
                    YLogger.warning(self, "Invalid license key [%s]", line)

        return False