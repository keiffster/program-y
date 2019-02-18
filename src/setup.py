from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

version = None
with open(path.join(here, 'version.txt'), encoding='utf-8') as f:
    version = f.read()
version = version.strip()
print("Building PyPi Package for version %s"%version)

if version is None:
    print("No version.txt found")

long_description = ""
with open(path.join(here, path.join(here, 'README.md')), encoding='utf-8') as f:
    long_description = f.read()

download_url = "https://github.com/keiffster/program-y/%s.tar.gz"%version

setup(
  name = 'programy',
  packages=find_packages(),
  package_data={'': ['*.conf', '*.aiml']},
  include_package_data=True,
  version = version,
  description = 'AIML Framework and Platform',
  long_description=long_description,
  long_description_content_type='text/markdown',
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
      'Programming Language :: Python :: 3.7',
  ],
  install_requires=[
    'python-dateutil==2.7.3',
    'beautifulsoup4==4.6.3',
    'lxml==4.2.5',
    'PyYAML==4.2b4',
    'requests==2.20.0',
    'Flask==1.0.2',
    'Flask-SocketIO==3.0.2',
    'tweepy==3.6.0',
    'sleekxmpp==1.3.3',
    'python-telegram-bot==11.1.0',
    'pymessenger==0.0.7.0',
    'twilio==6.18.1',
    'slackclient==1.3.0',
    'viberbot==1.0.11',
    'line-bot-sdk==1.8.0',
    'kik==1.5.0',
    'wikipedia==1.4.0',
    'MetOffer==1.3.2',
    'APScheduler==3.5.3',
    'emoji==0.5.1',
    'autocorrect==0.3.0',
    'redis==2.10.6',
    'pymongo==3.7.1',
    'SQLAlchemy==1.2.12',
    'PyMySQL==0.9.2',
    'wget==3.2',
    'textblob==0.15.2'
]
)