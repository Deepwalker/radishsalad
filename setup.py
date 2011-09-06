#!/usr/bin/env python

import os.path
from setuptools import setup, find_packages



def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setupconf = dict(
    name = 'radishsalad',
    version = '0.1.0',
    license = 'BSD',
    url = 'https://github.com/Deepwalker/radishsalad/',
    author = 'Mikhail Krivushin',
    author_email = 'krivushinme@gmail.com',
    description = ('Redis datastore library'),
    long_description = read('README.rst'),

    packages = find_packages(),

    install_requires = ['redis'],
    test_loader = 'attest:Loader',
    test_suite = 'test.py',

    classifiers = [
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        ],
    )

if __name__ == '__main__':
    setup(**setupconf)
