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

from programy.storage.stores.nosql.mongo.engine import MongoStorageEngine
from programy.storage.stores.nosql.mongo.config import MongoStorageConfiguration

from programy.storage.stores.nosql.mongo.store.categories import MongoCategoryStore

from programy.storage.stores.nosql.mongo.store.maps import MongoMapsStore
from programy.storage.stores.nosql.mongo.store.sets import MongoSetsStore
from programy.storage.stores.nosql.mongo.store.rdfs import MongoRDFsStore

from programy.storage.stores.nosql.mongo.store.properties import MongoPropertyStore
from programy.storage.stores.nosql.mongo.store.properties import MongoDefaultVariablesStore
from programy.storage.stores.nosql.mongo.store.properties import MongoRegexesStore
from programy.storage.stores.nosql.mongo.store.lookups import MongoDenormalStore
from programy.storage.stores.nosql.mongo.store.lookups import MongoNormalStore
from programy.storage.stores.nosql.mongo.store.lookups import MongoGenderStore
from programy.storage.stores.nosql.mongo.store.lookups import MongoPersonStore
from programy.storage.stores.nosql.mongo.store.lookups import MongoPerson2Store
from programy.storage.stores.nosql.mongo.store.spelling import MongoSpellingStore
from programy.storage.stores.nosql.mongo.store.licensekeys import MongoLicenseKeysStore
from programy.storage.stores.nosql.mongo.store.usergroups import MongoUserGroupsStore

from programy.storage.stores.nosql.mongo.store.nodes import MongoTemplateNodeStore
from programy.storage.stores.nosql.mongo.store.nodes import MongoPatternNodeStore

from programy.storage.stores.nosql.mongo.store.processors import MongoPostProcessorStore
from programy.storage.stores.nosql.mongo.store.processors import MongoPreProcessorStore


class Uploader(object):

    @staticmethod
    def upload(type, url, database, filename, dirname, subdir, extension, drop_all=False, verbose=False):
        config = MongoStorageConfiguration()
        config._url = url
        config._database = database
        config._drop_all_first = drop_all
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = Uploader._get_store(type, engine)

        if drop_all is True:
            print("Dropped database")
            exit(0)

        print("Emptying [%s]"%type)
        store.empty()

        print("Loading [%s]"%type)
        if filename is not None:
            count, success = store.upload_from_file(filename,  format=Store.TEXT_FORMAT, commit=True, verbose=verbose)
            print("Lines processed ", count)
            print("Entities successful", success)
        elif dirname is not None:
            count, success = store.upload_from_directory(directory=dirname, subdir=subdir, extension=extension, commit=True, verbose=verbose)
            print("Lines processed ", count)
            print("Entities successful", success)
        else:
            raise Exception("You must specify either --file or --dir")

    @staticmethod
    def _get_store(type, engine):
        if type == 'categories':
            return MongoCategoryStore(engine)
        if type == 'maps':
            return MongoMapsStore(engine)
        if type == 'sets':
            return MongoSetsStore(engine)
        if type == 'rdfs':
            return MongoRDFsStore(engine)
        if type == 'postprocessors':
            return MongoPostProcessorStore(engine)
        if type == 'preprocessors':
            return MongoPreProcessorStore(engine)
        if type == 'templatenodes':
            return MongoTemplateNodeStore(engine)
        if type == 'patternnodes':
            return MongoPatternNodeStore(engine)
        if type == 'properties':
            return  MongoPropertyStore(engine)
        if type == 'defaults':
            return MongoDefaultVariablesStore(engine)
        if type == 'regexes':
            return MongoRegexesStore(engine)
        if type == 'denormals':
            return MongoDenormalStore(engine)
        if type == 'normals':
            return MongoNormalStore(engine)
        if type == 'genders':
            return MongoGenderStore(engine)
        if type == 'persons':
            return MongoPersonStore(engine)
        if type == 'person2s':
            return MongoPerson2Store(engine)
        if type == 'spelling':
            return MongoSpellingStore(engine)
        if type == 'licenses':
            return MongoLicenseKeysStore(engine)
        if type == 'usergroups':
            return MongoUserGroupsStore(engine)

        raise Exception("Unknone entity type [%s]"%type)

    @staticmethod
    def create_arguments():
        arguments = argparse.ArgumentParser(description='Program-Y Set Mongo Loader')

        arguments.add_argument('-e', '--entity', help="Name of entity to load")
        arguments.add_argument('-u', '--url', help="Mongo DB connection url")
        arguments.add_argument('-b', '--db', help="Mongo Database")
        arguments.add_argument('-f', '--file', help="File to load")
        arguments.add_argument('-d', '--dir', help="Directory to load files from")
        arguments.add_argument('-x', '--extension', help="Extension of file to load (dir only)")
        arguments.add_argument('-s', '--subdir', action='store_true', help="Recurse into all subdirectories")
        arguments.add_argument('-a', '--drop', action='store_true', help="Drop all collections first")
        arguments.add_argument('-v', '--verbose', action='store_true', help="Verbose output of loading process")
        arguments.add_argument('-z', '--verboseX', action='store_true', help="Verbose output of loading process")

        return arguments


if __name__ == '__main__':

    arguments = Uploader.create_arguments()
    try:
        args = arguments.parse_args()
        Uploader.upload(args.entity, args.url, args.db, args.file, args.dir, args.subdir, args.extension, drop_all=args.drop, verbose=args.verbose)

    except Exception as e:
        print("An error occured - %s"%e)
        arguments.print_help()