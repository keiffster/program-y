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

from programy.storage.stores.sql.store.processors import SQLPostProcessorsStore
from programy.storage.stores.sql.store.processors import SQLPreProcessorsStore


class Uploader(object):

    @staticmethod
    def upload(type, url, filename, dirname, subdir, extension, create=False, drop_all=False, verbose=False):
        print ()
        config = SQLStorageConfiguration()
        config._url = url
        config._create_db = create
        config._drop_all_first = drop_all
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = Uploader._get_store(type, engine)

        print("Emptying [%s]"%type)
        store.empty()

        print("Loading [%s]"%type)
        if filename is not None:
            count, success = store.upload_from_file(filename, commit=True, verbose=verbose)
            print("Lines processed ", count)
            print("Entities successful", success)
        elif dirname is not None:
            count, success = store.upload_from_directory(dirname, format=Store.TEXT_FORMAT, extension=extension, subdir=subdir, commit=True, verbose=verbose)
            print("Lines processed ", count)
            print("Entities successful", success)
        else:
            raise Exception("You must specify either --file or --dir")

    @staticmethod
    def _get_store(type, engine):
        if type == 'categories':
            return SQLCategoryStore(engine)
        if type == 'maps':
            return SQLMapsStore(engine)
        if type == 'sets':
            return SQLSetsStore(engine)
        if type == 'rdfs':
            return SQLRDFsStore(engine)
        if type == 'postprocessors':
            return SQLPostProcessorsStore(engine)
        if type == 'preprocessors':
            return SQLPreProcessorsStore(engine)
        if type == 'templatenodes':
            return SQLTemplateNodesStore(engine)
        if type == 'patternnodes':
            return SQLPatternNodesStore(engine)
        if type == 'properties':
            return  SQLPropertyStore(engine)
        if type == 'defaults':
            return SQLDefaultVariableStore(engine)
        if type == 'regexes':
            return SQLRegexStore(engine)
        if type == 'denormals':
            return SQLDenormalStore(engine)
        if type == 'normals':
            return SQLNormalStore(engine)
        if type == 'genders':
            return SQLGenderStore(engine)
        if type == 'persons':
            return SQLPersonStore(engine)
        if type == 'person2s':
            return SQLPerson2Store(engine)
        if type == 'spelling':
            return SQLSpellingStore(engine)
        if type == 'licenses':
            return SQLLicenseKeysStore(engine)
        if type == 'usergroups':
            return SQLUserGroupStore(engine)

        raise Exception("Unknone entity type [%s]"%type)

    @staticmethod
    def create_arguments():
        arguments = argparse.ArgumentParser(description='Program-Y Set SQL Loader')

        arguments.add_argument('-e', '--entity', help="Name of entity to load")
        arguments.add_argument('-u', '--url', help="SQL Alchemy connection url")
        arguments.add_argument('-f', '--file', help="File to load")
        arguments.add_argument('-d', '--dir', help="Directory to load files from")
        arguments.add_argument('-x', '--extension', help="Extension of file to load (dir only)")
        arguments.add_argument('-s', '--subdir', action='store_true', help="Recurse into all subdirectories")
        arguments.add_argument('-c', '--create', action='store_true', help="Create database")
        arguments.add_argument('-a', '--drop', action='store_true', help="Drop all table first")
        arguments.add_argument('-v', '--verbose', action='store_true', help="Verbose output of loading process")

        return arguments


if __name__ == '__main__':

    arguments = Uploader.create_arguments()
    try:
        args = arguments.parse_args()
        Uploader.upload(args.entity, args.url, args.file, args.dir, args.subdir, args.extension, create=args.create, drop_all=args.drop, verbose=args.verbose)

    except Exception as e:
        print("An error occured - %s"%e)
        arguments.print_help()