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
from programy.clients.restful.config import RestConfiguration
from programy.utils.substitutions.substitues import Substitutions


class AlexaConfiguration(RestConfiguration):

    DEFAULT_LAUNCH_TEXT = "Hello and welcome"
    DEFAULT_CANCEL_TEXT = "OK, what else can I do?"
    DEFAULT_STOP_TEXT = "Good bye matey"
    DEFAULT_HELP_TEXT = "Ask me anything, I know loads"
    DEFAULT_ERROR_TEXT = "Oopsie there has been an error"
    DEFAULT_LEAVE_INTENT = "AMAZON.StopIntent, AMAZON.CancelIntent"

    def __init__(self):
        RestConfiguration.__init__(self, "alexa")
        self._launch_text = AlexaConfiguration.DEFAULT_LAUNCH_TEXT
        self._launch_srai = None

        self._stop_text = AlexaConfiguration.DEFAULT_STOP_TEXT
        self._stop_srai = None

        self._cancel_text = AlexaConfiguration.DEFAULT_CANCEL_TEXT
        self._cancel_srai = None

        self._help_text = AlexaConfiguration.DEFAULT_HELP_TEXT
        self._help_srai = None

        self._error_text = AlexaConfiguration.DEFAULT_ERROR_TEXT
        self._error_srai = None

        self._leave_intents = AlexaConfiguration.DEFAULT_LEAVE_INTENT

        self._intent_map_file = None

    @property
    def launch_text(self):
        return self._launch_text
    @property
    def launch_srai(self):
        return self._launch_srai

    @property
    def stop_text(self):
        return self._stop_text
    @property
    def stop_srai(self):
        return self._stop_srai

    @property
    def cancel_text(self):
        return self._cancel_text
    @property
    def cancel_srai(self):
        return self._cancel_srai

    @property
    def help_text(self):
        return self._help_text
    @property
    def help_srai(self):
        return self._help_srai

    @property
    def error_text(self):
        return self._error_text
    @property
    def error_srai(self):
        return self._error_srai

    @property
    def leave_intents(self):
        return self._leave_intents

    @property
    def intent_map_file(self):
        return self._intent_map_file

    def check_for_license_keys(self, license_keys):
        RestConfiguration.check_for_license_keys(self, license_keys)

    def load_configuration_section(self, configuration_file, alexa, bot_root, subs: Substitutions = None):
        if alexa is not None:
            self._launch_text = configuration_file.get_option(alexa, "launch_text", missing_value=AlexaConfiguration.DEFAULT_LAUNCH_TEXT, subs=subs)
            self._launch_srai = configuration_file.get_option(alexa, "launch_srai", missing_value=None, subs=subs)

            self._stop_text = configuration_file.get_option(alexa, "stop_text", missing_value=AlexaConfiguration.DEFAULT_STOP_TEXT, subs=subs)
            self._stop_srai = configuration_file.get_option(alexa, "stop_srai", missing_value=None, subs=subs)

            self._cancel_text = configuration_file.get_option(alexa, "cancel_text", missing_value=AlexaConfiguration.DEFAULT_CANCEL_TEXT, subs=subs)
            self._cancel_srai = configuration_file.get_option(alexa, "cancel_srai", missing_value=None, subs=subs)

            self._help_text = configuration_file.get_option(alexa, "help_text", missing_value=AlexaConfiguration.DEFAULT_HELP_TEXT, subs=subs)
            self._help_srai = configuration_file.get_option(alexa, "help_srai", missing_value=None, subs=subs)

            self._error_text = configuration_file.get_option(alexa, "error_text", missing_value=AlexaConfiguration.DEFAULT_ERROR_TEXT, subs=subs)
            self._error_srai = configuration_file.get_option(alexa, "error_srai", missing_value=None, subs=subs)

            self._intent_map_file = configuration_file.get_option(alexa, "intent_map_file", missing_value=None, subs=subs)
            leave_intents = configuration_file.get_option(alexa, "leave_intents",
                                                           missing_value=AlexaConfiguration.DEFAULT_LEAVE_INTENT, subs=subs)
            self._leave_intents = [x.strip() for x in leave_intents.split(",")]
            super(AlexaConfiguration, self).load_configuration_section(configuration_file, alexa, bot_root, subs=subs)

    def to_yaml(self, data, defaults=True):
        if defaults is True:
            data["launch_text"] = AlexaConfiguration.DEFAULT_LAUNCH_TEXT
            data["launch_srai"] = None

            data["stop_text"] = AlexaConfiguration.DEFAULT_STOP_TEXT
            data["stop_srai"] = None

            data["cancel_text"] = AlexaConfiguration.DEFAULT_CANCEL_TEXT
            data["cancel_srai"] = None

            data["help_text"] = AlexaConfiguration.DEFAULT_HELP_TEXT
            data["help_srai"] = None

            data["error_text"] = AlexaConfiguration.DEFAULT_ERROR_TEXT
            data["error_srai"] = None

            data["leave_intents"] = AlexaConfiguration.DEFAULT_LEAVE_INTENT
            data["intent_map_file"] = None
        else:
            data["launch_text"] = self._launch_text
            data["launch_srai"] = self._launch_srai

            data["stop_text"] = self._stop_text
            data["stop_srai"] = self._stop_srai

            data["cancel_text"] = self._cancel_text
            data["cancel_srai"] = self._cancel_srai

            data["help_text"] = self._help_text
            data["help_srai"] = self._help_srai

            data["error_text"] = self._error_text
            data["error_srai"] = self._error_srai
            data["leave_intents"] = self._leave_intents
            data["intent_map_file"] = self._intent_map_file

        super(AlexaConfiguration, self).to_yaml(data, defaults)
