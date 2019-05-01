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
from programy.dialog.tokenizer.tokenizer import Tokenizer
from programy.parser.pattern.factory import PatternNodeFactory
from programy.parser.template.factory import TemplateNodeFactory
from programy.binaries import BinariesManager
from programy.braintree import BraintreeManager
from programy.security.manager import SecurityManager
from programy.oob.handler import OOBHandler


class Brain(object):

    def __init__(self, bot, configuration: BrainConfiguration):

        assert (bot is not None)
        assert (configuration is not None)

        self._questions = 0

        self._bot = bot
        self._configuration = configuration

        self._binaries = BinariesManager(configuration.binaries)
        self._braintree = BraintreeManager(configuration.braintree)
        self._tokenizer = Tokenizer.load_tokenizer(configuration)

        self._denormal_collection = DenormalCollection()
        self._normal_collection = NormalCollection()
        self._gender_collection = GenderCollection()
        self._person_collection = PersonCollection()
        self._person2_collection = Person2Collection()
        self._rdf_collection = RDFCollection()
        self._sets_collection = SetCollection()
        self._maps_collection = MapCollection()

        self._properties_collection = PropertiesCollection()
        self._default_variables_collection = DefaultVariablesCollection()

        self._preprocessors = PreProcessorCollection()
        self._postprocessors = PostProcessorCollection()

        self._pattern_factory = None
        self._template_factory = None

        self._security = SecurityManager(configuration.security)

        self._oobhandler = OOBHandler(configuration.oob)

        self._regex_templates = RegexTemplatesCollection()

        self._dynamics_collection = DynamicsCollection()

        self._aiml_parser = self.load_aiml_parser()

        self.load(self.configuration)

    def ylogger_type(self):
        return "brain"

    @property
    def num_questions(self):
        return self._questions

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
    def default_variables(self):
        return self._default_variables_collection

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
    def regex_templates(self):
        return self._regex_templates

    @property
    def dynamics(self):
        return self._dynamics_collection

    @property
    def tokenizer(self):
        return self._tokenizer

    @property
    def security(self):
        return self._security

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

    def load(self, configuration: BrainConfiguration):

        load_aiml = True
        if self.configuration.binaries.load_binary is True:
            load_aiml = self._binaries.load_binary(self.bot.client.storage_factory)

        if load_aiml is True:
            self.load_aiml()

        if configuration.binaries.save_binary is True:
            self._binaries.save_binary(self.bot.client.storage_factory)

        YLogger.info(self, "Loading collections")
        self.load_collections()

        YLogger.info(self, "Loading services")
        self.load_services(configuration)

        YLogger.info(self, "Loading security services")
        self.load_security_services()

        YLogger.info(self, "Loading oob processors")
        self._oobhandler.load_oob_processors()

        YLogger.info(self, "Loading regex templates")
        self.load_regex_templates()

        YLogger.info(self, "Loading dynamics sets, maps and vars")
        self.load_dynamics()

    def dump_brain_tree(self, client_context):
        self._braintree.dump_brain_tree(client_context)

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

    def _load_default_variables(self):
        self._default_variables_collection.empty()
        self._default_variables_collection.load(self.bot.client.storage_factory)

        self._set_system_defined()

    def _set_system_defined(self):
        self.set_sentiment_scores(0.0, 0.5)

    def set_sentiment_scores(self, positivity, subjectivity):
        if self._default_variables_collection.has_variable("positivity") is False:
            self._default_variables_collection.set_value("positivity", str(positivity))

        if self._default_variables_collection.has_variable("subjectivity") is False:
            self._default_variables_collection.set_value("subjectivity", str(subjectivity))

    def _load_maps(self):
        self._maps_collection.empty()
        self._maps_collection.load(self.bot.client.storage_factory)

    def reload_map(self, mapname):
        if self._maps_collection.contains(mapname):
            self._maps_collection.reload(self.bot.client.storage_factory, mapname)
        else:
            YLogger.error(self, "Unknown map name [%s], unable to reload ", mapname)

    def _load_sets(self):
        self._sets_collection.empty()
        self._sets_collection.load(self.bot.client.storage_factory)

    def reload_set(self, setname):
        if self._sets_collection.contains(setname):
            self._sets_collection.reload(self.bot.client.storage_factory, setname)
        else:
            YLogger.error(self, "Unknown set name [%s], unable to reload ", setname)

    def _load_rdfs(self):
        self._rdf_collection.empty()
        self._rdf_collection.load(self.bot.client.storage_factory)

    def reload_rdf(self, rdfname):
        if self._rdf_collection.contains(rdfname):
            self._rdf_collection.reload(self.bot.client.storage_factory, rdfname)
        else:
            YLogger.error(self, "Unknown rdf name [%s], unable to reload ", rdfname)

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
        self._load_default_variables()
        self._load_rdfs()
        self._load_sets()
        self._load_maps()
        self._load_preprocessors()
        self._load_postprocessors()

    def load_services(self, configuration):
        ServiceFactory.preload_services(configuration.services)

    def load_security_services(self):
        self._security.load_security_services(self.bot.client)

    def load_dynamics(self):
        if self.configuration.dynamics is not None:
            self._dynamics_collection.load_from_configuration(self.configuration.dynamics)
        else:
            YLogger.debug(self, "No dynamics configuration defined...")

    def load_regex_templates(self):
        self._regex_templates.load(self.bot.client.storage_factory)

    def pre_process_question(self, client_context, question):
        return self.preprocessors.process(client_context, question)

    def post_process_response(self, client_context, response: str):
        return self.postprocessors.process(client_context, response)

    def failed_authentication(self, client_context):
        return self._security.failed_authentication(client_context)

    def authenticate_user(self, client_context):
        return self._security.authenticate_user(client_context)

    def resolve_matched_template(self, client_context, match_context):

        assert (client_context is not None)
        assert (match_context is not None)

        template_node = match_context.template_node()

        YLogger.debug(client_context, "AIML Parser evaluating template [%s]", template_node.to_string())

        response = template_node.template.resolve(client_context)

        if self._oobhandler.oob_in_response(response) is True:
            response = self._oobhandler.handle(client_context, response)

        return response

    def ask_question(self, client_context, sentence, srai=False):

        assert (client_context is not None)
        assert (client_context.bot is not None)
        assert (self._aiml_parser is not None)

        client_context.brain = self

        authenticated = self.authenticate_user(client_context)
        if authenticated is not None:
            return authenticated

        conversation = client_context.bot.get_conversation(client_context)

        if conversation is not None:

            self._questions += 1

            topic_pattern = conversation.get_topic_pattern(client_context)

            that_pattern = conversation.get_that_pattern(client_context, srai)

            match_context = self._aiml_parser.match_sentence(client_context,
                                                             sentence,
                                                             topic_pattern=topic_pattern,
                                                             that_pattern=that_pattern)

            if match_context is not None:
                return self.resolve_matched_template(client_context, match_context)

        return None

