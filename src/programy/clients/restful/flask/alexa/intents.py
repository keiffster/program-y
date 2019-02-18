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
import json
import argparse
from abc import ABCMeta, abstractmethod


class Intent(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def generate(self):
        raise NotImplementedError()


class SystemIntent(Intent):
    __metaclass__ = ABCMeta

    def __init__(self, samples_file=None):
        self._samples_file = samples_file

    @abstractmethod
    def get_name(self):
        raise NotImplementedError()

    def _load_samples(self):
        samples = []

        if self._samples_file is not None:
            with open(self._samples_file, "r") as samples_file:
                for line in samples_file:
                    samples.append(line.strip())

        return samples

    def generate(self):
        intent = {}
        intent["name"] = self.get_name()
        intent["samples"] = self._load_samples()
        return intent


class CancelIntent(SystemIntent):

    def __init__(self, samples_file=None):
        SystemIntent.__init__(self, samples_file)
        
    def get_name(self):
        return "AMAZON.CancelIntent"


class HelpIntent(SystemIntent):

    def __init__(self, samples_file=None):
        SystemIntent.__init__(self, samples_file)

    def get_name(self):
        return "AMAZON.HelpIntent"


class StopIntent(SystemIntent):

    def __init__(self, samples_file=None):
        SystemIntent.__init__(self, samples_file)

    def get_name(self):
        return "AMAZON.StopIntent"


class QueryIntent(object):

    def __init__(self, query):
        self._query = query

    def create_name(self):
        words = self._query.split(" ")
        return "Ask" + "".join([word[0].upper() + word[1:] for word in words])

    def generate(self):
        slot = {}
        slot['name'] = self.create_name()
        slot['slots'] = [{"name": "text", "type": "AMAZON.SearchQuery"}]
        slot['samples'] = ["%s {text}" % self._query]
        return slot


class LanguageModel(object):

    def __init__(self, invocationName, intents):

        assert (isinstance(invocationName, str))
        assert (isinstance(intents, list))

        self._invocationName = invocationName
        self._intents = intents

    def generate(self):
        model = {}
        model["invocationName"] = self._invocationName
        model["intents"] = []
        for intent in self._intents:
            model["intents"].append(intent.generate())
        return model


class InteractionModel(object):

    def __init__(self, languageModel):

        assert (isinstance(languageModel, LanguageModel))

        self._languageModel = languageModel

    def generate(self):
        model = {}
        model["languageModel"] = self._languageModel.generate()
        return model


class Intents(object):

    def __init__(self, interactionModel):

        assert (isinstance(interactionModel, InteractionModel))

        self._interactionModel = interactionModel

    def generate(self):
        intents = {}
        intents["interactionModel"] = self._interactionModel.generate()
        return intents


class IntentGenerator(object):

    def __init__(self, invocation_name, system_intents, intents_word_file, intents_json_file, intents_mapping_file):
        self._invocation_name = invocation_name
        self._system_intents = system_intents
        self._intents_word_file = intents_word_file
        self._intents_json_file = intents_json_file
        self._intents_mapping_file = intents_mapping_file

    def generate(self):
        intents = self._system_intents[:]

        intent_mappings = {}
        with open(self._intents_word_file, "r") as intent_words:
            for line in intent_words:
                word = line.strip().lower()
                intent = QueryIntent(word)
                intents.append(intent)
                intent_mappings[intent.create_name()] = word

        intents = Intents(InteractionModel(LanguageModel(self._invocation_name, intents)))

        with open(self._intents_json_file, "w+") as intent_json:
            intent_json.write(json.dumps(intents.generate(), indent=4, sort_keys=True))

        with open(self._intents_mapping_file, "w+") as intent_json:
            intent_json.write(json.dumps(intent_mappings, indent=4, sort_keys=True))


if __name__ == '__main__':

    print("Generating intents...")

    parser = argparse.ArgumentParser(description='Program-Y Alexa Client Intent Generatorr')
    try:

        parser.add_argument('-in', '--invocation_name', required=True, help="Invocation Name")
        parser.add_argument('-ci', '--cancel_intent', action='store_true', help="Include Cancel Intent")
        parser.add_argument('-cif', '--cancel_intent_file', help="Cancel Intents file")
        parser.add_argument('-hi', '--help_intent', action='store_true', help="Include Help Intent")
        parser.add_argument('-hif', '--help_intent_file',help="Help Intent file")
        parser.add_argument('-si', '--stop_intent', action='store_true', help="Include Stop Intent")
        parser.add_argument('-sif', '--stop_intent_file', help="Stop Intent file")
        parser.add_argument('-if', '--intents_file', required=True, help="Intents filename")
        parser.add_argument('-ij', '--intents_json', required=True, help="Intents JSON filename")
        parser.add_argument('-im', '--intents_maps', required=True, help="Intents Map filename")

        args = parser.parse_args()

        system_intents = []
        if args.cancel_intent is True:
            system_intents.append(CancelIntent(args.cancel_intent_file))
        if args.stop_intent is True:
            system_intents.append(StopIntent(args.stop_intent_file))
        if args.help_intent is True:
            system_intents.append(HelpIntent(args.help_intent_file))

        print("\nReading [%s]"%args.intents_file)

        generator = IntentGenerator(args.invocation_name, system_intents, args.intents_file, args.intents_json, args.intents_maps)
        generator.generate()

        print("\nGenerated [%s]"%args.intents_json)
        print("Generated [%s]"%args.intents_maps)


    except Exception as e:
        print(e)
        parser.print_help()
