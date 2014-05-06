#!/usr/bin/env python

import re
import os

from distutils.core import setup
from setuptools import find_packages


VERSIONFILE="mirskutils/_version.py"
verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))


dependencies = [
    'Django',
    'jsonfield',
    'South',
    'Sphinx',
    'django-compressor',
    'django-sekizai',
    'django-bootstrap-form',
    'django-admin-bootstrapped',
]



if os.environ.get('WITH_GEVENT',None) == 'true':
    os.environ['SERVER_INSTALL'] = 'true'
    dependencies.append('gevent >= 1.0dev')

if os.environ.get('SERVER_INSTALL', '') == 'true':
    dependencies.append('uwsgi')

if os.environ.get('WITH_MYSQL',None) == 'true':
    dependencies.append('mysqldb')
else:
    dependencies.append('psycopg2')



# dependency links deprecated in pip 1.5 and removed in pip 1.6

links = []


setup(name='MirskUtils',
      version=verstr,
      description='Mirsky Utility Functions',
      author='Andrew',
      author_email='andrew@mirsky.net',
      scripts=['bin/mirskutils-admin.py'],
      url='http://andrew.mirsky.com/',
      packages=find_packages(),
      include_package_data=True,
      install_requires=dependencies,
      dependency_links = links,
     )



