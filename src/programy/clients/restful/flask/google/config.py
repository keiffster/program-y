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


class GoogleConfiguration(RestConfiguration):

    DEFAULT_LAUNCH_TEXT = "Hello and welcome"
    DEFAULT_QUIT_TEXT = "Good bye matey"
    DEFAULT_HELP_TEXT = "Ask me anything, I know loads"
    DEFAULT_ERROR_TEXT = "Oopsie there has been an error"

    def __init__(self):
        RestConfiguration.__init__(self, "google")     
        self._launch_text = GoogleConfiguration.DEFAULT_LAUNCH_TEXT
        self._launch_srai = None

        self._quit_text = GoogleConfiguration.DEFAULT_QUIT_TEXT
        self._quit_srai = None

        self._help_text = GoogleConfiguration.DEFAULT_HELP_TEXT
        self._help_srai = None

        self._error_text = GoogleConfiguration.DEFAULT_ERROR_TEXT
        self._error_srai = None

    @property
    def launch_text(self):
        return self._launch_text
    @property
    def launch_srai(self):
        return self._launch_srai

    @property
    def quit_text(self):
        return self._quit_text
    @property
    def quit_srai(self):
        return self._quit_srai

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

    def check_for_license_keys(self, license_keys):
        RestConfiguration.check_for_license_keys(self, license_keys)

    def load_configuration_section(self, configuration_file, google, bot_root, subs: Substitutions = None):
        if google is not None:
            self._launch_text = configuration_file.get_option(google, "launch_text", missing_value=GoogleConfiguration.DEFAULT_LAUNCH_TEXT)
            self._launch_srai = configuration_file.get_option(google, "launch_srai", missing_value=None)

            self._quit_text = configuration_file.get_option(google, "quit_text", missing_value=GoogleConfiguration.DEFAULT_QUIT_TEXT)
            self._quit_srai = configuration_file.get_option(google, "quit_srai", missing_value=None)

            self._help_text = configuration_file.get_option(google, "help_text", missing_value=GoogleConfiguration.DEFAULT_HELP_TEXT)
            self._help_srai = configuration_file.get_option(google, "help_srai", missing_value=None)

            self._error_text = configuration_file.get_option(google, "error_text", missing_value=GoogleConfiguration.DEFAULT_ERROR_TEXT)
            self._error_srai = configuration_file.get_option(google, "error_srai", missing_value=None)

            super(GoogleConfiguration, self).load_configuration_section(configuration_file, google, bot_root, subs=subs)

    def to_yaml(self, data, defaults=True):
        if defaults is True:
            data["launch_text"] = GoogleConfiguration.DEFAULT_LAUNCH_TEXT
            data["launch_srai"] = None

            data["quit_text"] = GoogleConfiguration.DEFAULT_QUIT_TEXT
            data["quit_srai"] = None

            data["help_text"] = GoogleConfiguration.DEFAULT_HELP_TEXT
            data["help_srai"] = None

            data["error_text"] = GoogleConfiguration.DEFAULT_ERROR_TEXT
            data["error_srai"] = None

        else:
            data["launch_text"] = self._launch_text
            data["launch_srai"] = self._launch_srai

            data["quit_text"] = self._quit_text
            data["quit_srai"] = self._quit_srai

            data["help_text"] = self._help_text
            data["help_srai"] = self._help_srai

            data["error_text"] = self._error_text
            data["error_srai"] = self._error_srai

        super(GoogleConfiguration, self).to_yaml(data, defaults)
