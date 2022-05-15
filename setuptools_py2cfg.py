#!/usr/bin/env python3

'''
converts an existing setup.py file to a setup.cfg in the format expected by setuptools
'''

import setuptools

import os, io, re, sys
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, FileType
from pathlib import Path
from functools import partial
from collections import defaultdict
from unittest.mock import Mock
from configparser import ConfigParser
import runpy


def parseargs(cli_args=None):
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter, description=__doc__)

    parser.add_argument(
        '-t', '--dangling-list-threshold', default=40, metavar='int', type=int,
        help='lists longer than this many characters are converted to a dangling list')
    parser.add_argument(
        '-i', '--dangling-list-indent', default=4, metavar='int', type=int,
        help='number of spaces to use when indenting dangling lists')
    parser.add_argument(
        '-a', '--always-use-dangling-lists', action='store_const', const=0, default=False,
        help='use dangling lists everywhere', dest='dangling_list_threshold')
    parser.add_argument(
        '-n', '--never-use-dangling-lists', action='store_const', const=99999, default=False,
        help='never use dangling lists', dest='dangling_list_threshold')
    parser.add_argument(
        'setup_py', type=FileType('r'), default='./setup.py', nargs='?', metavar='path',
        help='path to setup.py file')

    return parser.parse_args(cli_args)


def execsetup(setup_py: Path):
    # Mock all function in the setuptools module.
    global setuptools
    sys.modules['setuptools'] = Mock(spec=setuptools)
    import setuptools

    cwd = Path.cwd()
    # Evaluate setup.py with our mocked setuptools and get kwargs given to setup().
    try:
        os.chdir(str(setup_py.parent))
        #   runpy imports the file as a module and mocks it as __main__
        #   Reason : A lot of setup.py use __file__ and __name__ == "__main__"
        runpy.run_path(setup_py, {}, "__main__")
    finally:
        os.chdir(str(cwd))

    # Retrieve the arguments given to setup() in the target setup.py
    return setuptools.setup.call_args[1]


def main(cli_args=None):
    # Wrap _main() to test the output And avoid printing to stderr when running from the cli.
    print(_main(cli_args))


def _main(cli_args=None):
    args = parseargs(cli_args)
    setup_py = Path(args.setup_py.name).resolve()
    setuppy_dir = setup_py.parent
    setup_call_args = execsetup(setup_py)
    metadata, options, sections = py2cfg(setup_call_args, setuppy_dir, args.dangling_list_threshold)

    # Dump and reformat sections to ini format.
    config = ConfigParser(interpolation=None)
    if metadata:
        config['metadata'] = metadata
    if options:
        config['options'] = options
    for section, value in sections.items():
        config[section] = value

    # Load the existing setup.cfg if it exists
    setup_cfg = setuppy_dir / 'setup.cfg'
    if setup_cfg.exists():
        setup_cfg_parser = ConfigParser()
        with open(setup_cfg, 'r') as f:
            setup_cfg_parser.read_file(f)

        config = merge_configs(setup_cfg_parser, config)

    buf = io.StringIO()
    config.write(buf)

    # Convert leading tabs to spaces.
    res = re.sub('^(\t+)', ' ' * args.dangling_list_indent, buf.getvalue(), 0, re.MULTILINE)

    # Remove trailing whitespace.
    res = re.sub(' +$', '', res, 0, re.MULTILINE)
    return res.rstrip()


def py2cfg(setup, setuppy_dir, dangling_list_threshold):
    # Wrap these functions for convenience.
    global find_file, list_comma, list_semi, find_or_list_comma
    find_file = partial(find_file, setuppy_dir=setuppy_dir)
    list_comma = partial(list_comma, threshold=dangling_list_threshold)
    list_semi = partial(list_semi, threshold=dangling_list_threshold)

    sections = defaultdict(dict)

    find_or_list_comma = partial(find_or_list_comma, sections=sections, threshold=dangling_list_threshold)

    metadata = {}
    setif(setup, metadata, 'name')
    setif(setup, metadata, 'version')
    setif(setup, metadata, 'author')
    setif(setup, metadata, 'author_email')
    setif(setup, metadata, 'maintainer')
    setif(setup, metadata, 'maintainer_email')
    setif(setup, metadata, 'license', find_file)
    setif(setup, metadata, 'description')
    setif(setup, metadata, 'keywords', list_comma)
    setif(setup, metadata, 'url')
    setif(setup, metadata, 'download_url')
    setif(setup, metadata, 'long_description', find_file)
    setif(setup, metadata, 'long_description_content_type')
    setif(setup, metadata, 'classifiers', join_lines)
    setif(setup, metadata, 'platforms', list_comma)
    setif(setup, metadata, 'provides', list_comma)
    setif(setup, metadata, 'requires', list_comma)
    setif(setup, metadata, 'obsoletes', list_comma)
    setif(setup, metadata, 'project_urls', mapping)

    options = {}
    setif(setup, options, 'package_dir', mapping)
    setif(setup, options, 'py_modules', list_comma)
    setif(setup, options, 'packages', find_or_list_comma)
    setif(setup, options, 'zip_safe')
    setif(setup, options, 'setup_requires', list_semi)
    setif(setup, options, 'install_requires', list_semi)
    setif(setup, options, 'include_package_data')
    setif(setup, options, 'python_requires')
    setif(setup, options, 'use_2to3')
    setif(setup, options, 'use_2to3_fixers', list_comma)
    setif(setup, options, 'use_2to3_exclude_fixers', list_comma)
    setif(setup, options, 'convert_2to3_doctest', list_comma)
    setif(setup, options, 'scripts', list_comma)
    setif(setup, options, 'eager_resources', list_comma)
    setif(setup, options, 'dependency_links', list_comma)
    setif(setup, options, 'test_suite')
    setif(setup, options, 'tests_require', list_semi)
    setif(setup, options, 'include_package_data')
    setif(setup, options, 'namespace_packages', list_comma)
    setif(setup, options, 'include_package_data')

    entry_points = setup.get('entry_points')
    if entry_points:
        if isinstance(entry_points, dict):
            sections['options.entry_points'] = extract_section(entry_points)
        else:
            pass  # TODO: Handle entry_points in ini syntax.

    if 'extras_require' in setup:
        sections['options.extras_require'] = extract_section(setup['extras_require'])

    if 'package_data' in setup:
        sections['options.package_data'] = extract_section(setup['package_data'])

    if 'exclude_package_data' in setup:
        sections['options.exclude_package_data'] = extract_section(setup['exclude_package_data'])

    return metadata, options, sections


def find_file(content, setuppy_dir):
    '''
    Search for a file inside the setup.py directory matching the given text.
    Returns the original text if an exact match is not found.

      >>> find_file('BSD 3-Clause License\n\nCopyright....')
      'file: LICENSE'
      >>> find_file('Revised BSD License')
      'Revised BSD License'
    '''

    for path in (p for p in setuppy_dir.iterdir() if p.is_file()):
        try:
            if path.read_text() == content:
                return 'file: %s' % path.name
        except:
            pass
    return content


def join_lines(seq):
    return '\n' + '\n'.join(seq)


def list_semi(value, threshold):
    s = '; '.join(value)
    return join_lines(value) if len(s) > threshold else s


def mapping(value):
    return join_lines('\t' * 2 + k + " = " + v for k, v in value.items())


def list_comma_orig(value, threshold):
    ''''''
    value = value.split() if isinstance(value, str) else value
    s = ', '.join(value)
    return join_lines(value) if len(s) > threshold else s

list_comma = list_comma_orig


def ensure_list(value):
    return value if isinstance(value, (list, tuple)) else [value]


def find_or_list_comma(value, threshold, sections):
    # If find_packages() -> 'find:', else semicolon separated list.
    if isinstance(value, Mock):
        call = setuptools.find_packages.call_args
        args, findSection = list(call)
        if findSection:
            sections['options.packages.find'] = extract_section(findSection)

        return 'find:'

    return list_comma_orig(value, threshold)


def setif(src, dest, key, transform=None):
    '''Assign value to `dest` if `key` exists in `src`, while optionally
    applying a transformation to `src[key]`.'''

    if key in src:
        dest[key] = transform(src[key]) if transform else src[key]


def extract_section(value):
    '''
    Join all dictionary values into a semicolon separated list.

      >>> extract_section({'tests': ['pytest >= 3.0.0', 'tox >= 2.6.0']})
      {'tests': 'tox >= 2.6.0; pytest >= 3.0.0'}
    '''
    if isinstance(value, dict):
        return {k: list_semi(ensure_list(v)) for k, v in value.items()}


def merge_configs(cfg1, cfg2):
    """Merges two configurations"""
    def to_dict(cfg):
        return {k: dict(**v) for k, v in cfg.items()}

    def merge_dicts(d1, d2):
        d_out = {}

        # Get the set of all the keys between the two, trying to preserve
        # order (in Python 3.6) to avoid scrambling the sections randomly
        k1 = list(d1.keys())
        k2 = list(d2.keys())
        keys = set(d1.keys()) | set(d2.keys())

        def key_order(key):
            try:
                return k1.index(key)
            except ValueError:
                return k2.index(key)

        for k in sorted(keys, key=key_order):
            # The configuration dictionaries should be mappings from str to
            # dict, so if both keys are present, merge the dictionaries,
            # otherwise whichever one exists.
            v1 = d1.get(k, None)
            v2 = d2.get(k, None)

            assert not v1 or isinstance(v1, dict)
            assert not v2 or isinstance(v2, dict)

            if v1 and not v2:
                d_out[k] = v1
            elif v2 and not v1:
                d_out[k] = v2
            else:
                d_out[k] = v1.copy()
                d_out[k].update(v2)

        return d_out

    dict_merged = merge_dicts(*map(to_dict, (cfg1, cfg2)))

    merged_config = ConfigParser()
    merged_config.read_dict(dict_merged)

    return merged_config


if __name__ == '__main__':
    main()
