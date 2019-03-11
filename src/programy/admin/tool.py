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
import os
import sys
import zipfile
import wget
import shutil
import nltk
import textblob.download_corpora as download_corpora

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


class AdminTool(object):

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
            elif os.path.isdir(file_path):
                new_dest = os.path.join(dest, item)
                os.mkdir(new_dest)
                AdminTool.recursive_copy(file_path, new_dest)

    @staticmethod
    def delete_folder_contents(folder):
        for root, dirs, files in os.walk(folder):
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))

    @staticmethod
    def create_sub_folder(root, folder):
        fullpath = root + os.sep + folder
        if os.path.exists(fullpath) is False:
            print("Creating sub folder: [%s]" % fullpath)
            os.mkdir(fullpath)

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

    @staticmethod
    def list_bots(display=print):
        display("Available bots are:\n")
        for bot in bots:
            display("\t%s" % bot)
        if os.name == 'posix':
            display("\n\tTo download use 'python3 -m programy.admin.tool download <bot-name>'")
        else:
            display("\n\tTo download use 'python -m programy.admin.tool download <bot-name>'")

        display("\nAdditional components are:\n")
        display("\ttextblob")
        if os.name == 'posix':
            display("\n\tTo install use 'python3 -m programy.admin.tool install <component>'")
        else:
            display("\n\tTo install use 'python -m programy.admin.tool install <component>'")
        display()

    @staticmethod
    def download_bot(bot_name, display=print):
        url = bots[bot_name]
        display("Downloading [%s] from [%s]" % (bot_name, url))
        filename = wget.download(url, bar=wget.bar_thermometer)
        display("\nDownload complete")
        return filename

    @staticmethod
    def extract_bot(filename, remove_after=True):
        zip_ref = zipfile.ZipFile(filename, 'r')
        zip_ref.extractall()
        zip_ref.close()
        if remove_after is True:
            os.remove(filename)

    @staticmethod
    def zip_dir_name_from_filename(filename):
        return filename.split(".")[0]

    @staticmethod
    def install_bot(words, display=print):

        if len(words) < 2:
            raise Exception("Missing bot name from download command")
        bot_name = words[1]

        if bot_name not in bots:
            raise Exception("Unknown bot [%s]" % bot_name)

        filename = AdminTool.download_bot(bot_name, display)

        AdminTool.extract_bot(filename)

        master_dir = AdminTool.zip_dir_name_from_filename(filename)

        AdminTool.recursive_copy(master_dir, ".")

        if os.name == 'posix':
            AdminTool.make_all_executable("." + os.sep + "scripts" + os.sep + "xnix")

        shutil.rmtree(master_dir)

        AdminTool.show_execute_help(bot_name, display)

    @staticmethod
    def install_additional(words, display=print):

        if len(words) < 2:
            raise Exception("Missing additional element from install command")
        additional = words[1]

        if additional=='textblob':
            display("Installing additional components for %s"%additional)

            nltk.download('punkt')

            download_corpora.download_all()
        else:
            raise Exception("Missing additional component from install command ['textblob']")

    @staticmethod
    def show_execute_help(bot_name, display=print):
        display("\nTo run %s bot in console mode, use the following commands" % bot_name)
        if os.name == 'posix':
            display("\n\tcd scripts/xnix")
            display("\t./%s.sh" % bot_name)
        else:
            display("\n\tcd scripts\\windows")
            display("\t%s.cmd" % bot_name)

    @staticmethod
    def show_help(words, display=print):
        display ("Available commands are:\n")
        display("\thelp")
        display("\tlist")
        display("\tdownload <bot-name>")
        display("\tinstall <component>")
        display("")

    def run(self, words, display=print):
        try:
            num_words = len(words)
            if num_words > 0:
                primary = words[0]
                if primary == 'list':
                    AdminTool.list_bots(display)
                elif primary == 'download':
                    AdminTool.install_bot(words, display)
                elif primary == 'install':
                    AdminTool.install_additional(words, display)
                elif primary == 'help':
                    AdminTool.show_help(words, display)
                else:
                    raise Exception("Unknown primary command [%s]" % words[0])
            else:
                AdminTool.show_help(words, display)

        except Exception as e:
            display(str(e))
            AdminTool.show_help(words, display)


if __name__ == '__main__':

    tool = AdminTool()
    tool.run(sys.argv[1:])
