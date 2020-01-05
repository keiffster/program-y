"""
Copyright (c) 2016-2020 Keith Sterling http://www.keithsterling.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions
of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""
from programy.utils.logging.ylogger import YLogger
from programy.extensions.base import Extension


class ClientAdminExtension(Extension):

    def _commands(self):
        return "LIST BOTS, LIST BRAINS, DUMP BRAIN"

    def _list(self, commands, client_context):
        if len(commands) > 1:

            if commands[1] == 'BOTS':
                ids = client_context.client.bot_factory.botids()
                return ", ".join(ids)

            elif commands[1] == 'BRAINS':

                if len(commands) > 2:
                    botid = commands[2]
                    bot = client_context.client.bot_factory.bot(botid)
                    if bot:
                        ids = bot.brain_factory.brainids()
                        return ", ".join(ids)

                    else:
                        return "Invalid Bot Id [%s]" % botid

        return "Invalid LIST command, BOTS or BRAINS only"

    def _dump(self, commands, client_context):
        if commands[1] == 'BRAIN':

            if len(commands) == 4:
                botid = commands[2]
                bot = client_context.client.bot_factory.bot(botid)
                if bot is not None:
                    brainid = commands[3]
                    brain = bot.brain_factory.brain(brainid)
                    if brain is not None:
                        brain.dump_brain_tree(client_context)
                        return "Brain dumped, see config for location"

                    else:
                        return "Invalid Brain Id [%s]" % brainid

                else:
                    return "Invalid Bot Id [%s]" % botid

            else:
                return "Incomplete DUMP BRAIN Command"

        else:
            return "Invalid DUMP command, BRAIN only"

    # execute() is the interface that is called from the <extension> tag in the AIML
    def execute(self, client_context, data):
        YLogger.debug(client_context, "Client Admin - [%s]", data)

        try:
            commands = data.split()

            if commands[0] == 'COMMANDS':
                return self._commands()

            elif commands[0] == 'LIST':
                return self._list(commands, client_context)

            elif commands[0] == 'DUMP':
                return self._dump(commands, client_context)

            else:
                return "Invalid Admin Command, LIST or DUMP only"

        except Exception as e:
            YLogger.exception(client_context, "Failed to execute client admin extension", e)

        return "Client Admin Error"
