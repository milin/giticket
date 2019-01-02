========
giticket
========


.. image:: https://img.shields.io/pypi/v/giticket.svg
        :target: https://pypi.python.org/pypi/giticket

.. image:: https://img.shields.io/travis/milin/giticket.svg
        :target: https://travis-ci.org/milin/giticket

.. image:: https://readthedocs.org/projects/giticket/badge/?version=latest
        :target: https://giticket.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




Auto add ticket info to your git commits.


* Free software: MIT license
* Documentation: https://giticket.readthedocs.io.


Features
--------

This hook saves developers time by prepending ticket numbers to commit-msgs.
For this to work the following two conditions must be met:
   - The ticket format regex specified must match, if the regex is passed in.
   - The branch name format must be <ticket number>_<rest of the branch name>

For e.g. if you name your branch `JIRA-1234_awesome_feature` and commit `Fix some bug`, the commit will be updated to `JIRA-1234 Fix some bug`. Pass `--regex=` or update `args: [--regex=<custom regex>]` in your .yaml file if you have custom ticket regex. By default its `[A-Z]+-\d+`.

It is best used along with pre_commit_.

The following is a sample commit.

::

    repos:
    - repo:  https://github.com/milin/giticket
      rev: 'master'
      hooks:
      - id:  giticket
        args: ['--regex=SPROD-[0-9]']  # Optional 


.. _pre-commit: https://pre-commit.com/
