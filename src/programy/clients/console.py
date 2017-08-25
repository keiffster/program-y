"""
Copyright (c) 2016-17 Keith Sterling http://www.keithsterling.com

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

from programy.clients.client import BotClient
from programy.config.sections.client.console import ConsoleConfiguration

import pyttsx3
import speech_recognition as sr

class ConsoleBotClient(BotClient):

    def __init__(self, argument_parser=None):
        BotClient.__init__(self, argument_parser)
        self.clientid = "Console"

    def set_environment(self):
        self.bot.brain.properties.add_property("env", "Console")

    def get_client_configuration(self):
        return ConsoleConfiguration()

    def talkSpeech(self, response):
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)
        rate = engine.getProperty('rate')
        engine.setProperty('rate', rate-50)
        engine.say(response)
        engine.runAndWait()

    def listen_speech_bot(self):
            record = sr.Recognizer()
            try:
                with sr.Microphone() as source:
                    # initialize bot starting message #
                    if self.arguments.noloop is False:
                        logging.info("Entering conversation loop...")
                        running = True
                        self.display_response(self.bot.get_version_string)
                        self.display_response(
                            self.bot.brain.post_process_response(self.bot, self.clientid, self.bot.initial_question))

                    while running is True:
                        audio = record.listen(source)
                        try:
                            speechRecorded = record.recognize_google(audio)
                            response = self.bot.ask_question(self.clientid, speechRecorded)
                            if response is None:
                                self.talkSpeech(self.bot.default_response)
                                self.log_unknown_response(speechRecorded)
                            else:
                                self.talkSpeech(response)
                                self.log_response(speechRecorded, response)
                                self.display_response(response)

                        except LookupError as e:
                            print(e)
                        except sr.UnknownValueError:
                            print("Google Speech Recognition could not understand audio")
                        except sr.RequestError as e:
                            print("Could not request results from Speech Recognition service; {0}".format(e))
                        except KeyboardInterrupt:
                            running = False
                            self.display_response(self.bot.exit_response)
                        except Exception as excep:
                            logging.exception(excep)
                            logging.error("Oops something bad happened !")
                            self.display_response(self.bot.default_response)
                            self.log_unknown_response(speechRecorded)

            # error occured when user has no microphone
            except OSError:
                print("\nNo default input devices available.")
                print("Switching to text type bot only.\n")
                self.text_type_bot()



    def text_type_bot(self):
        if self.arguments.noloop is False:
            logging.info("Entering conversation loop...")
            running = True
            self.display_response(self.bot.get_version_string)
            self.display_response(self.bot.brain.post_process_response(self.bot, self.clientid, self.bot.initial_question))
            while running is True:
                try:
                    question = self.get_question()
                    response = self.bot.ask_question(self.clientid, question)
                    if response is None:
                        self.display_response(self.bot.default_response)
                        self.log_unknown_response(question)
                    else:
                        self.display_response(response)
                        self.log_response(question, response)

                except KeyboardInterrupt:
                    running = False
                    self.display_response(self.bot.exit_response)
                except Exception as excep:
                    logging.exception(excep)
                    logging.error("Oops something bad happened !")
                    self.display_response(self.bot.default_response)
                    self.log_unknown_response(question)


    def run(self):
        if 'text' in self.arguments.bot_type:
            self.text_type_bot()
        elif 'talk' in self.arguments.bot_type:
            self.listen_speech_bot()
        else:
            print('No bot type specified')

    def get_question(self, input_func=input):
        ask = "%s "%self.bot.prompt
        return input_func(ask)

    def display_response(self, response, output_func=print):
        output_func(response)

if __name__ == '__main__':
    def run():
        print("Loading, please wait...")
        console_app = ConsoleBotClient()
        console_app.run()
    run()
