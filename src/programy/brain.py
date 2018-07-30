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

from programy.utils.logging.ylogger import YLogger
import re
import xml.etree.ElementTree as ET
try:
    import _pickle as pickle
except:
    import pickle

from programy.processors.processing import PreProcessorCollection
from programy.processors.processing import PostProcessorCollection
from programy.config.brain.brain import BrainConfiguration
from programy.mappings.denormal import DenormalCollection
from programy.mappings.gender import GenderCollection
from programy.mappings.maps import MapCollection
from programy.mappings.normal import NormalCollection
from programy.mappings.person import PersonCollection
from programy.mappings.person import Person2Collection
from programy.mappings.properties import PropertiesCollection
from programy.mappings.properties import RegexTemplatesCollection
from programy.mappings.properties import DefaultVariablesCollection
from programy.mappings.sets import SetCollection
from programy.dynamic.dynamics import DynamicsCollection
from programy.rdf.collection import RDFCollection
from programy.parser.aiml_parser import AIMLParser
from programy.services.service import ServiceFactory
from programy.utils.classes.loader import ClassLoader
from programy.dialog.dialog import Sentence
from programy.parser.tokenizer import Tokenizer
from programy.parser.pattern.factory import PatternNodeFactory
from programy.parser.template.factory import TemplateNodeFactory
from programy.storage.factory import StorageFactory

class Brain(object):

    def __init__(self, bot, configuration: BrainConfiguration):
        self._bot = bot
        self._configuration = configuration

        self._tokenizer = self.load_tokenizer()

        self._denormal_collection = DenormalCollection()
        self._normal_collection = NormalCollection()
        self._gender_collection = GenderCollection()
        self._person_collection = PersonCollection()
        self._person2_collection = Person2Collection()
        self._rdf_collection = RDFCollection()
        self._sets_collection = SetCollection()
        self._maps_collection = MapCollection()

        self._properties_collection = PropertiesCollection()
        self._variables_collection = DefaultVariablesCollection()
        self._defaults_collection = RegexTemplatesCollection()

        self._preprocessors = PreProcessorCollection()
        self._postprocessors = PostProcessorCollection()

        self._pattern_factory = None
        self._template_factory = None

        self._authentication = None
        self._authorisation = None

        self._default_oob = None
        self._oob = {}

        self._regex_templates = RegexTemplatesCollection()

        self._dynamics_collection = DynamicsCollection()

        self._aiml_parser = self.load_aiml_parser()

        self.load(self.configuration)


    def ylogger_type(self):
        return "brain"

    @property
    def id(self):
        return self._configuration.section_name

    @property
    def bot(self):
        return self._bot

    @property
    def configuration(self):
        return self._configuration

    @property
    def aiml_parser(self):
        return self._aiml_parser

    @property
    def denormals(self):
        return self._denormal_collection

    @property
    def normals(self):
        return self._normal_collection

    @property
    def genders(self):
        return self._gender_collection

    @property
    def persons(self):
        return self._person_collection

    @property
    def person2s(self):
        return self._person2_collection

    @property
    def rdf(self):
        return self._rdf_collection

    @property
    def sets(self):
        return self._sets_collection

    @property
    def maps(self):
        return self._maps_collection

    @property
    def properties(self):
        return self._properties_collection

    @property
    def variables(self):
        return self._variables_collection

    @property
    def preprocessors(self):
        return self._preprocessors

    @property
    def postprocessors(self):
        return self._postprocessors

    @property
    def pattern_factory(self):
        return self._pattern_factory

    @property
    def template_factory(self):
        return self._template_factory

    @property
    def authentication(self):
        return self._authentication

    @property
    def authorisation(self):
        return self._authorisation

    @property
    def default_oob(self):
        return self._default_oob

    @property
    def oobs(self):
        return self._oob

    @property
    def regex_templates(self):
        return self._regex_templates

    @property
    def dynamics(self):
        return self._dynamics_collection

    @property
    def tokenizer(self):
        return self._tokenizer

    def load_tokenizer(self):
        #TODO move into tokenizer code base
        if self.configuration is not None and self.configuration.tokenizer.classname is not None:
            YLogger.info(self, "Loading tokenizer from class [%s]", self.configuration.tokenizer.classname)
            tokenizer_class = ClassLoader.instantiate_class(self.configuration.tokenizer.classname)
            return tokenizer_class(self.configuration.tokenizer.split_chars)
        else:
            return Tokenizer(self.configuration.tokenizer.split_chars)

    def load_aiml_parser(self):
        self._load_pattern_nodes()
        self._load_template_nodes()
        return AIMLParser(self)

    def load_aiml(self):
        YLogger.info(self, "Loading aiml source brain")
        self._aiml_parser.load_aiml()

    def reload_aimls(self):
        YLogger.info(self, "Loading aiml source brain")
        self._aiml_parser.empty()
        self._aiml_parser.load_aiml()

    def load_binary(self, binaries_configuration):
        # TODO MOve into BinariesManager
        YLogger.info(self, "Loading binary brain from [%s]", binaries_configuration.binary_filename)
        try:

            storage_engine = self.bot.client.storage_factory.storage_engine(binaries_configuration.storage)
            binaries_storage = storage_engine.binaries_storage()
            self._aiml_parser = binaries_storage.load_binary()

            return False   # Tell caller, load succeeded and skip aiml load

        except Exception as excep:
            YLogger.exception(self, "Failed to load binary file", excep)
            if binaries_configuration.load_aiml_on_binary_fail is True:
                return True   # Tell caller, load failed and to load aiml directly
            else:
                raise excep

    def save_binary(self, binaries_configuration):
        # TODO MOve into BinariesManager
        try:
            if self.bot.client.storage_factor.storage_engine_available(StorageFactory.BINARIES) is True:
                YLogger.info(self, "Saving binary brain to [%s]", StorageFactory.BINARIES)

                storage_engine = self.bot.client.storage_factory.storage_engine(StorageFactory.BINARIES)
                binaries_storage = storage_engine.binaries_storage()
                binaries_storage.save_binary(self._aiml_parser)

        except Exception as failure:
            YLogger.info(self, "Failed to save binary [%s]", failure)

    def load(self, configuration: BrainConfiguration):

        load_aiml = True
        if self.configuration.binaries.load_binary is True:
            load_aiml = self.load_binary(configuration.binaries)

        if load_aiml is True:
            self.load_aiml()

        if configuration.binaries.save_binary is True:
            self.save_binary(configuration.binaries)

        YLogger.info(self, "Loading collections")
        self.load_collections()

        YLogger.info(self, "Loading services")
        self.load_services(configuration)

        YLogger.info(self, "Loading security services")
        self.load_security_services(configuration)

        YLogger.info(self, "Loading oob processors")
        self.load_oob_processors(configuration)

        YLogger.info(self, "Loading regex templates")
        self.load_regex_templates()

        YLogger.info(self, "Loading dynamics sets, maps and vars")
        self.load_dynamics()

    def dump_brain_tree(self):
        # TODO MOve into BrainTreeManager
        if self.configuration.braintree.create is True:
            YLogger.debug(self, "Dumping AIML Graph as tree to [%s]", self._configuration.braintree.file)

            client_context = self.bot.client.create_client_context("system")
            self.aiml_parser.pattern_parser.save_braintree(
                client_context,
                self.configuration.braintree)

    def _load_denormals(self):
        self._denormal_collection.empty()
        self._denormal_collection.load(self.bot.client.storage_factory)

    def _load_normals(self):
        self._normal_collection.empty()
        self._normal_collection.load(self.bot.client.storage_factory)

    def _load_genders(self):
        self._gender_collection.empty()
        self._gender_collection.load(self.bot.client.storage_factory)

    def _load_persons(self):
        self._person_collection.empty()
        self._person_collection.load(self.bot.client.storage_factory)

    def _load_person2s(self):
        self._person2_collection.empty()
        self._person2_collection.load(self.bot.client.storage_factory)

    def _load_properties(self):
        self._properties_collection.empty()
        self._properties_collection.load(self.bot.client.storage_factory)

    def _load_variables(self):
        self._variables_collection.empty()
        self._variables_collection.load(self.bot.client.storage_factory)

    def _load_maps(self):
        self._maps_collection.empty()
        self._maps_collection.load(self.bot.client.storage_factory)

    def reload_map(self, mapname):
        if self._maps_collection.contains(mapname):
            self._maps_collection.reload(self.bot.client.storage_factory, mapname)

    def _load_sets(self):
        self._sets_collection.empty()
        self._sets_collection.load(self.bot.client.storage_factory)

    def reload_set(self, setname):
        if self._sets_collection.contains(setname):
            self._sets_collection.reload(self.bot.client.storage_factory, setname)

    def _load_rdfs(self):
        self._rdf_collection.empty()
        self._rdf_collection.load(self.bot.client.storage_factory)

    def reload_rdf(self, rdfname):
        if self._rdf_collection.contains(rdfname):
            self._rdf_collection.reload(self.bot.client.storage_factory, rdfname)

    def _load_preprocessors(self):
        self._preprocessors.empty()
        self._preprocessors.load(self.bot.client.storage_factory)

    def _load_postprocessors(self):
        self._postprocessors.empty()
        self._postprocessors.load(self.bot.client.storage_factory)

    def _load_pattern_nodes(self):
        self._pattern_factory = PatternNodeFactory()
        self._pattern_factory.load(self.bot.client.storage_factory)

    def _load_template_nodes(self):
        self._template_factory = TemplateNodeFactory()
        self._template_factory.load(self.bot.client.storage_factory)

    def load_collections(self):
        self._load_denormals()
        self._load_normals()
        self._load_genders()
        self._load_persons()
        self._load_person2s()
        self._load_properties()
        self._load_variables()
        self._load_rdfs()
        self._load_sets()
        self._load_maps()
        self._load_preprocessors()
        self._load_postprocessors()

    def load_services(self, configuration):
        ServiceFactory.preload_services(configuration.services)

    def load_security_services(self, configuration):
        # TODO MOve into Security Manager
        if configuration.security is not None:
            if configuration.security.authentication is not None:
                if configuration.security.authentication.classname is not None:
                    try:
                        classobject = ClassLoader.instantiate_class(
                            configuration.security.authentication.classname)
                        self._authentication = classobject(configuration.security.authentication)
                        self._authentication.initialise(self.bot.client)
                    except Exception as excep:
                        YLogger.exception(self, "Failed to load security services", excep)
            else:
                YLogger.debug(self, "No authentication configuration defined")

            if configuration.security.authorisation is not None:
                if configuration.security.authorisation.classname is not None:
                    try:
                        classobject = ClassLoader.instantiate_class(
                            configuration.security.authorisation.classname)
                        self._authorisation = classobject(configuration.security.authorisation)
                        self._authorisation.initialise(self.bot.client)
                    except Exception as excep:
                        YLogger.exception(self, "Failed to instatiate authorisation class", excep)
            else:
                YLogger.debug(self, "No authorisation configuration defined")

        else:
            YLogger.debug(self, "No security configuration defined, running open...")

    def load_dynamics(self):
        if self.configuration.dynamics is not None:
            self._dynamics_collection.load_from_configuration(self.configuration.dynamics)
        else:
            YLogger.debug(self, "No dynamics configuration defined...")

    def pre_process_question(self, client_context, question):
        return self.preprocessors.process(client_context, question)

    def load_oob_processors(self, configuration):
        # TODO MOve into OOBManager
        if configuration.oob is not None:
            if configuration.oob.default() is not None:
                try:
                    YLogger.info(self, "Loading default oob")
                    classobject = ClassLoader.instantiate_class(configuration.oob.default().classname)
                    self._default_oob = classobject()
                except Exception as excep:
                    YLogger.exception(self, "Failed to load OOB Processor", excep)

            for oob_name in  configuration.oob.oobs():
                try:
                    YLogger.info(self, "Loading oob: %s", oob_name)
                    classobject = ClassLoader.instantiate_class(configuration.oob.oob(oob_name).classname)
                    self._oob[oob_name] = classobject()
                except Exception as excep:
                    YLogger.exception(self, "Failed to load OOB", excep)

    def strip_oob(self, response):
        # TODO MOve into OOBManager
        match = re.compile(r"(.*)(<\s*oob\s*>.*<\/\s*oob\s*>)(.*)")
        groupings = match.match(response)
        if groupings is not None:
            front = groupings.group(1).strip()
            back = groupings.group(3).strip()
            response = ""
            if front != "":
                response = front + " "
            response += back
            oob = groupings.group(2)
            return response, oob
        return response, None

    def process_oob(self, client_context, oob_command):
        # TODO MOve into OOBManager
        oob_content = ET.fromstring(oob_command)

        if oob_content.tag == 'oob':
            for child in oob_content.findall('./'):
                if child.tag in self._oob:
                    oob_class = self._oob[child.tag]
                    return oob_class.process_out_of_bounds(client_context, child)
                return self._default_oob.process_out_of_bounds(client_context, child)

        return ""

    def load_regex_templates(self):
        if self.bot.client.storage_factory.storage_engine_available(StorageFactory.REGEX_TEMPLATES) is True:
            storage_engine = self.bot.client.storage_factory.storage_engine(StorageFactory.REGEX_TEMPLATES)
            regex_store = storage_engine.regex_store()
            regex_store.load(self._regex_templates)

    def post_process_response(self, client_context, response: str):
        return self.postprocessors.process(client_context, response)

    def failed_authentication(self, client_context):
        # TODO Move into security manager
        YLogger.error(client_context, "[%s] failed authentication!")

        # If we have an SRAI defined, then use that
        if self.authentication.configuration.denied_srai is not None:
            match_context = self._aiml_parser.match_sentence(client_context,
                                                             Sentence(self._bot.brain.tokenizer, self.authentication.configuration.denied_srai),
                                                             topic_pattern="*",
                                                             that_pattern="*")
            # If the SRAI matched then return the result
            if match_context is not None:
                return self.resolve_matched_template(client_context, match_context)

        # Otherswise return the static text, which is either
        #    User defined via config.yaml
        #    Or use the default value BrainSecurityConfiguration.DEFAULT_ACCESS_DENIED
        return self.authentication.configuration.denied_text

    def authenticate_user(self, client_context):
        # TODO Move into security manager
        if self.authentication is not None:
            if self.authentication.authenticate(client_context) is False:
                return self.failed_authentication(client_context)
        return None

    def resolve_matched_template(self, client_context, match_context):

        template_node = match_context.template_node()

        YLogger.debug(client_context, "AIML Parser evaluating template [%s]", template_node.to_string())

        response = template_node.template.resolve(client_context)

        if "<oob>" in response:
            response, oob = self.strip_oob(response)
            if oob is not None:
                oob_response = self.process_oob(client_context, oob)
                response = response + " " + oob_response

        return response

    def ask_question(self, client_context, sentence, srai=False):

        client_context.brain = self

        authenticated = self.authenticate_user(client_context)
        if authenticated is not None:
            return authenticated

        conversation = client_context.bot.get_conversation(client_context)

        topic_pattern = conversation.get_topic_pattern(client_context)

        that_pattern = conversation.get_that_pattern(client_context, srai)

        match_context = self._aiml_parser.match_sentence(client_context,
                                                         sentence,
                                                         topic_pattern=topic_pattern,
                                                         that_pattern=that_pattern)

        if match_context is not None:
            return self.resolve_matched_template(client_context, match_context)

        return None

