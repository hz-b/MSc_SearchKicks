#!/usr/bin/python
from setuptools import setup, find_packages

setup(name = 'search_kicks',
      version = '0.1.0',
      maintainer = 'Olivier Churlaud',
      maintainer_email= 'olivier@.churlaud.com',
      description = 'Various tools to find kicks and work on orbit data',
      url = 'https://github.com/ochurlaud/MSc_SearchKicks',
      package_dir = {'search_kicks': 'search_kicks'},
      packages=find_packages(),
    )
