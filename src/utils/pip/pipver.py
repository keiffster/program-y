import json
from urllib.request import urlopen, Request
from packaging.version import Version

def get_current_versions(req_file):

    with open(req_file, "r") as file:
        for line in file:
            line = line.strip()
            if line:
                if line.startswith('#') is False:
                    name_ver = line.split('==')
                    try:
                        url = "https://pypi.python.org/pypi/%s/json" % (name_ver[0])
                        data = json.load(urlopen(Request(url)))
                        versions = list(data["releases"].keys())
                        versions.sort(key=Version)
                        latest = versions[len(versions) - 1]
                        print("Package: %s, current: %s, latest: %s" % (name_ver[0], name_ver[1], latest))
                    except Exception as e:
                        print(name_ver)
                        print(e)

if __name__ == '__main__':

    get_current_versions("../../../requirements.txt")
