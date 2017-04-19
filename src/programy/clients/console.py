import logging

from programy.clients.clients import BotClient

class ConsoleBotClient(BotClient):

    def __init__(self):
        BotClient.__init__(self)
        self.clientid = "Console"

    def set_environment(self):
        self.bot.brain.predicates.pairs.append(["env", "Console"])

    def run(self):
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
