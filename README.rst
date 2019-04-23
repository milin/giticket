========
giticket
========


.. image:: https://img.shields.io/pypi/v/giticket.svg
        :target: https://pypi.python.org/pypi/giticket

.. image:: https://travis-ci.com/milin/giticket.svg?branch=master
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

For e.g. if you name your branch ``JIRA-1234_awesome_feature`` and commit ``Fix some bug``, the commit will be updated to ``JIRA-1234 Fix some bug``.

Pass ``--regex=`` or update ``args: [--regex=<custom regex>]`` in your .yaml file if you have custom ticket regex.
By default it's ``[A-Z]+-\d+``.

Pass ``--format=`` or update ``args: [--format=<custom template string>]`` in your .yaml file if you have custom message replacement.
By default it's ``'{ticket} {commit_msg}``, where ``ticket`` is replaced with the found ticket number and ``commit_msg`` is replaced with the original commit message.


It is best used along with pre-commit_. You can use it along with pre-commit by adding the following hook in your ``.pre-commit-config.yaml`` file.

::

    repos:
    - repo:  https://github.com/milin/giticket
      rev: 'e0bf7ae'
      hooks:
      - id:  giticket
        args: ['--regex=PROJ-[0-9]', --format='"{ticket} {commit-msg}"']  # Optional


You need to have precommit setup to use this hook.
--------------------------------------------------
   Install Pre-commit and the commit-msg hook-type.


   ::

        pip install pre-commit==1.11.1
        pre-commit install
        pre-commit install --hook-type commit-msg


.. _pre-commit: https://pre-commit.com/
