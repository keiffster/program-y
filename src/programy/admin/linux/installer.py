import argparse
import os
import sys
import zipfile
import shutil
import wget

ybot = "https://github.com/keiffster/y-bot/archive/master.zip"
servusai = "https://github.com/keiffster/servusai-y/archive/master.zip"

programy_root = "/opt/program-y"
servusai_root = "./Servusai"
ybot_root = "./Y-bot"

systemd_root = "/etc/systemd"  # /system

webserver = "nginx"
webserver_root = "/etc/nginx"      # /site-enabled

clients = [
    {"name": "Alexa", "src": "./alexa"},
    {"name": "Console", "src": "./console"},
    {"name": "Discord", "src": "./discord"},
    {"name": "Facebook", "src": "./facebook"},
    {"name": "Google", "src": "./google"},
    {"name": "Kik", "src": "./kik"},
    {"name": "Line", "src": "./line"},
    {"name": "Microsoft", "src": "./microsoft"},
    {"name": "REST", "src": "./rest"},
    {"name": "Slack", "src": "./slack"},
    {"name": "TCP Socket", "src": "./socket"},
    {"name": "Telegram", "src": "./telegram"},
    {"name": "Twillio", "src": "./twillio"},
    {"name": "Twitter", "src": "./twitter"},
    {"name": "Viber", "src": "./viber"},
    {"name": "Web", "src": "./web", "remove_default": True},
    {"name": "XMPP", "src": "./xmpp"}
]


class Installer:

    def __init__(self):
        self._args = None
        self._name = "y-bot"

        self._programy_root = programy_root

        self._ybot = False
        self._ybot_root = ybot_root

        self._servusai = False
        self._servusai_root = servusai_root

        self._systemd_root = systemd_root

        self._webserver = webserver
        self._webserver_root = webserver_root

        self._clients = False
        self._client = None

        self._debug = False

    def parse_arguments(self):
        parser = argparse.ArgumentParser(description='Program-u multi client installer')

        parser.add_argument('--name', dest='name', help='Name of your multi client bot')

        parser.add_argument('--programyroot', dest='programyroot', help='Programy install folder')

        parser.add_argument('--ybot', dest='ybot', action='store_true', help='Install y-bot core')
        parser.add_argument('--ybotroot', dest='ybotroot', help='Y-bot install folder')

        parser.add_argument('--servusai', action='store_true', help='Install servusai clients')
        parser.add_argument('--servusairoot', dest='servusairoot', help='Servusai install folder')

        parser.add_argument('--systemdroot', dest='systemdroot', help='Systemd root directory')

        parser.add_argument('--webserver', dest='webserver', help='Which web server to install for [nginx]')
        parser.add_argument('--webserverroot', dest='webserverroot', help='Web server root folder')

        parser.add_argument('--list', dest='listclients', action='store_true', help='List all clients')
        parser.add_argument('--clients', dest='clients', action='store_true', help='Loop through install of clients')
        parser.add_argument('--client', dest='client', help='Install specific client')

        parser.add_argument('--debug', dest='debug', action='store_true', help='Do not actually execute commands')

        self._args = parser.parse_args()

        self._check_args()

        self._arg_defaults()

    def _check_args(self):
        if self._args.clients is True and self._args.client is not None:
            raise Exception("Both --clients and --client are not allowed!")

        if self._args.clients is True or self._args.client is not None:
            if self._args.webserver != "nginx":
                raise Exception("Only Nginx suppported at this time!")

    def _arg_defaults(self):
        if self._args.programyroot is not None:
            self._programy_root = self._args.programyroot

        self._servusai = self._args.servusai

        if self._args.servusairoot is not None:
            self._servusai_root = self._args.servusairoot

        self._ybot = self._args.ybot

        if self._args.ybotroot is not None:
            self._ybot_root = self._args.ybotroot

        if self._args.systemdroot is not None:
            self._systemd_root = self._args.systemdroot

        if self._args.webserver is not None:
            self._webserver = self._args.webserver

        if self._args.webserverroot is not None:
            self._webserver_root = self._args.webserverroot

        self._clients = self._args.clients

        if self._args.client is not None:
            self._client = self._args.client

        self._debug = self._args.debug

        self._print_settings()

    def _print_settings(self):
        print("Settings:")
        print("\tName:", self._name)

        print("\tProgramy Root:", self._programy_root)

        print("\tY-Bot?", self._ybot)
        print("\tY-Bot Root:", self._ybot_root)

        print("\tServusai?", self._servusai)
        print("\tServusai Root:", self._servusai_root)

        print("\tSystemd Root:", self._systemd_root)

        print("\tWeb Server:", self._webserver)
        print("\tWeb Server Root:", self._webserver_root)

        print("\tClients?", self._clients)
        if self._client is not None:
            print("\tClient:", self._client)

    def _wget_download(self, url):
        return wget.download(url, bar=wget.bar_thermometer)     # pragma: no cover

    def _download_bot(self, name, url):
        print("Downloading [%s] from [%s]" % (name, url))
        filename = self._wget_download(url)

        self._extract_bot(filename)                                                      # pragma: no cover

        master_dir = self._zip_dir_name_from_filename(filename)                          # pragma: no cover

        os.mkdir(name)

        self._recursive_copy(master_dir, name)                                           # pragma: no cover

        if os.name == 'posix':                                                           # pragma: no cover
            self._make_all_executable(name + os.sep + "scripts" + os.sep + "xnix")       # pragma: no cover

        shutil.rmtree(master_dir)                                                        # pragma: no cover

    def _extract_bot(self, filename, path=None, remove_after=True):
        zip_ref = zipfile.ZipFile(filename, 'r')
        zip_ref.extractall(path=path)
        zip_ref.close()
        if remove_after is True:
            os.remove(filename)

    def _zip_dir_name_from_filename(self, filename):
        return filename.split(".")[0]

    def _recursive_copy(self, src, dest):
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
                self._recursive_copy(file_path, new_dest)

    def _make_all_executable(self, path):
        for item in os.listdir(path):
            file_path = os.path.join(path, item)
            self._make_executable(file_path)

    def _make_executable(self, path):
        mode = os.stat(path).st_mode
        mode |= (mode & 0o444) >> 2  # copy R bits to X
        os.chmod(path, mode)

    def install(self):
        if self._args.ybot is True:
            self._install_ybot()

        if self._args.servusai is True:
            self._install_servusai()

        if self._args.listclients is True:
            self._list_clients()

        if self._args.clients is True:
            self._install_clients()

        if self._args.client is not None:
            self._install_client(self._args.client)

    def _list_clients(self):
        print("\nAvailable Clients:")
        for client in clients:
            print("\t", client['name'])
        print()

    def _install_ybot(self):
        print("\nInstall Y-Bot Core")
        self._download_bot("Y-Bot", ybot)

    def _install_servusai(self):
        print("\nInstall Servusai")
        self._download_bot("Servusai", servusai)

    def _install_clients(self):
        print("\nInstalling Clients")
        for client in clients:
            self._install_client(client['name'])

    def _install_client(self, name):
        for client in clients:
            if name.upper() == client['name'].upper():
                print("\nInstalling Client", name)
                self._do_client_install(client)
                return

        raise Exception("Unknown client", name)

    def _do_client_install(self, client):

        self._install_systemd_service(client)

        self._install_web_service(client)

    def _install_systemd_service(self, client):
        print("%s systemd service install" % client['name'])

        service_file = "servusai-%s.service" % client["name"].lower()

        service_file_src = self._servusai_root + "/Servusai/%s/config/xnix/%s" % (client["name"].lower(), service_file)
        service_file_dest = self._systemd_root + "/system/%s" % service_file

        self._execute("cp %s %s" %(service_file_src, service_file_dest))

        self._execute("systemctl daemon-reload")

        self._execute("systemctl enable %s" % service_file)
        self._execute("systemctl start %s" % service_file)
        self._execute("systemctl status %s" % service_file)
        print()

    def _install_web_service(self, client):
        print("%s web service install" % client['name'])

        if client.get("remove_default", False) is True:
            self._execute("rm /etc/nginx/sites-enabled/default")

        web_site_src = self._servusai_root + "/Servusai/%s/config/xnix/%s.site" % (client["name"].lower(), client["name"].lower())
        web_site_dest = self._webserver_root + "/sites-enabled"

        self._execute("cp %s %s" % (web_site_src, web_site_dest))
        self._execute("service nginx restart")
        print()

    def _execute(self, command):
        try:
            if self._debug is False:
                stream = os.popen(command)
                output = stream.read()
                stream.close()
                print(command, "->", output)

            else:
                print(command)

            return True

        except Exception as error:
            print(error)

        return False


if __name__ == '__main__':

    installer = Installer()

    installer.parse_arguments()

    installer.install()

