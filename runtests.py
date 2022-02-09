#!/usr/bin/python3 -u
"""
Run the test suite on multiple Python versions.

Usage::

    python3 test_matrix.py
    python3 test_matrix.py -v # verbose mode
"""
from __future__ import absolute_import
from __future__ import print_function
import argparse
import os.path
import shutil
import subprocess
import sys
try:
    from shutil import which
except ImportError:
    # Python 2
    from distutils.spawn import find_executable as which


from tests.utils import run_command


TEST_DIR = os.path.join(os.path.dirname(__file__), 'tests')
TEST_COMPAT = os.path.join(TEST_DIR, "test_pythoncapi_compat.py")
TEST_UPGRADE = os.path.join(TEST_DIR, "test_upgrade_pythoncapi.py")

PYTHONS = (
    "python2.7",
    "python3.4",
    "python3.5",
    "python3.6",
    "python3.7",
    "python3.8",
    "python3.9",
    "python3.10",
    "python3.11",
    "python3",
    "python3-debug",
    "pypy",
    "pypy2",
    "pypy2.7",
    "pypy3",
    "pypy3.6",
    "pypy3.7",
)


def run_tests_exe(executable, verbose, tested):
    executable = os.path.realpath(executable)
    if executable in tested:
        return

    cmd = [executable, TEST_COMPAT]
    if verbose:
        cmd.append('-v')
    run_command(cmd)
    tested.add(executable)


def run_tests(python, verbose, tested):
    executable = which(python)
    if not executable:
        print("Ignore missing Python executable: %s" % python)
        return
    run_tests_exe(executable, verbose, tested)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action="store_true",
                        help='Verbose mode')
    parser.add_argument('-c', '--current', action="store_true",
                        help="Only test the current Python executable "
                             "(don't test multiple Python versions)")
    return parser.parse_args()


def main():
    args = parse_args()

    path = os.path.join(TEST_DIR, 'build')
    if os.path.exists(path):
        shutil.rmtree(path)

    # upgrade_pythoncapi.py requires Python 3.6 or newer
    if sys.version_info >= (3, 6):
        print("Run %s" % TEST_UPGRADE)
        cmd = [sys.executable, TEST_UPGRADE]
        if args.verbose:
            cmd.append('-v')
        run_command(cmd)
    else:
        print("Don't test upgrade_pythoncapi.py: it requires Python 3.6")
    print()

    tested = set()
    if not args.current:
        for python in PYTHONS:
            run_tests(python, args.verbose, tested)
        run_tests_exe(sys.executable, args.verbose, tested)

        print()
        print("Tested: %s Python executables" % len(tested))
    else:
        run_tests_exe(sys.executable, args.verbose, tested)


if __name__ == "__main__":
    main()
