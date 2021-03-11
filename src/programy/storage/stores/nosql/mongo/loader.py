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
from programy.storage.stores.nosql.mongo.store.processors import MongoPreProcessorStore
from programy.storage.stores.nosql.mongo.store.processors import MongoPostProcessorStore
from programy.storage.stores.nosql.mongo.store.processors import MongoPostQuestionProcessorStore
from programy.storage.stores.nosql.mongo.store.triggers import MongoTriggerStore
from programy.storage.stores.nosql.mongo.store.oobs import MongoOOBStore
from programy.storage.stores.nosql.mongo.store.services import MongoServiceStore
from programy.utils.console.console import outputLog


class Uploader:

    @staticmethod
    def upload(storetype, url, database, filename, dirname, subdir, extension, verbose=False):
        config = MongoStorageConfiguration()
        config.url = url
        config.database = database
        config.drop_all_first = False
        engine = MongoStorageEngine(config)
        engine.initialise()
        store = Uploader._get_store(storetype, engine)

        outputLog(None, "Emptying [%s]" % storetype)
        store.empty()

        outputLog(None, "Loading [%s]" % storetype)
        if filename is not None:
            count, success = store.upload_from_file(filename, fileformat=Store.TEXT_FORMAT, commit=True, verbose=verbose)
            outputLog(None, "Lines processed: %d" % count)
            outputLog(None, "Entities successful: %d" % success)

        elif dirname is not None:
            count, success = store.upload_from_directory(directory=dirname,
                                                         subdir=subdir,
                                                         extension=extension,
                                                         commit=True,
                                                         verbose=verbose)
            outputLog(None, "Lines processed: %d" % count)
            outputLog(None, "Entities successful: %d" % success)

        else:
            raise Exception("You must specify either --file or --dir")

        return count, success

    @staticmethod
    def _get_store(storetype, engine):
        if storetype == 'categories':
            return MongoCategoryStore(engine)
        if storetype == 'maps':
            return MongoMapsStore(engine)
        if storetype == 'sets':
            return MongoSetsStore(engine)
        if storetype == 'rdfs':
            return MongoRDFsStore(engine)
        if storetype == 'preprocessors':
            return MongoPreProcessorStore(engine)
        if storetype == 'postprocessors':
            return MongoPostProcessorStore(engine)
        if storetype == 'postquestionprocessors':
            return MongoPostQuestionProcessorStore(engine)
        if storetype == 'templatenodes':
            return MongoTemplateNodeStore(engine)
        if storetype == 'patternnodes':
            return MongoPatternNodeStore(engine)
        if storetype == 'properties':
            return MongoPropertyStore(engine)
        if storetype == 'defaults':
            return MongoDefaultVariablesStore(engine)
        if storetype == 'regexes':
            return MongoRegexesStore(engine)
        if storetype == 'denormals':
            return MongoDenormalStore(engine)
        if storetype == 'normals':
            return MongoNormalStore(engine)
        if storetype == 'genders':
            return MongoGenderStore(engine)
        if storetype == 'persons':
            return MongoPersonStore(engine)
        if storetype == 'person2s':
            return MongoPerson2Store(engine)
        if storetype == 'spelling':
            return MongoSpellingStore(engine)
        if storetype == 'licenses':
            return MongoLicenseKeysStore(engine)
        if storetype == 'usergroups':
            return MongoUserGroupsStore(engine)
        if storetype == 'triggers':
            return MongoTriggerStore(engine)
        if storetype == 'oobs':
            return MongoOOBStore(engine)
        if storetype == 'services':
            return MongoServiceStore(engine)

        raise Exception("Unknone entity storetype [%s]" % storetype)

    @staticmethod
    def create_arguments():
        loader_args = argparse.ArgumentParser(description='Program-Y Set Mongo Loader')

        loader_args.add_argument('-e', '--entity', help="Name of entity to load")
        loader_args.add_argument('-u', '--url', help="Mongo DB connection url")
        loader_args.add_argument('-b', '--db', help="Mongo Database")
        loader_args.add_argument('-f', '--file', help="File to load")
        loader_args.add_argument('-d', '--dir', help="Directory to load files from")
        loader_args.add_argument('-x', '--extension', help="Extension of file to load (dir only)")
        loader_args.add_argument('-s', '--subdir', action='store_true', help="Recurse into all subdirectories")
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
                            args.db,
                            args.file,
                            args.dir,
                            args.subdir,
                            args.extension,
                            verbose=args.verbose)

        except Exception as excep:
            outputLog(None, "Mongo loader error - %s" % excep)
            arguments.print_help()

        except SystemExit as excep:
            outputLog(None, "Mongo loader error - %s" % excep)
            arguments.print_help()

if __name__ == '__main__':

    Uploader.run()                          #pragma: no cover
