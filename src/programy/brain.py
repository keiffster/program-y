"""
Copyright (c) 2016 Keith Sterling

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import logging
import os.path
import xml.etree.ElementTree as ET

from programy.processors.processing import ProcessorLoader
from programy.config.brain import BrainConfiguration
from programy.mappings.denormal import DenormalCollection
from programy.mappings.gender import GenderCollection
from programy.mappings.maps import MapCollection
from programy.mappings.normal import NormalCollection
from programy.mappings.person import PersonCollection
from programy.mappings.predicates import PredicatesCollection
from programy.mappings.pronouns import PronounsCollection
from programy.mappings.properties import PropertiesCollection
from programy.mappings.sets import SetCollection
from programy.mappings.triples import TriplesCollection
from programy.parser.aiml_parser import AIMLParser
from programy.utils.services.service import ServiceFactory
from programy.utils.text.text import TextUtils

class Brain(object):

    def __init__(self, configuration: BrainConfiguration):
        self._configuration = configuration
        self._aiml_parser = AIMLParser(self)

        self._denormal_collection = DenormalCollection()
        self._normal_collection = NormalCollection()
        self._gender_collection = GenderCollection()
        self._person_collection = PersonCollection()
        self._person2_collection = PersonCollection()
        self._predicates_collection = PredicatesCollection()
        self._pronouns_collection = PronounsCollection()
        self._triples_collection = TriplesCollection()
        self._sets_collection = SetCollection()
        self._maps_collection = MapCollection()
        self._properties_collection = PropertiesCollection()

        self._preprocessors = ProcessorLoader()
        self._postprocessors = ProcessorLoader()

        self.load(self._configuration)

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
    def predicates(self):
        return self._predicates_collection

    @property
    def pronounds(self):
        return self._pronouns_collection

    @property
    def triples(self):
        return self._triples_collection

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
    def preprocessors(self):
        return self._preprocessors

    @property
    def postprocessors(self):
        return self._postprocessors

    def load(self, brain_configuration: BrainConfiguration):
        self._aiml_parser.load_aiml(brain_configuration)
        self.load_collections(brain_configuration)
        self.load_services(brain_configuration)

    def _load_denormals(self, brain_configuration):
        if brain_configuration.denormal is not None:
            total = self._denormal_collection.load_from_filename(brain_configuration.denormal)
            logging.info("Loaded a total of %d denormalisations", total)
        else:
            logging.warning("No configuration setting for denormal")

    def _load_normals(self, brain_configuration):
        if brain_configuration.normal is not None:
            total = self._normal_collection.load_from_filename(brain_configuration.normal)
            logging.info("Loaded a total of %d normalisations", total)
        else:
            logging.warning("No configuration setting for normal")

    def _load_genders(self, brain_configuration):
        if brain_configuration.gender is not None:
            total = self._gender_collection.load_from_filename(brain_configuration.gender)
            logging.info("Loaded a total of %d genderisations", total)
        else:
            logging.warning("No configuration setting for gender")

    def _load_persons(self, brain_configuration):
        if brain_configuration.person is not None:
            total = self._person_collection.load_from_filename(brain_configuration.person)
            logging.info("Loaded a total of %d persons", total)
        else:
            logging.warning("No configuration setting for person")

    def _load_person2s(self, brain_configuration):
        if brain_configuration.person2 is not None:
            total = self._person2_collection.load_from_filename(brain_configuration.person2)
            logging.info("Loaded a total of %d person2s", total)
        else:
            logging.warning("No configuration setting for person2")

    def _load_predicates(self, brain_configuration):
        if brain_configuration.predicates is not None:
            total = self._predicates_collection.load_from_filename(brain_configuration.predicates)
            logging.info("Loaded a total of %d predicates", total)
        else:
            logging.warning("No configuration setting for predicates")

    def _load_pronouns(self, brain_configuration):
        if brain_configuration.pronouns is not None:
            total = self._pronouns_collection.load_from_filename(brain_configuration.pronouns)
            logging.info("Loaded a total of %d pronouns", total)
        else:
            logging.warning("No configuration setting for pronouns")

    def _load_properties(self, brain_configuration):
        if brain_configuration.properties is not None:
            total = self._properties_collection.load_from_filename(brain_configuration.properties)
            logging.info("Loaded a total of %d properties", total)
        else:
            logging.warning("No configuration setting for properties")

    def _load_triples(self, brain_configuration):
        if brain_configuration.triples is not None:
            total = self._properties_collection.load_from_filename(brain_configuration.triples)
            logging.info("Loaded a total of %d triples", total)
        else:
            logging.warning("No configuration setting for triples")

    def _load_sets(self, brain_configuration):
        if brain_configuration.set_files is not None:
            total = self._sets_collection.load(brain_configuration.set_files)
            logging.info("Loaded a total of %d sets files", total)
        else:
            logging.warning("No configuration setting for set files")

    def _load_maps(self, brain_configuration):
        if brain_configuration.map_files is not None:
            total = self._maps_collection.load(brain_configuration.map_files)
            logging.info("Loaded a total of %d maps files", total)
        else:
            logging.warning("No configuration setting for map files")

    def _load_preprocessors(self, brain_configuration):
        if brain_configuration.preprocessors is not None:
            total = self._preprocessors.load(brain_configuration.preprocessors)
            logging.info("Loaded a total of %d pre processors", total)
        else:
            logging.warning("No configuration setting for pre processors")

    def _load_postprocessors(self, brain_configuration):
        if brain_configuration.postprocessors is not None:
            total = self._postprocessors.load(brain_configuration.postprocessors)
            logging.info("Loaded a total of %d post processors", total)
        else:
            logging.warning("No configuration setting for post processors")

    def load_collections(self, brain_configuration):
        self._load_denormals(brain_configuration)
        self._load_normals(brain_configuration)
        self._load_genders(brain_configuration)
        self._load_persons(brain_configuration)
        self._load_person2s(brain_configuration)
        self._load_predicates(brain_configuration)
        self._load_pronouns(brain_configuration)
        self._load_properties(brain_configuration)
        self._load_triples(brain_configuration)
        self._load_sets(brain_configuration)
        self._load_maps(brain_configuration)
        self._load_preprocessors(brain_configuration)
        self._load_postprocessors(brain_configuration)

    def load_services(self, brain_configuration):
        ServiceFactory.preload_services(brain_configuration.services)

    def pre_process_question(self, bot, clientid, question):
        return self.preprocessors.process(bot, clientid, question)

    def ask_question(self, bot, clientid, sentence) -> str:

        conversation = bot.get_conversation(clientid)

        topic_pattern = conversation.predicate("topic")
        if topic_pattern is None:
            logging.info("No Topic pattern default to [*]")
            topic_pattern = "*"
        else:
            logging.info("Topic pattern = [%s]", topic_pattern)

        try:
            that_question = conversation.nth_question(2)
            that_sentence = that_question.current_sentence()

            # If the last response was valid, i.e not none and not empty string, then use
            # that as the that_pattern, otherwise we default to '*' as pattern
            if that_sentence.response is not None and that_sentence.response != '':
                that_pattern = TextUtils.strip_all_punctuation(that_sentence.response)
                logging.info("That pattern = [%s]", that_pattern)
            else:
                logging.info("That pattern, no response, default to [*]")
                that_pattern = "*"

        except Exception:
            logging.info("No That pattern default to [*]")
            that_pattern = "*"

        match_context =  self._aiml_parser.match_sentence(bot, clientid,
                                                        sentence,
                                                        topic_pattern=topic_pattern,
                                                        that_pattern=that_pattern)

        if match_context is not None:
            template_node = match_context.template_node()
            logging.debug("AIML Parser evaluating template [%s]", template_node.to_string())
            #template_node.template.dump(tabs="", output_func=print)
            response = template_node.template.resolve(bot, clientid)
            return response

        return None

    def post_process_response(self, bot, clientid, response: str):
        return self.postprocessors.process(bot, clientid, response)

    def dump_tree(self):
        self._aiml_parser.pattern_parser.root.dump(tabs="")
