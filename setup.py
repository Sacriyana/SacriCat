#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from distutils.core import setup, Extension
import sacricat

# Install : python setup.py install
# Register : python setup.py register

#  platform = 'Unix',
#  download_url = 'http://xael.org/norman/python/python-nmap/',


setup (
    name = 'sacricat',
    version = sacricat.__version__,
    author = 'Sacriyana',
    author_email = 'localhost@localhost',
    license ='CC BY-NC',
    keywords="networking, security",
    # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    platforms=[
        "Operating System :: OS Independent",
        ],
    packages=['sacricat',],
    url = 'https://github.com/Sacriyana/SacriCat',
    bugtrack_url = 'https://github.com/Sacriyana/SacriCat',
    description = 'SacriCat is a toolbox for hackers in CTF for both side, player or creator',
    long_description=open('readme.md').read() + "\n",
    )
