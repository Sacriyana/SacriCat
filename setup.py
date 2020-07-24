#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from distutils.core import setup, Extension
import sacricat

setup (
    name = 'sacricat',
    version = sacricat.__version__,
    author = 'Sacriyana',
    author_email = '10485983+Sacriyana@users.noreply.github.com',
    license ='CC BY-NC',
    keywords="networking, security, ctf",
    platforms=[
        "Operating System :: OS Independent",
    ],
    packages=['sacricat',],
    url = 'https://github.com/Sacriyana/SacriCat',
    bugtrack_url = 'https://github.com/Sacriyana/SacriCat',
    description = 'SacriCat is a socket toolbox for hackers in CTF for both side, player and creator.',
    long_description=open('readme.md').read() + "\n",
)
