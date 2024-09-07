# setuptools-py2cfg

<p>
    <a href="https://pypi.python.org/pypi/setuptools-py2cfg"><img alt="pypi version" src="https://img.shields.io/pypi/v/setuptools-py2cfg.svg"></a>
    <a href="https://github.com/gvalkov/setuptools-py2cfg/actions/workflows/tox.yml?query=branch:main"><img alt="Build status" src="https://img.shields.io/github/actions/workflow/status/gvalkov/setuptools-py2cfg/tox.yml?branch=main"></a>
    <a href="https://github.com/gvalkov/setuptools-py2cfg/blob/main/LICENSE.txt"><img alt="License" src="https://img.shields.io/pypi/l/setuptools-py2cfg"></a>
</p>


Since version 30.3.0, [setuptools supports] declarative configuration through
the `setup.cfg` file. This script helps convert existing `setup.py` files to
`setup.cfg` in the format expected by setuptools.

A `setup.cfg` file may be migrated to `pyproject.toml` with the help of
[`ini2toml`](https://pypi.org/project/ini2toml) and
[`validate-pyproject`](https://github.com/abravalheri/validate-pyproject).


## Usage

Just point `setuptools-py2cfg` to a `setup.py` file or run it in a directory
containing `setup.py`. For example, given the following `setup.py`:

``` python
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
```

Running `setuptools-py2cfg.py` would print:

``` ini
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
```

There are several non-essential options that control the format of the
generated ini-file:

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

Keep in mind that a `setup.py` file with a single call to `setuptools.setup()`
is still needed after migrating all metadata to `setup.cfg`.

## Installation

The latest stable version of setuptools-py2cfg can be installed from
pypi:

``` bash
$ pip install setuptools-py2cfg
```

## Todo

-   Handle `entry_scripts` in ini-format.
-   Write a test or two.

## License

Released under the terms of the [Revised BSD License].

  [setuptools supports]: https://setuptools.readthedocs.io/en/latest/userguide/declarative_config.html
  [Revised BSD License]: https://raw.github.com/gvalkov/setuptools-py2cfg/master/LICENSE
