# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 00:23:29 2018

@author: khanhphamdinh
"""

from setuptools import setup, find_packages, find_namespace_packages

try:
    from pypandoc import convert
    read_md = lambda f: convert(f, 'rst')
except ImportError:
    print("warning: pypandoc module not found, could not convert Markdown to RST")
    read_md = lambda f: open(f, 'r').read()

DISTNAME = 'core_nlp'
INSTALL_REQUIRES = (
    ['pandas>=0.19.2', 'requests>=2.3.0', 'wrapt>=1.10.0', 'lxml>=4.3.0', 'pypandoc>=1.4']
)

VERSION = '0.0.1'
LICENSE = 'MIT'
DESCRIPTION = 'Viet Nam NLP'
AUTHOR = "KhanhPhamDinh"
EMAIL = "phamdinhkhanh.tkt53.neu@gmail.com"
URL = "https://github.com/phamdinhkhanh/core_nlp"
DOWNLOAD_URL = 'https://github.com/phamdinhkhanh/core_nlp'

setup(name=DISTNAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=read_md('README.md'),
      author=AUTHOR,
      author_email=EMAIL,
      url=URL,
      license = LICENSE,
      #package name are looked in python path
      # packages=find_packages(exclude = ['contrib', 'docs', 'tests*']),
      # version="0.0.1",
      packages=find_packages(include=['core_nlp','core_nlp.*']),
      package_data={
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst'],
        # And include any *.msg files found in the 'tokenization' package, too:
        'tokenization': ['*.txt'],
      },
      classifiers=[
        'Development Status :: 0 - Alpha',
        'Environment :: Console',
        'Intended Audience :: NLP',
        'Operating System :: OS Independent',
        'Programming Language :: Cython',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Financial/Stock Market',
      ],

      keywords = 'nlp',
      install_requires=INSTALL_REQUIRES,
      zip_safe=False,
     )
