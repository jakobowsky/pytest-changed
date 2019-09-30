==============
pytest-changed
==============

.. image:: https://img.shields.io/pypi/v/pytest-changed.svg
    :target: https://pypi.org/project/pytest-changed
    :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/pytest-changed.svg
    :target: https://pypi.org/project/pytest-changed
    :alt: Python versions

.. image:: https://travis-ci.org/gastrofix-gmbh/pytest-changed.svg?branch=master
    :target: https://travis-ci.org/gastrofix-gmbh/pytest-changed
    :alt: See Build Status on Travis CI

.. image:: https://ci.appveyor.com/api/projects/status/github/gastrofix-gmbh/pytest-changed?branch=master
    :target: https://ci.appveyor.com/project/gastrofix-gmbh/pytest-changed/branch/master
    :alt: See Build Status on AppVeyor

A pytest plugint that finds changed tests and runs only those.

Features
--------

Passing the :code:`--changed` flag to your pytest run, you will not only select changed files but also identify the functions that have been changed.

Installation
------------

You can install "pytest-changed" via `pip`_ from `PyPI`_::

    $ pip install pytest-changed


Usage
-----

You just have to invoke pytest and pass the :code:`--changed` flag to it::

    $ pytest --changed

Requirements
------------

* TODO


Contributing
------------
Contributions are very welcome. Tests can be run with `tox`_, please ensure
the coverage at least stays the same before you submit a pull request.

License
-------

Distributed under the terms of the `Mozilla Public License 2.0`_ license, "pytest-changed" is free and open source software


Issues
------

If you encounter any problems, please `file an issue`_ along with a detailed description.

.. _`Cookiecutter`: https://github.com/audreyr/cookiecutter
.. _`@hackebrot`: https://github.com/hackebrot
.. _`MIT`: http://opensource.org/licenses/MIT
.. _`BSD-3`: http://opensource.org/licenses/BSD-3-Clause
.. _`GNU GPL v3.0`: http://www.gnu.org/licenses/gpl-3.0.txt
.. _`Apache Software License 2.0`: http://www.apache.org/licenses/LICENSE-2.0
.. _`cookiecutter-pytest-plugin`: https://github.com/pytest-dev/cookiecutter-pytest-plugin
.. _`file an issue`: https://github.com/gastrofix-gmbh/pytest-changed/issues
.. _`pytest`: https://github.com/pytest-dev/pytest
.. _`tox`: https://tox.readthedocs.io/en/latest/
.. _`pip`: https://pypi.org/project/pip/
.. _`PyPI`: https://pypi.org/project

----

This `pytest`_ plugin was generated with `Cookiecutter`_ along with `@hackebrot`_'s `cookiecutter-pytest-plugin`_ template.
