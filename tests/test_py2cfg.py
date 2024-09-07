import pytest
import textwrap
from pathlib import Path

import setuptools_py2cfg
from .util import generate_package, compare_configs, configs_to_str


@pytest.fixture
def empty_setup_py(tmpdir):
    return Path(tmpdir / "setup.py")


@pytest.fixture
def testpkg1(request):
    return Path(request.fspath.dirname, "testpkg1")


@pytest.fixture
def tmpdir_cwd(tmpdir):
    with tmpdir.as_cwd():
        yield tmpdir


def test_execsetup(empty_setup_py: Path):
    empty_setup_py.write_text("from setuptools import setup; setup(a=1, b=2, c=3)")
    args = setuptools_py2cfg.execsetup(empty_setup_py)
    assert args == {"a": 1, "b": 2, "c": 3}


def test_full(testpkg1):
    res = setuptools_py2cfg._main([str(testpkg1 / "setup.py")])
    assert res == textwrap.dedent("""\
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
    project_urls =
        Repo = https://github.com/gvalkov/setuptools-py2cfg

    [options]
    package_dir =
         = src1
        a = src2
    packages = find:
    zip_safe = True
    install_requires = colorama
    test_suite = tests.test

    [options.packages.find]
    where = src1
    exclude = tests; unneeded

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
        pep8-naming""")


def _setup_cfg_merge_params():
    params = [
        # Basic
        (
            {
                "setup.py": """
            from setuptools import setup, find_packages

            setup(packages=find_packages())
            """,
                "setup.cfg": """
            [metadata]
            name=foo
            version=1.0.0
            """,
            },
            {
                "metadata": {
                    "name": "foo",
                    "version": "1.0.0",
                },
                "options": {"packages": "find:"},
            },
        ),
        # Merging the "options" section
        (
            {
                "setup.py": """
            from setuptools import setup, find_packages

            setup(packages=find_packages())
            """,
                "setup.cfg": """
            [metadata]
            name=foo
            version=1.0.0

            [options]
            install_requires=python-dateutil
            """,
            },
            {
                "metadata": {
                    "name": "foo",
                    "version": "1.0.0",
                },
                "options": {
                    "install_requires": "python-dateutil",
                    "packages": "find:",
                },
            },
        ),
        # Both add a section
        (
            {
                "setup.py": """
            from setuptools import setup

            setup(extras_require={
                'tests': ['pytest'],
            })
            """,
                "setup.cfg": """
            [metadata]
            name=foo
            version=1.0.0

            [options]
            install_requires=python-dateutil
            """,
            },
            {
                "metadata": {
                    "name": "foo",
                    "version": "1.0.0",
                },
                "options": {
                    "install_requires": "python-dateutil",
                },
                "options.extras_require": {
                    "tests": "pytest",
                },
            },
        ),
    ]

    return params


@pytest.mark.parametrize("files, expected", _setup_cfg_merge_params())
def test_setup_cfg_merge(files, expected, tmpdir_cwd):
    generate_package(tmpdir_cwd, files)

    res = setuptools_py2cfg._main([str(tmpdir_cwd / "setup.py")])

    assert compare_configs(res, expected), configs_to_str(res, expected)
