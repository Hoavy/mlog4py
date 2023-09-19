#!/usr/bin/env python
#coding:utf-8

import os
import re
from setuptools import setup, find_packages


def find_package_info(*file_paths):
    try:
        with open(os.path.join(*file_paths), 'r') as f:
            info_file = f.read()
    except Exception:
        raise RuntimeError("Unable to find package info.")

    # The version line must have the form
    # __version__ = 'ver'
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              info_file, re.M)
    author_match = re.search(r"^__author__ = ['\"]([^'\"]*)['\"]",
                             info_file, re.M)

    if version_match and author_match:
        return version_match.group(1), author_match.group(1)
    raise RuntimeError("Unable to find package info.")

here = os.path.abspath(os.path.dirname(__file__))
__version__, __author__ = find_package_info(here, 'src', 'release.py')

setup(
    name='mlog4py',
    version=__version__,
    description='Python library for mlogger',
    author=__author__,
    author_email='d@wanghaowei.com',
    
    python_requires='>=2.7',
    package_dir={
        '': 'src',
        },
    packages=find_packages('src'),
    include_package_data=True,
    scripts=[
        ],
    data_files=[],
    zip_safe=False
)
