"""
Copyright (c) 2016-17 Keith Sterling http://www.keithsterling.com

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

import logging

from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters

from programy.clients.client import BotClient
from programy.config.sections.client.telegram_client import TelegramConfiguration


TELEGRAM_CLIENT = None


def start(bot, update):
    if TELEGRAM_CLIENT is None:
        raise Exception("Please initialise Telegram Client first")
    TELEGRAM_CLIENT.start(bot, update)


def message(bot, update):
    if TELEGRAM_CLIENT is None:
        raise Exception("Please initialise Telegram Client first")
    TELEGRAM_CLIENT.message(bot, update)


def unknown(bot, update):
    if TELEGRAM_CLIENT is None:
        raise Exception("Please initialise Telegram Client first")
    TELEGRAM_CLIENT.unknown(bot, update)


class TelegramBotClient(BotClient):

    _running = False

    def __init__(self, argument_parser=None):
        BotClient.__init__(self, "telegram", argument_parser)

    def set_environment(self):
        self.bot.brain.properties.add_property("env", 'telegram')

    def get_client_configuration(self):
        return TelegramConfiguration()

    @staticmethod
    def get_token(license_keys):
        return license_keys.get_key("TELEGRAM_TOKEN")

    @staticmethod
    def register_handlers(dispatcher):
        start_handler = CommandHandler('start', start)
        message_handler = MessageHandler(Filters.text, message)
        unknown_handler = MessageHandler(Filters.command, unknown)

        dispatcher.add_handler(start_handler)
        dispatcher.add_handler(message_handler)
        # Add unknown last
        dispatcher.add_handler(unknown_handler)

    @staticmethod
    def poll_and_process(updater):
        print("Telegram client running....")
        TelegramBotClient._running = True
        while TelegramBotClient._running is True:
            try:
                updater.start_polling()
            except KeyboardInterrupt as keye:
                print("Telegram client stopping....")
                TelegramBotClient._running = False
                updater.stop()
            except Exception as excep:
                logging.exception(excep)
                if logging.getLogger().isEnabledFor(logging.ERROR):
                    logging.error("Oops something bad happened !")

    def start(self, bot, update):
        try:
            initial_question = self.bot.get_initial_question(update.message.chat_id)
            processed_question = self.bot.brain.post_process_response(self.bot,
                                                                      update.message.chat_id,
                                                                      initial_question)
            bot.send_message(chat_id=update.message.chat_id, text=processed_question)
        except Exception as e:
            print(e)

    def message(self, bot, update):
        try:
            response = self.bot.ask_question(update.message.chat_id, update.message.text, responselogger=self)
            bot.send_message(chat_id=update.message.chat_id, text=response)
        except Exception as e:
            print(e)

    def get_unknown_command(self, clientid):
        if self.configuration.client_configuration.unknown_command_srai is None:
            unknown_response = self.configuration.client_configuration.unknown_command
        else:
            unknown_response = self.bot.ask_question(clientid,
                                                     self.configuration.client_configuration.unknown_command_srai,
                                                     responselogger=self)
            if unknown_response is None or unknown_response == "":
                unknown_response = self.configuration.client_configuration.unknown_command
        return unknown_response

    def unknown(self, bot, update):
        try:
            unknown_response = self.get_unknown_command(update.message.chat_id)
            bot.send_message(chat_id=update.message.chat_id, text=unknown_response)
        except Exception as e:
            print(e)

    def create_updater(self, telegram_token):
        return Updater(token=telegram_token)

    def run(self):
        if logging.getLogger().isEnabledFor(logging.DEBUG):
            logging.debug("Telegram Client is running....")

        telegram_token = self.get_token(self.bot.license_keys)

        updater = self.create_updater(telegram_token)

        self.register_handlers(updater.dispatcher)

        self.poll_and_process(updater)


if __name__ == '__main__':

    print("Loading Telegram client, please wait. See log output for progress...")
    TELEGRAM_CLIENT = TelegramBotClient()
    TELEGRAM_CLIENT.run()
