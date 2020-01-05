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
import argparse
from programy.storage.entities.store import Store
from programy.storage.stores.sql.engine import SQLStorageEngine
from programy.storage.stores.sql.config import SQLStorageConfiguration
from programy.storage.stores.sql.store.categories import SQLCategoryStore
from programy.storage.stores.sql.store.maps import SQLMapsStore
from programy.storage.stores.sql.store.sets import SQLSetsStore
from programy.storage.stores.sql.store.rdfs import SQLRDFsStore
from programy.storage.stores.sql.store.properties import SQLPropertyStore
from programy.storage.stores.sql.store.properties import SQLDefaultVariableStore
from programy.storage.stores.sql.store.properties import SQLRegexStore
from programy.storage.stores.sql.store.lookups import SQLDenormalStore
from programy.storage.stores.sql.store.lookups import SQLNormalStore
from programy.storage.stores.sql.store.lookups import SQLGenderStore
from programy.storage.stores.sql.store.lookups import SQLPersonStore
from programy.storage.stores.sql.store.lookups import SQLPerson2Store
from programy.storage.stores.sql.store.spelling import SQLSpellingStore
from programy.storage.stores.sql.store.licensekeys import SQLLicenseKeysStore
from programy.storage.stores.sql.store.usergroups import SQLUserGroupStore
from programy.storage.stores.sql.store.nodes import SQLTemplateNodesStore
from programy.storage.stores.sql.store.nodes import SQLPatternNodesStore
from programy.storage.stores.sql.store.processors import SQLPreProcessorsStore
from programy.storage.stores.sql.store.processors import SQLPostProcessorsStore
from programy.storage.stores.sql.store.processors import SQLPostQuestionProcessorsStore
from programy.utils.console.console import outputLog


class Uploader:

    @staticmethod
    def upload(storetype, url, filename, dirname, subdir, extension, create=False, drop_all=False, verbose=False):
        outputLog(None, "")
        config = SQLStorageConfiguration()
        config.url = url
        config.create_db = create
        config.drop_all_first = drop_all
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = Uploader._get_store(storetype, engine)

        outputLog(None, "Emptying [%s]" % storetype)
        store.empty()

        outputLog(None, "Loading [%s]" % storetype)

        if filename is not None:
            count, success = store.upload_from_file(filename, commit=True, verbose=verbose)
            outputLog(None, "Lines processed [%d]" % count)
            outputLog(None, "Entities successful [%s]" % success)

        elif dirname is not None:
            count, success = store.upload_from_directory(dirname, fileformat=Store.TEXT_FORMAT, extension=extension,
                                                         subdir=subdir, commit=True, verbose=verbose)
            outputLog(None, "Lines processed [%d]" % count)
            outputLog(None, "Entities successful [%s]" % success)

        else:
            raise Exception("You must specify either --file or --dir")

        return count, success

    @staticmethod
    def _get_store(storetype, engine):
        if storetype == 'categories':
            return SQLCategoryStore(engine)
        if storetype == 'maps':
            return SQLMapsStore(engine)
        if storetype == 'sets':
            return SQLSetsStore(engine)
        if storetype == 'rdfs':
            return SQLRDFsStore(engine)
        if storetype == 'preprocessors':
            return SQLPreProcessorsStore(engine)
        if storetype == 'postprocessors':
            return SQLPostProcessorsStore(engine)
        if storetype == 'postquestionprocessors':
            return SQLPostQuestionProcessorsStore(engine)
        if storetype == 'templatenodes':
            return SQLTemplateNodesStore(engine)
        if storetype == 'patternnodes':
            return SQLPatternNodesStore(engine)
        if storetype == 'properties':
            return SQLPropertyStore(engine)
        if storetype == 'defaults':
            return SQLDefaultVariableStore(engine)
        if storetype == 'regexes':
            return SQLRegexStore(engine)
        if storetype == 'denormals':
            return SQLDenormalStore(engine)
        if storetype == 'normals':
            return SQLNormalStore(engine)
        if storetype == 'genders':
            return SQLGenderStore(engine)
        if storetype == 'persons':
            return SQLPersonStore(engine)
        if storetype == 'person2s':
            return SQLPerson2Store(engine)
        if storetype == 'spelling':
            return SQLSpellingStore(engine)
        if storetype == 'licenses':
            return SQLLicenseKeysStore(engine)
        if storetype == 'usergroups':
            return SQLUserGroupStore(engine)

        raise Exception("Unknown entity storetype [%s]" % storetype)

    @staticmethod
    def create_arguments():
        loader_args = argparse.ArgumentParser(description='Program-Y Set SQL Loader')

        loader_args.add_argument('-e', '--entity', help="Name of entity to load")
        loader_args.add_argument('-u', '--url', help="SQL Alchemy connection url")
        loader_args.add_argument('-f', '--file', help="File to load")
        loader_args.add_argument('-d', '--dir', help="Directory to load files from")
        loader_args.add_argument('-x', '--extension', help="Extension of file to load (dir only)")
        loader_args.add_argument('-s', '--subdir', action='store_true', help="Recurse into all subdirectories")
        loader_args.add_argument('-c', '--create', action='store_true', help="Create database")
        loader_args.add_argument('-a', '--drop', action='store_true', help="Drop all table first")
        loader_args.add_argument('-v', '--verbose', action='store_true', help="Verbose output of loading process")

        return loader_args

    @staticmethod
    def get_args(arguments):
        return arguments.parse_args()       #pragma: no cover

    @staticmethod
    def run():
        arguments = Uploader.create_arguments()
        try:
            args = Uploader.get_args(arguments)
            Uploader.upload(args.entity,
                            args.url,
                            args.file,
                            args.dir,
                            args.subdir,
                            args.extension,
                            create=args.create,
                            drop_all=args.drop,
                            verbose=args.verbose)

        except Exception as excep:
            outputLog(None, "SQL Loader error occured - %s" % excep)
            arguments.print_help()
        except SystemExit as excep:
            outputLog(None, "SQL Loader error occured - %s" % excep)
            arguments.print_help()

if __name__ == '__main__':

    Uploader.run()                          #pragma: no cover
