from distutils.core import setup
from setuptools import setup, find_packages

setup(
  name = 'programy',
  packages=find_packages(),
  version = '1.8.0',
  description = 'AIML 2.0 Framework and Platform',
  author = 'Keith Sterling',
  author_email = 'keiffster@gmail.com',
  url = 'https://github.com/keiffster/program-y.git',
  download_url = 'https://github.com/keiffster/program-y/archive/1.8.0.tar.gz',
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
                    'metoffer']

)