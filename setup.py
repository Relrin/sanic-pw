#!/usr/bin/env python
from os import path as op
from setuptools import setup


def _read(fname):
    try:
        return open(op.join(op.dirname(__file__), fname)).read()
    except IOError:
        return ''


install_requires = [
    l for l in _read('requirements.txt').split('\n')
    if l and not l.startswith('#') and not l.startswith('-')]


setup(
    name="Sanic-PW",
    version="0.1.0",
    license="BSD",
    description='Peewee ORM integration for Sanic framework',
    long_description=_read('README.md'),
    platforms=('Any'),
    keywords = ("sanic", "peewee", "migrations", "migrate", "signals"),
    author='Valeryi Savich',
    author_email='Relrin78@gmail.com',
    url='https://github.com/Relrin/sanic-pw',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Natural Language :: Russian',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Testing',
        'Topic :: Utilities',
    ],
    packages=['sanic_pw', ],
    include_package_data=True,
    install_requires=install_requires,
)
