from setuptools import setup, find_packages
from os import path
import sys

version = None
if "--version" in sys.argv:
    index = sys.argv.index('--version')
    sys.argv.pop(index)
    version = sys.argv[index]
    sys.argv.pop(index)

if version is None:
    print("--version x.y.z missing from command line")
    exit(0)

download_url = "https://github.com/keiffster/program-y/%s.tar.gz"%version

here = path.abspath(path.dirname(__file__))
with open(path.join(here, '../README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
  name = 'programy',
  packages=find_packages(),
  package_data={'': ['*.conf', '*.aiml']},
  include_package_data=True,
  version = version,
  description = 'AIML Framework and Platform',
  long_description=long_description,
  author = 'Keith Sterling',
  author_email = 'keiffster@gmail.com',
  url = 'https://github.com/keiffster/program-y.git',
  download_url = download_url,
  keywords = ['aiml', 'chatbot', 'virtual assistant', 'ai'],
  classifiers = [
      # How mature is this project? Common values are
      #   3 - Alpha
      #   4 - Beta
      #   5 - Production/Stable
      'Development Status :: 5 - Production/Stable',

      # Indicate who your project is intended for
      'Intended Audience :: Developers',

      # Pick your license as you wish (should match "license" above)
      'License :: OSI Approved :: MIT License',

      # Specify the Python versions you support here. In particular, ensure
      # that you indicate whether you support Python 2, Python 3 or both.
      'Programming Language :: Python :: 3',
      'Programming Language :: Python :: 3.2',
      'Programming Language :: Python :: 3.3',
      'Programming Language :: Python :: 3.4',
      'Programming Language :: Python :: 3.5',
      'Programming Language :: Python :: 3.6',
  ],
  install_requires=['requests',
                    'flask',
                    'python-dateutil',
                    'beautifulsoup4',
                    'lxml',
                    'wikipedia',
                    'pyyaml',
                    'tweepy',
                    'sleekxmpp',
                    'metoffer',
                    'python-telegram-bot',
                    'pymessenger',
                    'twilio',
                    'slackclient',
                    'redis',
                    'viberbot',
                    'line-bot-sdk',
                    'kik',
                    'APScheduler',
                    'emoji'
                    ]

)