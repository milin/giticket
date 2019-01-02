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

It integrates with [pre-commit](https://pre-commit.com/)

The following is a sample commit.

::

    repos:
    - repo:  https://github.com/milin/giticket
      rev: 'master'
      hooks:
      - id:  giticket
        args: ['--regex=SPROD-[0-9]']  # Optional 
       



Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
