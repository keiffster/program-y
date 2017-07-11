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

from programy.config.sections.brain.file import BrainFileConfiguration

class BrainAIMLFileConfiguration(BrainFileConfiguration):

    def __init__(self, name="aiml"):
        BrainFileConfiguration.__init__(self, name, extension="aiml", directories=False)
        self._errors = None
        self._duplicates = None

    @property
    def errors(self):
        return self._errors

    @property
    def duplicates(self):
        return self._duplicates

    def load_config_section(self, file_config, brain_config, bot_root):
        files_config = file_config.get_option(brain_config, self.section_name)
        if files_config is not None:
            files = file_config.get_option(files_config, "files")
            if files is not None:
                self._files = self.sub_bot_root(files, bot_root)
                self._extension = file_config.get_option(files_config, "extension")
                self._directories = file_config.get_option(files_config, "directories")
            else:
                file = file_config.get_option(files_config, "file")
                if file is not None:
                    self._file = self.sub_bot_root(file, bot_root)

            errors = file_config.get_option(files_config, "errors", missing_value=None)
            if errors is not None:
                self._errors = self.sub_bot_root(errors, bot_root)
            duplicates = file_config.get_option(files_config, "duplicates", missing_value=None)
            if duplicates is not None:
                self._duplicates = self.sub_bot_root(duplicates, bot_root)

        else:
            logging.warning("'%s' section missing from bot config, using to defaults"%(self.section_name))

