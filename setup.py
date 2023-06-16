#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages
requirements = [
    'pre-commit',
    'six'
]
setup_requirements = ['pytest-runner', ]
test_requirements = ['pytest', ]

setup(
    install_requires=requirements,
    include_package_data=True,
    keywords='gitmsg',
    name='gitmsg',
    packages=find_packages(include=['gitmsg']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    version='1.3.0',
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'gitmsg=gitmsg.gitmsg:main',
        ]

    }
)
