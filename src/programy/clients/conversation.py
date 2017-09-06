import logging

from programy.clients.client import BotClient
from programy.config.sections.client.console import ConsoleConfiguration

import pyttsx3
import speech_recognition as sr


class ConversationBotClient(BotClient):

    def __init__(self, argument_parser=None):
        self.clientid = "Conversation"
        BotClient.__init__(self, argument_parser)

    def set_environment(self):
        self.bot.brain.properties.add_property("env", "Conversation")

    def get_client_configuration(self):
        return ConsoleConfiguration()

    def add_client_arguments(self, parser):
        parser.add_argument('--context', dest='context', action='store_true', help='displays additional conversation context')

    def parse_args(self, arguments, parsed_args):
        arguments.context = parsed_args.context

    def talkSpeech(self, response):
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        #engine.setProperty('voice', voices[1].id) for windows
        rate = engine.getProperty('rate')
        engine.setProperty('rate', rate-50)
        engine.say(response)
        engine.runAndWait()


    def run(self):
        record = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                # initialize bot starting message #
                if self.arguments.noloop is False:
                    logging.info("Entering conversation loop...")
                    running = True
                    self.display_response(self.bot.get_version_string)

                    # caliberate microphone
                    self.display_response('caliberating microphone...')
                    record.adjust_for_ambient_noise(source, 2)

                    # show and speak default response
                    default_response = self.bot.brain.post_process_response(self.bot, self.clientid, self.bot.initial_question)
                    self.display_response(default_response)
                    self.talkSpeech(default_response)
                    
                while running is True:
                    audio = record.listen(source)
                    try:
                        speechRecorded = record.recognize_sphinx(audio)
                        response = self.bot.ask_question(self.clientid, speechRecorded)
                        if response is None:
                            response = self.bot.ask_question(self.clientid, 'default aiml response')
                            self.talkSpeech(response)
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

    def get_question(self, input_func=input):
        ask = "%s "%self.bot.prompt
        return input_func(ask)

    def display_response(self, response, output_func=print):
        output_func(response)

if __name__ == '__main__':
    def run():
        print("Loading, please wait...")
        console_app = ConversationBotClient()
        console_app.run()
    run()
