========
giticket
========

.. image:: https://api.star-history.com/svg?repos=milin/giticket&type=Date)](https://star-history.com/#milin/giticket&Date

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
   - Unless you use ``regex_match`` mode, the branch name format must be <ticket number>_<rest of the branch name>

For e.g. if you name your branch ``JIRA-1234_awesome_feature`` and commit ``Fix some bug``, the commit will be updated to ``JIRA-1234 Fix some bug``.

Pass ``--regex=`` or update ``args: [--regex=<custom regex>]`` in your .yaml file if you have custom ticket regex.
By default it's ``[A-Z]+-\d+``.

Pass ``--format=`` or update ``args: [--format=<custom template string>]`` in your .yaml file if you have custom message replacement.
By default it's ``'{ticket} {commit_msg}``, where ``ticket`` is replaced with the found ticket number and ``commit_msg`` is replaced with the original commit message.

Pass ``--mode=`` or update ``args: [--mode=regex_match]`` in your .yaml file to extract ticket by the regex rather than relying on branch name convention.
With this mode you can also make use of ``{tickets}`` placeholder in ``format`` argument value to put multiple comma-separated tickets in the commit message in case your branch contains more than one ticket.

Pass ``--capitalize`` or ``--capitalize=N`` to capitalize the first ``N`` characters of the resulting commit message. When passed without a value, defaults to capitalizing the first character (``--capitalize=1``).

Pass ``--to_trailer`` to append the ticket(s) as a `git trailer <https://git-scm.com/docs/git-interpret-trailers>`_ at the bottom of the commit message instead of modifying the subject line. For example, committing on branch ``JIRA-1234_awesome_feature`` will append::

    Refs: JIRA-1234

Pass ``--trailer_token=`` to customise the trailer key written by ``--to_trailer``. Defaults to ``Refs``. For example, ``--trailer_token=Fixes`` produces::

    Fixes: JIRA-1234

It is best used along with pre-commit_. You can use it along with pre-commit by adding the following hook in your ``.pre-commit-config.yaml`` file.

::

    repos:
    - repo:  https://github.com/milin/giticket
      rev: v1.92
      hooks:
      - id:  giticket
        args: ['--regex=PROJ-[0-9]', '--format={ticket} {commit_msg}']  # Optional

Alternatively, to append tickets as a trailer instead of modifying the subject line:

::

    repos:
    - repo:  https://github.com/milin/giticket
      rev: v1.92
      hooks:
      - id:  giticket
        args: ['--to_trailer', '--trailer_token=Refs']  # --trailer_token is optional, defaults to Refs


You need to have precommit setup to use this hook.
--------------------------------------------------
   Install Pre-commit and the commit-msg hook-type.


   ::

        pip install pre-commit
        pre-commit install
        pre-commit install --hook-type commit-msg


.. _pre-commit: https://pre-commit.com/
