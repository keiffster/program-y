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

This is an example extension that allow you to call an external service to retreive the energy consumption data
of the customer. Currently contains no authentication
"""

from programy.utils.logging.ylogger import YLogger

from programy.extensions.base import Extension

class TranslateExtension(Extension):

    # execute() is the interface that is called from the <extension> tag in the AIML
    def execute(self, context, data):
        YLogger.debug(context, "Translate - Calling external service for with extra data [%s]", data)

        # TRANSLATE FROM EN TO FR <TEXT STRING>

        words = data.split(" ")
        if words:
            if len(words) > 5:
                if words[0] == "TRANSLATE":
                    if words[1] == "FROM":
                        from_lang = words[2]
                        if words[3] == "TO":

                            if context.bot.from_translator is not None:
                                to_lang = words[4]
                                text = " ".join(words[5:])

                                translated = context.bot.from_translator.translate(text, from_lang, to_lang)

                                return "TRANSLATED %s"%translated

                        else:
                            return "TRANSLATE DISABLED"

            elif len(words) == 2:
                if words[1] == 'ENABLED':

                    if context.bot.from_translator is not None:
                        return "TRANSLATE ENABLED"
                    else:
                        return "TRANSLATE DISABLED"

        return "TRANSLATE INVALID COMMAND"