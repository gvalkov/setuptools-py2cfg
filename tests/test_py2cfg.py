import pytest
import textwrap
from pathlib import Path

import setuptools_py2cfg


@pytest.fixture
def empty_setup_py(tmpdir):
    return Path(tmpdir / 'setup.py')


@pytest.fixture
def testpkg1(request):
    return Path(request.fspath.dirname, 'testpkg1')


def test_execsetup(empty_setup_py: Path):
    empty_setup_py.write_text('from setuptools import setup; setup(a=1, b=2, c=3)')
    args, setup_dir = setuptools_py2cfg.execsetup(empty_setup_py)
    assert args == {'a': 1, 'b': 2, 'c': 3}
    assert setup_dir == empty_setup_py.parent


def test_full(testpkg1):
    res = setuptools_py2cfg.main([str(testpkg1 / 'setup.py')])
    assert res == textwrap.dedent('''\
    [metadata]
    name = ansimarkup
    version = 1.4.0
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
        pytest-cov >= 2.3.1
    devel =
        bumpversion >= 0.5.2
        check-manifest >= 0.35
        readme-renderer >= 16.0
        flake8
        pep8-naming''')
