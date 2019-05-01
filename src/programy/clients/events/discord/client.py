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
from discord import Client as DiscordClient

from programy.clients.events.client import EventBotClient
from programy.clients.events.discord.config import DiscordConfiguration


class DiscordBotClient(EventBotClient):

    def __init__(self, discord_client: DiscordClient, argument_parser=None):
        self._discord_client = discord_client
        EventBotClient.__init__(self, "Discord", argument_parser)

    def get_client_configuration(self):
        return DiscordConfiguration()

    def get_license_keys(self):
        self._access_token = self.license_keys.get_key("DISCORD_TOKEN")

    def wait_and_answer(self):
        self._discord_client.run(self._access_token)

    def on_ready(self):
        YLogger.info(None, "Discord Client server now running")
        print("Discord Client server now running")
        return True

    def ask_question(self, client_context, question):
        return client_context.bot.ask_question(client_context, question, responselogger=self)

    def get_discord_user(self):
        return self._discord_client.user

    def on_message(self, message):
        print(message.author, self.get_discord_user())

        if message.author != self.get_discord_user():

            try:
                client_context = self.create_client_context(message.author.id)

                self._questions += 1
                return self.ask_question(client_context, message.content)

            except Exception as e:
                YLogger.exception(None, "Failed to ask question", e)

        return None


if __name__ == '__main__':

    print("Initiating Discord Client...")

    client = DiscordClient()
    discord = DiscordBotClient(client)

    @client.event
    async def on_ready():
        discord.on_ready()

    @client.event
    async def on_message(message):
        response = discord.on_message(message)
        if response:
            channel = message.channel
            if channel:
                await channel.send(response)

    discord.run()
