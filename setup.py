#!/usr/bin/env python3
# encoding: utf-8

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import re
with open('mozilla_config.py') as file:
    version_pattern = re.compile("__version__ = '(.*)'")
    version = version_pattern.search(file.read()).group(1)

with open('README.rst') as file:
    readme = file.read()

setup(
    name='mozilla_config',
    version=version,
    author='Kale Kundert',
    author_email='kale@thekunderts.net',
    description="Backup and restore your Firefox and Thunderbird profiles.",
    long_description=readme,
    url='https://github.com/kalekundert/mozilla_config',
    pymodules=[
        'mozilla_config',
    ],
    entry_points = {
        'console_scripts': ['mozilla_config=mozilla_config:main'],
    },
    include_package_data=True,
    install_requires=[
        'docopt',
    ],
    license='MIT',
    zip_safe=False,
    keywords=[
        'mozilla',
        'firefox',
        'thunderbird',
        'profile',
        'backup',
        'restore',
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries',
    ],
)
