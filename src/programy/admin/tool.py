"""
Copyright (c) 2016-2020 Keith Sterling http://www.keithsterling.com

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
import os
import sys
import zipfile
import shutil
import wget
import nltk
import textblob.download_corpora as download_corpora
from programy.utils.console.console import outputLog

bots = {
    'alice2-y': "https://github.com/keiffster/alice2-y/archive/master.zip",
    'professor-y': "https://github.com/keiffster/professor-y/archive/master.zip",
    'rosie-y': "https://github.com/keiffster/rosie-y/archive/master.zip",
    'talk-y': "https://github.com/keiffster/talk-y/archive/master.zip",
    'y-bot': "https://github.com/keiffster/y-bot/archive/master.zip",
    'servusai-y': "https://github.com/keiffster/servusai-y/archive/master.zip",
    'template-y': "https://github.com/keiffster/template-y/archive/master.zip",
    'traintimes-y': "https://github.com/keiffster/traintimes-y/archive/master.zip"
}


class AdminTool:

    @staticmethod
    def recursive_copy(src, dest):
        """
        Copy each file from src dir to dest dir, including sub-directories.
        """
        for item in os.listdir(src):
            file_path = os.path.join(src, item)

            # if item is a file, copy it
            if os.path.isfile(file_path):
                shutil.copy(file_path, dest)

            # else if item is a folder, recurse
            else: # os.path.isdir(file_path):
                new_dest = os.path.join(dest, item)
                os.mkdir(new_dest)
                AdminTool.recursive_copy(file_path, new_dest)

    @staticmethod
    def delete_folder_contents(folder):
        shutil.rmtree(folder)

    @staticmethod
    def make_all_executable(path):
        for item in os.listdir(path):
            file_path = os.path.join(path, item)
            AdminTool.make_executable(file_path)

    @staticmethod
    def make_executable(path):
        mode = os.stat(path).st_mode
        mode |= (mode & 0o444) >> 2  # copy R bits to X
        os.chmod(path, mode)

    def list_bots(self):
        self.display("Available bots are:\n")
        for bot in bots:
            self.display("\t%s" % bot)
        if os.name == 'posix':
            self.display("\n\tTo download use 'python3 -m programy.admin.tool download <bot-name>'")
        else:                                                                                           # pragma: no cover
            self.display("\n\tTo download use 'python -m programy.admin.tool download <bot-name>'")     # pragma: no cover

        self.display("\nAdditional components are:\n")
        self.display("\ttextblob")
        if os.name == 'posix':
            self.display("\n\tTo install use 'python3 -m programy.admin.tool install <component>'")
        else:                                                                                           # pragma: no cover
            self.display("\n\tTo install use 'python -m programy.admin.tool install <component>'")      # pragma: no cover
        self.display("")

    def wget_download(self, url):
        return wget.download(url, bar=wget.bar_thermometer)     # pragma: no cover

    def download_bot(self, bot_name):
        url = bots[bot_name]
        self.display("Downloading [%s] from [%s]" % (bot_name, url))
        filename = self.wget_download(url)
        self.display("\nDownload complete")
        return filename

    @staticmethod
    def extract_bot(filename, path=None, remove_after=True):
        zip_ref = zipfile.ZipFile(filename, 'r')
        zip_ref.extractall(path=path)
        zip_ref.close()
        if remove_after is True:
            os.remove(filename)

    @staticmethod
    def zip_dir_name_from_filename(filename):
        return filename.split(".")[0]

    def download_and_make_active(self, bot_name):
        filename = self.download_bot(bot_name)                                              # pragma: no cover
        AdminTool.extract_bot(filename)                                                     # pragma: no cover
        master_dir = AdminTool.zip_dir_name_from_filename(filename)                         # pragma: no cover
        AdminTool.recursive_copy(master_dir, ".")                                           # pragma: no cover
        if os.name == 'posix':                                                              # pragma: no cover
            AdminTool.make_all_executable("." + os.sep + "scripts" + os.sep + "xnix")       # pragma: no cover
        shutil.rmtree(master_dir)                                                           # pragma: no cover

    def install_bot(self, words):

        if len(words) < 2:
            raise Exception("Missing bot name from download command")
        bot_name = words[1]

        if bot_name not in bots:
            raise Exception("Unknown bot [%s]" % bot_name)

        self.download_and_make_active(bot_name)

        self.show_execute_help(bot_name)

    def install_textblob(self):
        nltk.download('punkt')              # pragma: no cover
        nltk.download('stopwords')          # pragma: no cover
        download_corpora.download_all()     # pragma: no cover

    def install_additional(self, words):

        if len(words) < 2:
            raise Exception("Missing additional element from install command")
        additional = words[1]

        if additional == 'textblob':
            self.display("Installing additional components for %s" % additional)
            self.install_textblob()
        else:
            raise Exception("Missing additional component from install command ['textblob']")

    def show_execute_help(self, bot_name):
        self.display("\nTo run %s bot in console mode, use the following commands" % bot_name)
        if os.name == 'posix':
            self.display("\n\tcd scripts/xnix")
            self.display("\t./%s.sh" % bot_name)
        else:                                           # pragma: no cover
            self.display("\n\tcd scripts\\windows")     # pragma: no cover
            self.display("\t%s.cmd" % bot_name)         # pragma: no cover

    def show_help(self):
        self.display("Available commands are:\n")
        self.display("\thelp")
        self.display("\tlist")
        self.display("\tdownload <bot-name>")
        self.display("\tinstall <component>")
        self.display("")

    def run(self, words):
        try:
            num_words = len(words)
            if num_words > 0:
                primary = words[0]
                if primary == 'list':
                    self.list_bots()
                elif primary == 'download':
                    self.install_bot(words)
                elif primary == 'install':
                    self.install_additional(words)
                elif primary == 'help':
                    self.show_help()
                else:
                    raise Exception("Unknown primary command [%s]" % words[0])
            else:
                self.show_help()

        except Exception as excep:
            self.display(str(excep))
            self.show_help()

    def display(self, text):
        outputLog(self, text)   # pragma: no cover


if __name__ == '__main__':      # pragma: no cover
    tool = AdminTool()          # pragma: no cover
    tool.run(sys.argv[1:])      # pragma: no cover
