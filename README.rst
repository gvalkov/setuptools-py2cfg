setuptools-py2cfg
=================

.. class:: no-web no-pdf

|pypi| |build| |license|

Since version 30.3.0, `setuptools supports`_ declarative configuration through the
``setup.cfg`` file. This script helps convert existing ``setup.py`` files to
``setup.cfg`` in the format expected by setuptools.



Usage
-----

Just point ``setuptools-py2cfg`` to a ``setup.py`` file or run it in a directory
containing a ``setup.py``. For example,  given the following ``setup.py``:

.. code-block:: python

  from setuptools import setup, find_packages

  classifiers = [
      'Development Status :: 5 - Production/Stable',
      'Programming Language :: Python :: 2.7',
      'Programming Language :: Python :: 3',
      'Programming Language :: Python :: 3.3',
      'Programming Language :: Python :: 3.4',
      'Programming Language :: Python :: 3.5',
      'Programming Language :: Python :: 3.6',
      'Intended Audience :: Developers',
      'Topic :: Software Development :: Libraries',
      'License :: OSI Approved :: BSD License',
  ]

  extras_require = {
      'tests': [
          'tox >= 2.6.0',
          'pytest >= 3.0.3',
      ],
      'devel': [
          'check-manifest >= 0.35',
          'readme-renderer >= 16.0',
      ]
  }

  kw = {
      'name':                 'ansimarkup',
      'version':              '1.3.0',

      'description':          'Produce colored terminal text with an xml-like markup',
      'long_description':     open('README.rst').read(),

      'author':               'Georgi Valkov',
      'author_email':         'georgi.t.valkov@gmail.com',
      'license':              'Revised BSD License',
      'keywords':             'ansi terminal markup',
      'url':                  'https://github.com/gvalkov/python-ansimarkup',
      'classifiers':          classifiers,
      'install_requires':     'colorama',
      'extras_require':       extras_require,
      'packages':             find_packages(),
      'zip_safe':             True,
  }

  if __name__ == '__main__':
      setup(**kw)

Running ``setuptools-py2cfg`` would print:

.. code-block:: ini

  [metadata]
  name = ansimarkup
  version = 1.3.0
  author = Georgi Valkov
  author_email = georgi.t.valkov@gmail.com
  license = Revised BSD License
  description = Produce colored terminal text with an xml-like markup
  keywords = ansi, terminal, markup
  url = https://github.com/gvalkov/python-ansimarkup
  long_description = file: README.rst
  classifiers =
      Development Status :: 5 - Production/Stable
      Programming Language :: Python :: 2.7
      Programming Language :: Python :: 3
      Programming Language :: Python :: 3.3
      Programming Language :: Python :: 3.4
      Programming Language :: Python :: 3.5
      Programming Language :: Python :: 3.6
      Intended Audience :: Developers
      Topic :: Software Development :: Libraries
      License :: OSI Approved :: BSD License

  [options]
  packages = find:
  zip_safe = True
  install_requires = colorama

  [options.extras_require]
  tests =
      tox >= 2.6.0
      pytest >= 3.0.3
  devel =
      check-manifest >= 0.35
      readme-renderer >= 16.0

There are several non-essential options that control the format of the generated ini-file::

  usage: setuptools-py2cfg.py [-h] [-t int] [-i int] [-a] [path]

  converts an existing setup.py file to a setup.cfg in the format expected by
  setuptools

  positional arguments:
    path                  path to setup.py file (default: ./setup.py)

  optional arguments:
    -h, --help            show this help message and exit
    -t int, --dangling-list-threshold int
                          lists longer than this many characters are converted
                          to a dangling list (default: 40)
    -i int, --dangling-list-indent int
                          number of spaces to use when indenting dangling lists
                          (default: 4)
    -a, --always-use-dangling-lists
                          use dangling lists everywhere (default: False)

Keep in mind that a ``setup.py`` file with a single call to
``setuptools.setup()`` is still needed after migrating all metadata to ``setup.cfg``.


Installation
------------

The latest stable version of setuptools-py2cfg can be installed from pypi:

.. code-block:: bash

  $ pip install setuptools-py2cfg


Todo
----

- Handle ``entry_scripts`` in ini-format.
- Write a test or two.


License
-------

Released under the terms of the `Revised BSD License`_.


.. |pypi| image:: https://img.shields.io/pypi/v/setuptools-py2cfg.svg?style=flat-square&label=latest%20stable%20version
    :target: https://pypi.python.org/pypi/setuptools-py2cfg
    :alt: Latest version released on PyPi

.. |license| image:: https://img.shields.io/pypi/l/setuptools-py2cfg.svg?style=flat-square&label=license
    :target: https://pypi.python.org/pypi/setuptools-py2cfg
    :alt: BSD 3-Clause

.. |build| image:: https://img.shields.io/travis/gvalkov/setuptools-py2cfg/master.svg?style=flat-square&label=build
    :target: http://travis-ci.org/gvalkov/python-setuptools-py2cfg
    :alt: Build status

.. _`Revised BSD License`: https://raw.github.com/gvalkov/setuptools-py2cfg/master/LICENSE
.. _`setuptools supports`: http://setuptools.readthedocs.io/en/latest/setuptools.html#configuring-setup-using-setup-cfg-files
