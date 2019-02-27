"""
Copyright (c) 2016-2019 Keith Sterling http://www.keithsterling.com

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


class TranscriptAdminExtension(Extension):

    # execute() is the interface that is called from the <extension> tag in the AIML
    def execute(self, client_context, data):
        YLogger.debug(client_context, "Transcript Admin - [%s]", data)

        show_props = True if data == "PROPERTIES" else False

        transcript = ""

        if client_context.bot.has_conversation(client_context):
            conversation = client_context.bot.get_conversation(client_context)

            transcript += "Questions:<br /><ul>"
            for question in conversation.questions:
                transcript += "<li>%s - %s</li>"%(question.combine_sentences(), question.combine_answers())
            transcript += "</ul>"
            transcript += "<br />"

            if data == "PROPERTIES":
                transcript += "Properties:<br /><ul>"
                for name, value in conversation.properties.items():
                    transcript += "<li>%s = %s</li>"%(name, value)
                transcript += "</ul>"
                transcript += "<br />"

        else:
            transcript += "No conversation currently available"

        return transcript
