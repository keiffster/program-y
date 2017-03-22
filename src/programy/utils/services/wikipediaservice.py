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
import wikipedia
import logging

from programy.utils.services.service import Service
from programy.config.brain import BrainServiceConfiguration

class WikipediaAPI(object):

    @staticmethod
    def summary(title, sentences=0, chars=0, auto_suggest=True, redirect=True):
        return wikipedia.summary(title, sentences, chars, auto_suggest, redirect)

class WikipediaService(Service):

    def __init__(self, config):
        Service.__init__(self, config)

    def ask_question(self, bot, clientid: str, question: str):
        try:
            search = WikipediaAPI.summary(question, sentences=1)
            return search
        except wikipedia.exceptions.DisambiguationError:
            logging.error("Wikipedia search is ambiguous for question [%s]", question)
            return ""
        except wikipedia.exceptions.PageError:
            logging.error("No page on Wikipedia for question [%s]", question)
            return ""
        except Exception:
            logging.error("General error querying Wikipedia for question [%s]", question)
            return ""


# Integration Test
if __name__ == '__main__':

    def run():
        servce_config = BrainServiceConfiguration("WIKIPEDIA")

        service = WikipediaService(servce_config)
        service_response = service.ask_question(None, "testid", "keith sterling")
        print(service_response)

    run()
