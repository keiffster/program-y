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
from programy.utils.classes.loader import ClassLoader
from programy.storage.stores.sql.store.sqlstore import SQLStore
from programy.storage.entities.oobs import OOBsStore
from programy.storage.stores.sql.dao.oob import OOB
from programy.storage.entities.store import Store
from programy.utils.console.console import outputLog


class SQLOOBsStore(SQLStore, OOBsStore):

    def __init__(self, storage_engine):
        SQLStore.__init__(self, storage_engine)
        OOBsStore.__init__(self)

    def _get_all(self):
        return self._storage_engine.session.query(OOB)

    def empty(self):
        self._get_all().delete()

    def get_all_oobs(self):
        return self._storage_engine.session.query(OOB)

    def _get_entity(self, name, classname):
        return OOB(name=name, oob_class=classname)

    def load(self, handler, name=None):
        oobs = self.get_all_oobs()
        for oob in oobs:
            try:
                handler.add_oob(oob.name, ClassLoader.instantiate_class(oob.oob_class)())
            except Exception as e:
                YLogger.exception(self, "Failed pre-instantiating OOB [%s]", e, oob.oob_class)

    def _load_oobs_from_file(self, filename, verbose):
        count = 0
        success = 0
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                if self._process_config_line(line, verbose) is True:
                    success += 1
                count += 1

        return count, success

    def upload_from_file(self, filename, fileformat=Store.TEXT_FORMAT, commit=True, verbose=False):
        try:
            count, success = self._load_oobs_from_file(filename, verbose)

            self.commit(commit)

            return count, success

        except Exception as error:
            YLogger.exception(self, "Failed to load oobs from [%s]", error, filename)

        return 0, 0

    def _process_config_line(self, line, verbose=False):
        line = line.strip()
        if line.startswith('#') is False:
            splits = line.split("=")
            if len(splits) > 1:
                oob_name = splits[0].strip()
                class_name = splits[1].strip()
                oob = self._get_entity(oob_name, class_name)
                self.storage_engine.session.add(oob)
                if verbose is True:
                    outputLog(self, "[%s] = [%s]" % (oob_name, class_name))

                return True

        return False

