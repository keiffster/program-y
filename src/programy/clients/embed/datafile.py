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
from programy.clients.events.console.client import ConsoleBotClient
from programy.config.programy import ProgramyConfiguration
from programy.clients.args import CommandLineClientArguments
from programy.utils.substitutions.substitues import Substitutions
from programy.storage.config import FileStorageConfiguration
from programy.storage.stores.file.store.config import FileStoreConfiguration
from programy.storage.factory import StorageFactory


class EmbeddedDataFileBot(ConsoleBotClient):

    def __init__(self, files={}, defaults=False, logging_filename=None):
        self._files = files
        self._defaults = defaults

        filepath = os.path.dirname(__file__) + os.sep
        if logging_filename is not None:
            self._logging_filename = logging_filename
        else:
            self._logging_filename = filepath + 'basicbot/logging.yaml'

        ConsoleBotClient.__init__(self, "Console")

    def _render_callback(self):
        return False

    def parse_arguments(self, argument_parser):
        client_args = CommandLineClientArguments(self, parser=None)
        if self._logging_filename is not None:
            client_args._logging = self._logging_filename
        return client_args

    #def initiate_logging(self, arguments):
    #    pass

    def load_configuration(self, arguments, subs: Substitutions = None):
        client_config = self.get_client_configuration()

        client_config.storage.storage_configurations['file'] = FileStorageConfiguration()

        filepath = os.path.dirname(__file__) + os.sep

        client_config.storage.entity_store[StorageFactory.PATTERN_NODES] = 'file'
        if 'patterns' in self._files:
            client_config.storage.storage_configurations['file']._pattern_nodes_storage = FileStoreConfiguration(file=self._files['patterns'], fileformat="text")
        else:
            # Default if pattern node file not specified
            client_config.storage.storage_configurations['file']._pattern_nodes_storage = FileStoreConfiguration(file=filepath + 'basicbot/nodes/pattern_nodes.conf', fileformat="text")

        client_config.storage.entity_store[StorageFactory.TEMPLATE_NODES] = 'file'
        if 'templates' in self._files:
            client_config.storage.storage_configurations['file']._template_nodes_storage = FileStoreConfiguration(file=self._files['templates'], fileformat="text")
        else:
            # Default if template node file not specified
            client_config.storage.storage_configurations['file']._template_nodes_storage = FileStoreConfiguration(file=filepath + 'basicbot/nodes/template_nodes.conf', fileformat="text")

        if 'aiml' in self._files:
            client_config.storage.entity_store[StorageFactory.CATEGORIES] = 'file'
            client_config.storage.storage_configurations['file']._categories_storage = FileStoreConfiguration(dirs=self._files['aiml'], fileformat="xml",
                                                                                                              extension="aiml", encoding="utf-8",
                                                                                                              subdirs=True,
                                                                                                              delete_on_start=False)

        client_config.storage.entity_store[StorageFactory.LEARNF] = 'file'
        if 'learnf' in self._files:
            client_config.storage.storage_configurations['file']._learnf_storage = FileStoreConfiguration(dirs=self._files['learnf'], fileformat="xml",
                                                                                                              extension="aiml", encoding="utf-8",
                                                                                                              subdirs=True,
                                                                                                              delete_on_start=False)
        elif self._defaults is True:
            client_config.storage.storage_configurations['file']._learnf_storage = FileStoreConfiguration(dirs=filepath + 'basicbot/categories/learnf', fileformat="xml",
                                                                                                              extension="aiml", encoding="utf-8",
                                                                                                              subdirs=True,
                                                                                                              delete_on_start=False)

        client_config.storage.entity_store[StorageFactory.PROPERTIES] = 'file'
        if 'properties' in self._files:
            client_config.storage.storage_configurations['file']._properties_storage = FileStoreConfiguration(file=self._files['properties'], fileformat="text")
            
        elif self._defaults is True:
            client_config.storage.storage_configurations['file']._properties_storage = FileStoreConfiguration(
                file=filepath + 'basicbot/properties/properties.txt', fileformat="text")

        client_config.storage.entity_store[StorageFactory.DEFAULTS] = 'file'
        if 'defaults' in self._files:
            client_config.storage.storage_configurations['file']._defaults_storage = FileStoreConfiguration(file=self._files['defaults'], fileformat="text")
        
        elif self._defaults is True:
            client_config.storage.storage_configurations['file']._defaults_storage = FileStoreConfiguration(
                file=filepath + 'basicbot/properties/defaults.txt', fileformat="text")

        client_config.storage.entity_store[StorageFactory.SETS] = 'file'
        if 'sets' in self._files:
            client_config.storage.storage_configurations['file']._sets_storage = FileStoreConfiguration(dirs=self._files['sets'], fileformat="text",
                                                                                                              extension="txt", encoding="utf-8",
                                                                                                              subdirs=True,
                                                                                                              delete_on_start=False)
        elif self._defaults is True:
            client_config.storage.storage_configurations['file']._sets_storage = FileStoreConfiguration(dirs=[filepath + 'basicbot/sets'], fileformat="text",
                                                                                                              extension="txt", encoding="utf-8",
                                                                                                              subdirs=True,
                                                                                                              delete_on_start=False)

        client_config.storage.entity_store[StorageFactory.MAPS] = 'file'
        if 'maps' in self._files:
            client_config.storage.storage_configurations['file']._maps_storage = FileStoreConfiguration(dirs=self._files['maps'], fileformat="text",
                                                                                                              extension="txt", encoding="utf-8",
                                                                                                              subdirs=True,
                                                                                                              delete_on_start=False)
        elif self._defaults is True:
            client_config.storage.storage_configurations['file']._maps_storage = FileStoreConfiguration(dirs=['basicbot/maps'], fileformat="text",
                                                                                                              extension="txt", encoding="utf-8",
                                                                                                              subdirs=True,
                                                                                                              delete_on_start=False)

        client_config.storage.entity_store[StorageFactory.RDF] = 'file'
        if 'rdfs' in self._files:
            client_config.storage.storage_configurations['file']._rdfs_storage = FileStoreConfiguration(dirs=self._files['rdfs'], fileformat="text",
                                                                                                              extension="txt", encoding="utf-8",
                                                                                                              subdirs=True,
                                                                                                              delete_on_start=False)
        elif self._defaults is True:
            client_config.storage.storage_configurations['file']._rdfs_storage = FileStoreConfiguration(dirs=['basicbot/rdfs'], fileformat="text",
                                                                                                              extension="txt", encoding="utf-8",
                                                                                                              subdirs=True,
                                                                                                              delete_on_start=False)

        client_config.storage.entity_store[StorageFactory.DENORMAL] = 'file'
        if 'denormals' in self._files:
            client_config.storage.storage_configurations['file']._denormal_storage = FileStoreConfiguration(file=self._files['denormals'], fileformat="text")
        elif self._defaults is True:
            client_config.storage.storage_configurations['file']._denormal_storage = FileStoreConfiguration(file='basibot/lookups/denormals.txt', fileformat="text")

        client_config.storage.entity_store[StorageFactory.NORMAL] = 'file'
        if 'normals' in self._files:
            client_config.storage.storage_configurations['file']._normal_storage = FileStoreConfiguration(file=self._files['normals'], fileformat="text")
        elif self._defaults is True:
            client_config.storage.storage_configurations['file']._normal_storage = FileStoreConfiguration(file='basicbot/lookups/normals.txt', fileformat="text")

        client_config.storage.entity_store[StorageFactory.GENDER] = 'file'
        if 'genders' in self._files:
            client_config.storage.storage_configurations['file']._gender_storage = FileStoreConfiguration(file=self._files['genders'], fileformat="text")
        elif self._defaults is True:
            client_config.storage.storage_configurations['file']._gender_storage = FileStoreConfiguration(
                file='basicbot/lookups/genders.txt', fileformat="text")

        client_config.storage.entity_store[StorageFactory.PERSON] = 'file'
        if 'persons' in self._files:
            client_config.storage.storage_configurations['file']._person_storage = FileStoreConfiguration(file=self._files['persons'], fileformat="text")
        elif self._defaults is True:
            client_config.storage.storage_configurations['file']._person_storage = FileStoreConfiguration(
                file='basicbot/lookups/persons.txt', fileformat="text")

        client_config.storage.entity_store[StorageFactory.PERSON2] = 'file'
        if 'person2s' in self._files:
            client_config.storage.storage_configurations['file']._person2_storage = FileStoreConfiguration(file=self._files['person2s'], fileformat="text")
        elif self._defaults is True:
            client_config.storage.storage_configurations['file']._person2_storage = FileStoreConfiguration(file='basicbot/lookups/person2s.txt', fileformat="text")

        client_config.storage.entity_store[StorageFactory.REGEX_TEMPLATES] = 'file'
        if 'regexes' in self._files:
            client_config.storage.storage_configurations['file']._regex_storage = FileStoreConfiguration(file=self._files['regexes'], fileformat="text")
        elif self._defaults is True:
            client_config.storage.storage_configurations['file']._regex_storage = FileStoreConfiguration(
                file='basicbot/regex/regex-templates.txt', fileformat="text")

        if 'triggers' in self._files:
            client_config.storage.entity_store[StorageFactory.TRIGGERS] = 'file'
            client_config.storage.storage_configurations['file']._triggers_storage = FileStoreConfiguration(file=self._files['triggers'], fileformat="text")

        if 'usergroups' in self._files:
            client_config.storage.entity_store[StorageFactory.USERGROUPS] = 'file'
            client_config.storage.storage_configurations['file']._usergroups_storage = FileStoreConfiguration(file=self._files['usergroups'], fileformat="text")

        if 'spellings' in self._files:
            client_config.storage.entity_store[StorageFactory.SPELLING_CORPUS] = 'file'
            client_config.storage.storage_configurations['file']._spelling_storage = FileStoreConfiguration(file=self._files['spellings'], fileformat="text")

        client_config.storage.entity_store[StorageFactory.PREPROCESSORS] = 'file'
        if 'preprocessors' in self._files:
            client_config.storage.storage_configurations['file']._preprocessors_storage = FileStoreConfiguration(file=self._files['preprocessors'], fileformat="text")
        elif self._defaults is True:
            client_config.storage.storage_configurations['file']._preprocessors_storage = FileStoreConfiguration(file=filepath + 'basicbot/processing/preprocessors.conf', fileformat="text")

        client_config.storage.entity_store[StorageFactory.POSTPROCESSORS] = 'file'
        if 'postprocessors' in self._files:
            client_config.storage.storage_configurations['file']._postprocessors_storage = FileStoreConfiguration(file=self._files['postprocessors'], fileformat="text")
        elif self._defaults is True:
            client_config.storage.storage_configurations['file']._postprocessors_storage = FileStoreConfiguration(file=filepath + 'basicbot/processing/postprocessors.conf', fileformat="text")

        if 'postquestionprocessors' in self._files:
            client_config.storage.entity_store[StorageFactory.POSTQUESTIONPROCESSORS] = 'file'
            client_config.storage.storage_configurations['file']._postquestionprocessors_storage = FileStoreConfiguration(file=self._files['postquestionprocessors'], fileformat="text")

        if 'licenses' in self._files:
            client_config.storage.entity_store[StorageFactory.LICENSE_KEYS] = 'file'
            client_config.storage.storage_configurations['file']._license_storage = FileStoreConfiguration(file=self._files['licenses'], fileformat="text")

        if 'errors' in self._files:
            client_config.storage.entity_store[StorageFactory.ERRORS] = 'file'
            client_config.storage.storage_configurations['file']._errors_storage = FileStoreConfiguration(file=self._files['errors'], fileformat="text")

        if 'duplicates' in self._files:
            client_config.storage.entity_store[StorageFactory.ERRORS] = 'file'
            client_config.storage.storage_configurations['file']._duplicates_storage = FileStoreConfiguration(file=self._files['duplicates'], fileformat="text")

        if 'binaries' in self._files:
            client_config.storage.entity_store[StorageFactory.BINARIES] = 'file'
            client_config.storage.storage_configurations['file']._binaries_storage = FileStoreConfiguration(file=self._files['binaries'], fileformat="text")

        if 'braintrees' in self._files:
            client_config.storage.entity_store[StorageFactory.BRAINTREE] = 'file'
            client_config.storage.storage_configurations['file']._braintree_storage = FileStoreConfiguration(file=self._files['braintrees'], fileformat="text")

        if 'conversations' in self._files:
            client_config.storage.entity_store[StorageFactory.CONVERSATIONS] = 'file'
            client_config.storage.storage_configurations['file']._conversation_storage = FileStoreConfiguration(dirs=self._files['conversations'], fileformat="text",
                                                                                                                extension="txt", encoding="utf-8",
                                                                                                                subdirs=True,
                                                                                                                delete_on_start=False)

        if 'oobs' in self._files:
            client_config.storage.entity_store[StorageFactory.OOBS] = 'file'
            client_config.storage.storage_configurations['file']._oobs_storage = FileStoreConfiguration(file=self._files['oobs'], fileformat="text")

        self._configuration = ProgramyConfiguration(client_config)

    def ask_question(self, question):
        client_context = self.create_client_context("testuser")
        return self.renderer.render(client_context, self.process_question(client_context, question))


if __name__ == '__main__':

    files1 = {'aiml'         : ['/Users/keith/Documents/Development/Python/Projects/AIML/y-bot/storage/categories']}

    files2 = {'aiml'         : ['/Users/keith/Documents/Development/Python/Projects/AIML/y-bot/storage/categories'],
             'learnf'       : ['/Users/keith/Documents/Development/Python/Projects/AIML/y-bot/storage/categories/learnf'],
             'properties'   : '/Users/keith/Documents/Development/Python/Projects/AIML/y-bot/storage/properties/properties.txt',
             'defaults'     : '/Users/keith/Documents/Development/Python/Projects/AIML/y-bot/storage/properties/defaults.txt',
             'sets'         : ['/Users/keith/Documents/Development/Python/Projects/AIML/y-bot/storage/sets'],
             'maps'         : ['/Users/keith/Documents/Development/Python/Projects/AIML/y-bot/storage/maps'],
             'rdfs'         : ['/Users/keith/Documents/Development/Python/Projects/AIML/y-bot/storage/rdfs'],
             'denormals'    : '/Users/keith/Documents/Development/Python/Projects/AIML/y-bot/storage/lookups/denormal.txt',
             'normals'      : '/Users/keith/Documents/Development/Python/Projects/AIML/y-bot/storage/lookups/normal.txt',
             'genders'      : '/Users/keith/Documents/Development/Python/Projects/AIML/y-bot/storage/lookups/gender.txt',
             'persons'      : '/Users/keith/Documents/Development/Python/Projects/AIML/y-bot/storage/lookups/person.txt',
             'person2s'     : '/Users/keith/Documents/Development/Python/Projects/AIML/y-bot/storage/lookups/person2.txt',
             'triggers'     : '/Users/keith/Documents/Development/Python/Projects/AIML/y-bot/storage/triggers/triggers.txt',
             'regexes'      : '/Users/keith/Documents/Development/Python/Projects/AIML/y-bot/storage/regex/regex-templates.txt',
             'usergroups'     : '/Users/keith/Documents/Development/Python/Projects/AIML/y-bot/storage/security/usergroups.yaml',
             'spellings'     : '/Users/keith/Documents/Development/Python/Projects/AIML/y-bot/storage/spelling/corpus.txt',
             'preprocessors': '/Users/keith/Documents/Development/Python/Projects/AIML/y-bot/storage/processing/preprocessors.conf',
             'postprocessors': '/Users/keith/Documents/Development/Python/Projects/AIML/y-bot/storage/processing/postprocessors.conf',
             'postquestionprocessors': '/Users/keith/Documents/Development/Python/Projects/AIML/y-bot/storage/processing/postquestionprocessors.conf',
             'licenses'     : '/Users/keith/Documents/Development/Python/Projects/AIML/y-bot/storage/licenses/license.keys',
             'conversations': '/Users/keith/Documents/Development/Python/Projects/AIML/y-bot/storage/conversations',
             'duplicates'   : '/Users/keith/Documents/Development/Python/Projects/AIML/y-bot/storage/debug/duplicates.txt',
             'errors'       : '/Users/keith/Documents/Development/Python/Projects/AIML/y-bot/storage/debug/errors.txt',
             'services'     : '/Users/keith/Documents/Development/Python/Projects/AIML/y-bot/storage/services',
             }

    print("Loading Bot Brain....please wait!")
    my_bot = EmbeddedDataFileBot(files1, defaults=True)

    print("Asked 'Hello', Response '%s'" % my_bot.ask_question("Hello"))
    print("Asked 'What are you', Response '%s'" % my_bot.ask_question("What are you"))
    print("Asked 'Where are you',  Response '%s'" % my_bot.ask_question("Where are you"))

