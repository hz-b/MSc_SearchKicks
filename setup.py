#!/usr/bin/python
from setuptools import setup, find_packages

setup(name = 'search_kicks',
      version = '0.1.0',
      maintainer = 'Olivier Churlaud',
      maintainer_email= 'olivier.churlaud@helmholtz-berlin.de',
      description = 'Various tools to find kicks and work on orbit data',
      url = 'aragon.acc.bessy.de:/opt/repositories/controls/git/tools/search_kicks.git',
      package_dir = {'search_kicks': 'search_kicks'},
      packages=find_packages(),
    )
