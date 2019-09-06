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
from textblob import TextBlob


class PartsOfSpeechTagger(object):

    TAGS = {"CC": "Coordinating conjunction",
            "CD": "Cardinal number",
            "DT": "Determiner",
            "EX": "Existential there",
            "FW": "Foreign word",
            "IN": "Preposition or subordinating conjunction",
            "JJ": "Adjective",
            "JJR": "Adjective, comparative",
            "JJS": "Adjective, superlative",
            "LS": "List item marker",
            "MD": "Modal",
            "NN": "Noun, singular or mass",
            "NNS": "Noun, plural",
            "NNP": "Proper noun, singular",
            "NNPS": "Proper noun, plural",
            "PDT": "Predeterminer",
            "POS": "Possessive ending",
            "PRP": "Personal pronoun",
            "PRP$": "Possessive pronoun",
            "RB": "Adverb",
            "RBR": "Adverb, comparative",
            "RBS": "Adverb, superlative",
            "RP": "Particle",
            "SYM": "Symbol",
            "TO": "to",
            "UH": "Interjection",
            "VB": "Verb, base form",
            "VBD": "Verb, past tense",
            "VBG": "Verb, gerund or present participle",
            "VBN": "Verb, past participle",
            "VBP": "Verb, non - 3rd person singular present",
            "VBZ": "Verb, 3rd person singular present",
            "WDT": "Wh - determiner",
            "WP": "Wh - pronoun",
            "WP$": "Possessive wh - pronoun",
            "WRB": "Wh - adverb"
            }

    UNKNOWN = "Unknown"

    @staticmethod
    def tag_to_string(tag):
        if tag in PartsOfSpeechTagger.TAGS:
            return PartsOfSpeechTagger.TAGS[tag]
        else:
            return PartsOfSpeechTagger.UNKNOWN

    @staticmethod
    def tag_string(string):
        tagged = TextBlob(string)
        return tagged.tags
