"""
Copyright (c) 2016-2018 Keith Sterling http://www.keithsterling.com

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

import argparse
import os
import stat
import shutil
import datetime

from programy.admin.templates import *

class AdminTool(object):

    def execute(self, args):
        if args.create is not None:
            if args.create == 'app':
                self.create_app(args)
            elif args.create == 'script':
                self.create_script(args)
            else:
                raise Exception("Unknown create type")
        else:
            raise Exception("Unknown command")

    @staticmethod
    def create_sub_folder(root, folder):
        fullpath = root + os.sep + folder
        if os.path.exists(fullpath) is False:
            print("Creating sub: ", fullpath)
            os.mkdir(fullpath)

    @staticmethod
    def create_file_with_content(filepath, content, extra=None):
        print("Creating file:", filepath)
        with open(filepath, "w+") as file:
            file.write(content)
            if extra is not None:
                file.write("\n\n")
                file.write(extra)

    @staticmethod
    def make_executable(path):
        mode = os.stat(path).st_mode
        mode |= (mode & 0o444) >> 2  # copy R bits to X
        os.chmod(path, mode)

    @staticmethod
    def create_aiml_folder(location, defaults):
        AdminTool.create_sub_folder(location, "aiml")

        if defaults is True:
            aiml_file = location + os.sep + "aiml" + os.sep + "hello.aiml"
            AdminTool.create_file_with_content(aiml_file, AIML_TEMPLATE)

    @staticmethod
    def create_logging_file(location, app):
        config_file = location + os.sep + "logging.yaml"
        AdminTool.create_file_with_content(config_file, LOGGING_TEMPLATE)

    @staticmethod
    def create_initial_properties(location):
        props_file = location + os.sep + "config" + os.sep + "properties.txt"

        initiation_date = datetime.datetime.strftime(datetime.datetime.now(), "%B %d %Y")

        content = INITIAL_PROPERTIES % initiation_date

        AdminTool.create_file_with_content(props_file, content)

    @staticmethod
    def create_config_file(location, app):
        config_file = location + os.sep + "config.yaml"

        if app == "console":
            extra_config = None
        elif app == "webchat":
            extra_config = WEBCHAT_CONFIG
        elif app == "rest":
            extra_config = REST_CONFIG
        elif app == "xmpp":
            extra_config = XMPP_CONFIG
        elif app == "twitter":
            extra_config = TWITTER_CONFIG
        elif app == "socket":
            extra_config = SOCKET_CONFIG
        else:
            raise Exception ("Unknown app type [%s]"%app)

        AdminTool.create_file_with_content(config_file, CONFIG_TEMPLATE, extra=extra_config)

    @staticmethod
    def create_shell_script(location, app, platform, path=None):
        if platform == 'unix':
            if app == "console":
                script_file = "console.sh"
                script_contents = CONSOLE_SHELL_SCRIPT
            elif app == "webchat":
                script_file = "webchat.sh"
                script_contents = WEBCHAT_SHELL_SCRIPT
            elif app == "rest":
                script_file = "rest.sh"
                script_contents = REST_SHELL_SCRIPT
            elif app == "xmpp":
                script_file = "xmpp.sh"
                script_contents = XMPP_SHELL_SCRIPT
            elif app == "twitter":
                script_file = "twitter.sh"
                script_contents = TWITTER_SHELL_SCRIPT
            elif app == "socket":
                script_file = "socket.sh"
                script_contents = SOCKET_SHELL_SCRIPT
            else:
                raise Exception("Unknown app type [%s]" % app)

        elif platform == 'windows':
            if app == "console":
                script_file = "console.cmd"
                script_contents = CONSOLE_WINDOWS_CMD
            elif app == "webchat":
                script_file = "webchat.cmd"
                script_contents = WEBCHAT_WINDOWS_CMD
            elif app == "rest":
                script_file = "rest.cmd"
                script_contents = REST_WINDOWS_CMD
            elif app == "xmpp":
                script_file = "xmpp.cmd"
                script_contents = XMPP_WINDOWS_CMD
            elif app == "twitter":
                script_file = "twitter.cmd"
                script_contents = TWITTER_WINDOWS_CMD
            elif app == "socket":
                script_file = "socket.cmd"
                script_contents = SOCKET_WINDOWS_CMD
            else:
                raise Exception("Unknown app type [%s]" % app)

        else:
            raise Exception ("Unknown operation system [%s]"%platform)

        set_path = ""
        if path is not None:
            if platform == 'unix':
                set_path = "export PYTHONPATH=%s"%path
            elif platform == 'windows':
                set_path = "SET PYTHONPATH=%"%path
            else:
                raise Exception ("Unknown operation system [%s]"%platform)

        script_contents = script_contents % set_path

        script_file_path = location + os.sep + script_file
        AdminTool.create_file_with_content(script_file_path, script_contents)

        if platform == 'unix':
            print("Adding execute rights to :", script_file_path)
            AdminTool.make_executable(script_file_path)

        return script_file

    @staticmethod
    def create_app(args):
        print("Creating Template...")

        try:
            if os.path.exists(args.location) is True:
                if args.replace is True:
                    print("Empty/Removing existing directory")
                    shutil.rmtree(args.location)

            if os.path.exists(args.location) is False:
                print("Creating root:", args.location)
                os.mkdir(args.location)

            AdminTool.create_aiml_folder(args.location, args.default)
            AdminTool.create_sub_folder(args.location, "config")
            AdminTool.create_initial_properties(args.location)
            AdminTool.create_sub_folder(args.location, "conversations")
            AdminTool.create_sub_folder(args.location, "maps")
            AdminTool.create_sub_folder(args.location, "sets")
            AdminTool.create_sub_folder(args.location, "rdf")
            AdminTool.create_sub_folder(args.location, "spelling")
            AdminTool.create_sub_folder(args.location, "storage")
            AdminTool.create_config_file(args.location, args.app)
            AdminTool.create_logging_file(args.location, args.app)
            shell_script = AdminTool.create_shell_script(args.location, args.app,  args.os, args.path)

            print("\nA new Program-Y instance has been created in",args.location)
            print("You can start the bot by running the following:")
            print("\tcd", args.location)
            if args.os == 'unix':
                print("\t./%s"%shell_script)
            else:
                print("\t%s"%shell_script)

        except Exception as e:
            print("Failed to create new template:")
            print("Reason: ", e)

    @staticmethod
    def create_script(args):
        AdminTool.create_shell_script(args.location, args.app, args.os, args.path)

    @staticmethod
    def create_arguments():
        parser = argparse.ArgumentParser(description='Program-Y Flow Bot')

        parser.add_argument('-c', '--create', default="app", help="What to create", choices=['app', 'script'])
        parser.add_argument('-l', '--location', default=".", help='Destination for new structure')
        parser.add_argument('-r', '--replace', action='store_true', default=False, help='Replace current structure')
        parser.add_argument('-d', '--default', action='store_true', default=False, help="Create default files")
        parser.add_argument('-a', '--app', default="console", help="Type of app to create",
                            choices=['console', 'webchat', 'rest', 'xmpp', 'twitter', 'socket'])
        parser.add_argument('-o', '--os', default="unix", help="Type of os to support", choices=['unix', 'windows'])
        parser.add_argument('-p', '--path', help="Add PYTHONPATH to script")

        return parser

    @staticmethod
    def run():
        try:
            parser = AdminTool.create_arguments()
            app = AdminTool()
            app.execute(parser.parse_args())
        except Exception as e:
            parser.print_help()


if __name__ == '__main__':

    AdminTool.run()

